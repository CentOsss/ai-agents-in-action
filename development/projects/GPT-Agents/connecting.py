import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Загружаем переменные окружения из файла .env
load_dotenv()

# 2. Получаем API-ключ и кастомный эндпоинт из переменных окружения
api_key = os.getenv('OPENAI_API_KEY')
api_base = os.getenv('OPENAI_API_BASE')

if not api_key:
    raise ValueError("No API key found. Please check your .env file.")

# 3. Создаём клиента OpenAI с использованием ключа и кастомного эндпоинта
client = OpenAI(api_key=api_key, base_url=api_base)

def ask_chatgpt(user_message):
    # 4. Отправляем запрос к модели GPT-4
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "Отвечай всегда в формате JSON, как в примере. Пример: {'topic': 'Python', 'summary': 'A versatile programming language.' }"},
            {"role": "system", "content": "Отвечай на русском языке."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
    )
    # 5. Возвращаем только текст ответа
    return response.choices[0].message.content

# Пример использования функции
if __name__ == "__main__":
    user = "Расскажи мне о JavaScript"
    response = ask_chatgpt(user)
    print(response) 