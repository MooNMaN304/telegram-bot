"""Парсер расписаний через OpenRouter API (OpenAI-совместимый).

Используется вместо GigaChat для экономии токенов.
OpenRouter аггрегирует множество моделей — можно переключаться между ними
через settings.OPENROUTER_MODEL.

Поддерживает тот же интерфейс, что и GigaChatScheduleParser.
"""

import json
from typing import List, Type

from openai import OpenAI
from pydantic import BaseModel, ValidationError

from src.utils.logger import get_logger

logger = get_logger(__name__)


class OpenRouterScheduleParser:
    """Парсер расписаний через OpenRouter.

    Использует OpenAI-совместимый клиент для запросов к OpenRouter API.
    """

    def __init__(
        self,
        api_key: str,
        response_schema: Type[BaseModel],
        model: str = "tencent/hy3-preview",
        max_retries: int = 5,
        temperature: float = 0.2,
        base_url: str = "https://openrouter.ai/api/v1",
    ):
        self._api_key = api_key
        self._model = model
        self._base_url = base_url
        self._client = None  # Lazy initialization

        self.response_schema = response_schema
        self.max_retries = max_retries
        self.temperature = temperature

        self.system_prompt = (
            "Ты эксперт по парсингу HTML-расписаний сеансов кинотеатров Kinomax.\n"
            "Извлекай ТОЛЬКО данные о сеансах.\n"
            "Верни строго JSON без пояснений.\n"
            "{\n"
            '  "sessions": [\n'
            '    {"time": "16:25", "price": 750, "format": "2D"}\n'
            "  ]\n"
            "}\n"
            "Если сеансов нет — верни пустой массив."
        )

        self.user_prompt_template = (
            "HTML расписания:\n\n{html_content}\n\n"
            "Извлеки сеансы."
        )

    @property
    def client(self):
        """Ленивая инициализация OpenAI-клиента."""
        if self._client is None:
            logger.info("Инициализация OpenRouter клиента (первый вызов)...")
            self._client = OpenAI(
                api_key=self._api_key,
                base_url=self._base_url,
                timeout=30,
            )
            logger.info("OpenRouter клиент инициализирован (model=%s)", self._model)
        return self._client

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """Грубая оценка токенов"""
        return len(text) // 4

    def parse_cinema_schedule(self, html_content: str):
        """Парсит HTML расписание и возвращает распарсенные сеансы.

        Args:
            html_content: HTML-код блока с расписанием

        Returns:
            GigaChatScheduleResponse (или другая response_schema) с сеансами
        """
        try:
            # Ограничение HTML
            max_html_length = 50000
            if len(html_content) > max_html_length:
                logger.warning(
                    "HTML слишком большой (%d), обрезаем до %d",
                    len(html_content),
                    max_html_length,
                )
                html_content = html_content[:max_html_length]

            user_prompt = self.user_prompt_template.format(
                html_content=html_content
            )

            # Базовые messages (НЕ МЕНЯЮТСЯ)
            base_messages: List[dict] = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            # лог размера входа
            input_size = sum(len(m["content"]) for m in base_messages)
            logger.info(
                "📊 INPUT SIZE: %d chars (~%d tokens)",
                input_size,
                self._estimate_tokens("".join(m["content"] for m in base_messages)),
            )

            last_error = None

            for attempt in range(1, self.max_retries + 2):
                logger.info("🔁 Попытка #%d", attempt)

                messages = base_messages.copy()

                if attempt > 1:
                    messages.append({
                        "role": "user",
                        "content": (
                            "Исправь JSON. Верни ТОЛЬКО валидный JSON без объяснений.\n"
                            "ВАЖНО: цена (price) должна быть ЧИСЛОМ, без символа ₽ и без слова 'от'.\n"
                            'Пример: {"time": "16:25", "price": 750, "format": "2D"}\n'
                            "Никаких кавычек вокруг price, никаких 'от', никаких ₽."
                        )
                    })

                try:
                    response = self.client.chat.completions.create(
                        model=self._model,
                        messages=messages,
                        temperature=self.temperature,
                    )

                    # Логируем usage
                    if hasattr(response, "usage") and response.usage:
                        usage = response.usage
                        logger.info(
                            "🔥 TOKENS | prompt=%s | completion=%s | total=%s",
                            getattr(usage, "prompt_tokens", "?"),
                            getattr(usage, "completion_tokens", "?"),
                            getattr(usage, "total_tokens", "?"),
                        )

                    content = response.choices[0].message.content.strip()

                    logger.debug(
                        "Ответ OpenRouter (первые 150 символов): %s",
                        content[:150],
                    )

                    # чистка ```json
                    if content.startswith("```"):
                        content = (
                            content.split("```json", 1)[-1]
                            .split("```", 1)[0]
                            .strip()
                        )

                    data = json.loads(content)
                    validated = self.response_schema.model_validate(data)

                    logger.info(
                        "✅ Успешно распарсили %d сеансов",
                        len(validated.sessions),
                    )
                    return validated

                except json.JSONDecodeError as e:
                    last_error = e
                    logger.warning(
                        "❌ Попытка #%d: JSONDecodeError — %s", attempt, e
                    )
                    continue
                except ValidationError as e:
                    last_error = e
                    logger.warning(
                        "❌ Попытка #%d: ValidationError — %s", attempt, e
                    )
                    continue
                except Exception as e:
                    last_error = e
                    logger.warning(
                        "❌ Попытка #%d: %s — %s",
                        attempt,
                        type(e).__name__,
                        e,
                    )
                    continue

            logger.error(
                "❌ Все попытки OpenRouter исчерпаны (%d). "
                "Последняя ошибка: %s",
                self.max_retries,
                last_error,
            )
            return None

        except Exception as e:
            logger.exception("❌ Критическая ошибка OpenRouter: %s", e)
            return None