import os
from openai import OpenAI
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
api_base = os.getenv('OPENAI_API_BASE')

if not api_key:
    raise ValueError("No API key found. Please check your .env file.")

# Создаём клиента OpenAI с кастомным эндпоинтом
client = OpenAI(api_key=api_key, base_url=api_base)

def chat_with_history():
    # История сообщений для chat completion
    messages = [
        {"role": "system", "content": "Ты — полезный ассистент."},
        {"role": "user", "content": "Привет!"},
        {"role": "assistant", "content": "Здравствуйте! Чем могу помочь?"},
        {"role": "user", "content": "Что такое чат-комплишн?"}
    ]
    # Отправляем запрос к модели
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        temperature=0.7,
    )
    # Выводим ответ ассистента
    print("Ответ ассистента:", response.choices[0].message.content)

if __name__ == "__main__":
    chat_with_history() 