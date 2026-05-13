### Новый гигачат парсер для HTML расписаний кинотеатров Kinomax.
### Теперь он принимает HTML-контент, а не изображение, и возвращает строго валидный JSON с сеансами.
### Добавлено логирование использования токенов и улучшена обработка ошибок с несколькими попытками.

import json
import logging
from typing import List, Type

from gigachat import GigaChat
from gigachat.exceptions import ResponseError
from pydantic import ValidationError, BaseModel

logger = logging.getLogger(__name__)


class GigaChatScheduleParser:
    def __init__(
        self,
        credentials: str,
        response_schema: Type[BaseModel],
        model: str = "GigaChat",
        max_retries: int = 3,
        temperature: float = 0.2,
        verify_ssl: bool = False,
    ):
        self.giga = GigaChat(
            credentials=credentials,
            verify_ssl_certs=verify_ssl,
            model=model,
        )
        self.response_schema = response_schema
        self.max_retries = max_retries
        self.temperature = temperature

        self.system_prompt = (
            "Ты эксперт по парсингу HTML-расписаний сеансов кинотеатров Kinomax.\n"
            "Извлекай ТОЛЬКО данные о сеансах.\n"
            "Верни строго JSON без пояснений.\n"
            "{\n"
            '  "sessions": [\n'
            '    {"time": "16:25", "price": 330, "format": "2D"}\n'
            "  ]\n"
            "}\n"
            "Если сеансов нет — верни пустой массив."
        )

        self.user_prompt_template = (
            "HTML расписания:\n\n{html_content}\n\n"
            "Извлеки сеансы."
        )

    # ==========================================================
    # UTILS
    # ==========================================================

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """Грубая оценка токенов"""
        return len(text) // 4

    # ==========================================================
    # MAIN
    # ==========================================================

    def parse_cinema_schedule(self, html_content: str):
        try:
            # 🔥 Ограничение HTML
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

            # 🔥 БАЗОВЫЕ messages (НЕ МЕНЯЮТСЯ)
            base_messages: List[dict] = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            # 📊 лог размера входа
            input_size = sum(len(m["content"]) for m in base_messages)
            logger.info(
                "📊 INPUT SIZE: %d chars (~%d tokens)",
                input_size,
                self._estimate_tokens("".join(m["content"] for m in base_messages)),
            )

            last_error = None

            for attempt in range(1, self.max_retries + 2):
                logger.info("🔁 Попытка #%d", attempt)

                # ❗ ВАЖНО: каждый раз создаём новый messages
                messages = base_messages.copy()

                # 👉 только короткая инструкция, без накопления истории
                if attempt > 1:
                    messages.append({
                        "role": "user",
                        "content": "Исправь JSON. Верни только валидный JSON."
                    })

                try:
                    response = self.giga.chat(
                        {
                            "messages": messages,
                            "temperature": self.temperature,
                        }
                    )

                    # 🔥 полный dump ответа (чтобы понять структуру)
                    try:
                        logger.debug("FULL RESPONSE: %s", response.model_dump())
                    except Exception:
                        logger.debug("RAW RESPONSE: %s", response)

                    # 📊 usage (если есть)
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
                        "Ответ GigaChat (первые 150 символов): %s",
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

                except (json.JSONDecodeError, ValidationError) as e:
                    logger.warning(
                        "❌ Попытка %d — ошибка JSON: %s",
                        attempt,
                        e,
                    )
                    last_error = e

                except ResponseError as e:
                    logger.error(
                        "❌ API ошибка (попытка %d): %s",
                        attempt,
                        e,
                    )
                    last_error = e

            raise RuntimeError(
                f"Не удалось получить валидный JSON после {self.max_retries+1} попыток. "
                f"Последняя ошибка: {last_error}"
            )

        except Exception:
            logger.exception("💥 Критическая ошибка парсинга HTML → GigaChat")
            raise

#-------------------------------------------------------------------------------------------------
# import json
# import logging
# from typing import List, Type
# from gigachat import GigaChat
# from pydantic import ValidationError, BaseModel
# from gigachat.exceptions import ResponseError

# logger = logging.getLogger(__name__)

