import os
from openai import OpenAI
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Инициализация клиента OpenAI
client = OpenAI(
    base_url=os.getenv('OPENAI_API_BASE'),
    api_key=os.getenv('OPENAI_API_KEY')
)

def chat_with_history(messages, temperature=0.7):
    """
    Функция для общения с моделью с учетом истории сообщений
    
    Args:
        messages (list): Список сообщений в формате [{"role": "...", "content": "..."}]
        temperature (float): Параметр вариативности ответов (0.0 - 1.0)
    
    Returns:
        tuple: (текст ответа, объект ответа)
    """
    response = client.chat.completions.create(
        model=os.getenv('MODEL_NAME'),
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content, response

def test_temperature():
    """Тестирование разных значений temperature"""
    messages = [
        {"role": "system", "content": "Вы - полезный ассистент."},
        {"role": "user", "content": "Расскажи короткую историю."}
    ]
    
    print("\nТестирование разных значений temperature:")
    for temp in [0.0, 0.7, 1.0]:
        print(f"\nTemperature = {temp}:")
        response_text, _ = chat_with_history(messages, temperature=temp)
        print(response_text)

def main():
    # Начальный диалог
    messages = [
        {"role": "system", "content": "Вы - полезный ассистент."},
        {"role": "user", "content": "Какая столица Франции?"}
    ]
    
    # Получаем первый ответ
    response_text, response_obj = chat_with_history(messages)
    print("Ответ 1:", response_text)
    
    # Добавляем ответ ассистента в историю
    messages.append({"role": "assistant", "content": response_text})
    
    # Задаем следующий вопрос
    messages.append({"role": "user", "content": "Расскажи интересный факт о Париже."})
    
    # Получаем второй ответ
    response_text, response_obj = chat_with_history(messages)
    print("\nОтвет 2:", response_text)
    
    # Выводим статистику использования токенов
    print("\nСтатистика использования токенов:")
    print(f"Запрос: {response_obj.usage.prompt_tokens}")
    print(f"Ответ: {response_obj.usage.completion_tokens}")
    print(f"Всего: {response_obj.usage.total_tokens}")
    
    # Тестируем разные значения temperature
    test_temperature()

if __name__ == "__main__":
    main() 