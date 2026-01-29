# import os
# from openai import OpenAI

# DEEPSEEK_API_KEY = "sk-d3948b56b4534e94b47259e8099b50a3"

# client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "Hello"},
#     ],
#     stream=False
# )

# print(response.choices[0].message.content)


# import os
# import base64
# from openai import OpenAI

# DEEPSEEK_API_KEY = "sk-d3948b56b4534e94b47259e8099b50a3"

# # Установите переменную окружения
# os.environ['DEEPSEEK_API_KEY'] = DEEPSEEK_API_KEY

# client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

# # Функция для кодирования изображения в base64
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

# # Путь к изображению
# image_path = r"C:\Users\User\Desktop\programmer\telegram-bot\src\screenshot.png"
# base64_image = encode_image(image_path)

# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {
#             "role": "user", 
#             "content": f"Проанализируй это изображение (base64): {base64_image[:100]}..."
#         },
#     ],
#     stream=False
# )

# print(response.choices[0].message.content)
import os
import base64
from openai import OpenAI

DEEPSEEK_API_KEY = "sk-d3948b56b4534e94b47259e8099b50a3"

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_vision(image_path, prompt):
    """Анализ изображения с использованием vision-модели"""
    
    base64_image = encode_image(image_path)
    
    try:
        # Попробуйте эти модели (проверьте актуальность в документации DeepSeek):
        vision_models = [
            "deepseek-vision",      # Основная vision модель
            # "deepseek-chat-vision", # Vision версия чат-модели
            # "deepseek-coder-vision" # Для кода на скриншотах
        ]
        
        # Попробуйте первую модель из списка
        response = client.chat.completions.create(
            model="deepseek-vision",  # ИЛИ другая vision-модель
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000,
            stream=False
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        # Если первая модель не работает, проверьте доступные модели
        return f"Ошибка: {str(e)}\n\nПроверьте доступные модели в документации DeepSeek."

# Пример использования
image_path = r"C:\Users\User\Desktop\programmer\telegram-bot\src\screenshot.png"
result = analyze_image_with_vision(image_path, "Что изображено на этой картинке?")
print(result)