# class GigaChatScheduleParser:
#     def __init__(
#         self,
#         credentials: str,
#         response_schema: Type[BaseModel],
#         model: str = "GigaChat",
#         max_retries: int = 3,
#         temperature: float = 0.2,              # чуть выше, т.к. Lite менее точный
#         verify_ssl: bool = False,
#     ):
#         self.giga = GigaChat(
#             credentials=credentials,
#             verify_ssl_certs=verify_ssl,
#             model=model,
#         )
#         self.response_schema = response_schema
#         self.max_retries = max_retries
#         self.temperature = temperature

#         self.system_prompt = (
#             "Ты эксперт по парсингу HTML-расписаний сеансов кинотеатров Kinomax.\n"
#             "Извлекай ТОЛЬКО данные о сеансах из предоставленного HTML.\n"
#             "Игнорируй рекламу, футер, навигацию, отзывы, похожие фильмы.\n"
#             "Верни СТРОГО валидный JSON без markdown, комментариев и лишнего текста.\n"
#             "Формат строго такой:\n"
#             "{\n" 
#             '  "sessions": [\n'
#             '    {"time": "16:25", "price": 330, "format": "2D"},\n'
#             '    {"time": "19:10", "price": 380, "format": "3D"}\n'
#             "  ]\n"
#             "}\n"
#             "Если сеансов нет — верни пустой массив."
#         )

#         self.user_prompt_template = (
#             "Вот HTML-код блока с расписанием сеансов на один день:\n\n"
#             "{html_content}\n\n"
#             "Извлеки все сеансы фильма в указанном JSON-формате."
#         )

#     def parse_cinema_schedule(self, html_content: str):
#         """
#         Теперь принимает HTML-строку вместо пути к картинке
#         """
#         try:
#             # Ограничиваем размер HTML контента, чтобы не превышать лимит GigaChat (130048)
#             # Берём только первые 50000 символов, обрезая лишнее
#             max_html_length = 50000
#             if len(html_content) > max_html_length:
#                 logger.warning(
#                     f"HTML контент слишком большой ({len(html_content)} > {max_html_length}), обрезаем"
#                 )
#                 html_content = html_content[:max_html_length]
            
#             user_prompt = self.user_prompt_template.format(html_content=html_content)

#             messages: List[dict] = [
#                 {"role": "system", "content": self.system_prompt},
#                 {"role": "user", "content": user_prompt},
#             ]

#             last_error = None
#             for attempt in range(1, self.max_retries + 2):
#                 try:
#                     response = self.giga.chat(
#                         {
#                             "messages": messages,
#                             "temperature": self.temperature,
#                         }
#                     )
#                     content = response.choices[0].message.content.strip()
                    
#                     # 📊 Логирование использования токенов
#                     if hasattr(response, 'usage') and response.usage:
#                         usage = response.usage
#                         logger.info(
#                             "🔥 Использование токенов | "
#                             "Input: %s | Output: %s | Total: %s",
#                             getattr(usage, 'input_tokens', '?'),
#                             getattr(usage, 'output_tokens', '?'),
#                             getattr(usage, 'total_tokens', '?'),
#                         )
                    
#                     logger.debug("Ответ GigaChat (первые 150 символов): %s", content[:150])

#                     # чистим на случай ```json
#                     if content.startswith("```"):
#                         content = content.split("```json", 1)[-1].split("```", 1)[0].strip()

#                     data = json.loads(content)
#                     validated = self.response_schema.model_validate(data)
#                     logger.info("Успешно распарсили %d сеансов", len(validated.sessions))
#                     return validated
#                 except (json.JSONDecodeError, ValidationError) as e:
#                     logger.warning("Попытка %d — ошибка валидации: %s", attempt, e)
#                     last_error = e
#                     # добавляем обратную связь для self-correction
#                     messages.append({"role": "assistant", "content": content})
#                     messages.append({"role": "user", "content": "JSON некорректный. Исправь и верни только чистый JSON."})

#                 except ResponseError as e:
#                     logger.error("API ошибка (попытка %d): %s", attempt, e)
#                     last_error = e

#             raise RuntimeError(f"Не удалось получить валидный JSON после {self.max_retries+1} попыток. Последняя ошибка: {last_error}")

#         except Exception as e:
#             logger.exception("Критическая ошибка парсинга HTML → GigaChat")
#             raise

