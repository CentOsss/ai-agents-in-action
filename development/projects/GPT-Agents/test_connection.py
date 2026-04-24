import os
from openai import OpenAI
from dotenv import load_dotenv

def test_connection():
    # Загрузка переменных окружения
    load_dotenv()
    
    # Инициализация клиента OpenAI
    client = OpenAI(
        base_url=os.getenv('OPENAI_API_BASE'),
        api_key=os.getenv('OPENAI_API_KEY')
    )
    
    try:
        # Тестовый запрос
        response = client.chat.completions.create(
            model=os.getenv('MODEL_NAME'),
            messages=[
                {"role": "system", "content": "Вы - полезный ассистент."},
                {"role": "user", "content": "Привет! Как дела?"}
            ]
        )
        print("Успешное подключение к API!")
        print("Ответ модели:", response.choices[0].message.content)
        return True
    except Exception as e:
        print("Ошибка при подключении к API:", str(e))
        return False

if __name__ == "__main__":
    test_connection() 