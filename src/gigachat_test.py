import json
from typing import List

from gigachat import GigaChat
from pydantic import ValidationError

from src.parsing_movie.malibu_cinema.schemas import (
    KinomaxSessionsShema,
)

# -------------------------------
# Конфигурация
# -------------------------------


IMAGE_PATH = r"C:/Users/User/Desktop/programmer/telegram-bot/src/screen_right.png"
MAX_RETRIES = 2


# -------------------------------
# Инициализация клиента
# -------------------------------

giga = GigaChat(
    credentials="MDE5YjUxMzMtOGQ4Ni03NmJhLWJjOWEtMjM3Y2I5Zjk4NTRmOmNjMzFlMTk3LTAxNzUtNDFhZC04NzdlLTYyNTY3NzM0NjI3MA==",
    verify_ssl_certs=False,
    model="GigaChat-Pro",
)

# -------------------------------
# Вспомогательные функции
# -------------------------------

def upload_image(path: str) -> str:
    """Загружает изображение и возвращает file_id"""
    with open(path, "rb") as f:
        uploaded = giga.upload_file(f)
    return uploaded.id_


def clean_json(content: str) -> dict:
    """Очищает markdown и парсит JSON"""
    cleaned = content.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)


def validate_sessions(content: str) -> KinomaxSessionsShema:
    """Парсит и валидирует ответ модели"""
    data = clean_json(content)
    return KinomaxSessionsShema.model_validate(data)


# -------------------------------
# Основная логика
# -------------------------------

def parse_cinema_schedule(image_path: str) -> KinomaxSessionsShema:
    file_id = upload_image(image_path)
    print(f"📎 Загружено изображение, file_id={file_id}")

    messages: List[dict] = []

    system_prompt = (
        "Ты профессиональный парсер афиш кинотеатров.\n"
        "Твоя задача — извлечь данные ТОЛЬКО с изображения.\n\n"
        "Правила:\n"
        "- не выдумывай данные\n"
        "- не добавляй комментарии\n"
        "- не используй markdown\n"
        "- верни СТРОГО валидный JSON\n"
    )

    user_prompt = """
Распарсь данные с изображения и верни JSON СТРОГО следующего формата:

{
  "sessions": [
    {
      "time": "16:25",
      "price": 330,
      "format": "2D"
    }
  ]
}
"""

    # system
    messages.append(
        {
            "role": "system",
            "content": system_prompt,
        }
    )

    # user + image
    messages.append(
        {
            "role": "user",
            "content": user_prompt,
            "attachments": [file_id],
        }
    )

    last_error: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 2):
        print(f"🤖 Запрос к модели (попытка {attempt})")

        response = giga.chat(
            {
                "messages": messages,
                "temperature": 0.1,
            }
        )

        assistant_content = response.choices[0].message.content
        messages.append(
            {
                "role": "assistant",
                "content": assistant_content,
            }
        )

        try:
            result = validate_sessions(assistant_content)
            print("✅ Успешно распаршено")
            return result

        except (ValidationError, json.JSONDecodeError) as e:
            print("❌ Ошибка валидации")
            last_error = e

            messages.append(
                {
                    "role": "user",
                    "content": (
                        "Ты допустил ошибку.\n\n"
                        f"Ошибка валидации:\n{e}\n\n"
                        "Исправь ответ и верни ТОЛЬКО корректный JSON "
                        "строго по схеме."
                    ),
                }
            )

    raise RuntimeError(
        f"Не удалось получить корректный ответ от модели. "
        f"Последняя ошибка: {last_error}"
    )


# -------------------------------
# Точка входа
# -------------------------------

if __name__ == "__main__":
    result = parse_cinema_schedule(IMAGE_PATH)
    print("\n🎬 Итоговый результат:")
    print(result)
