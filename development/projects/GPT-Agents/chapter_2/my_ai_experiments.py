#!/usr/bin/env python3
"""
Мои эксперименты с AI - изучение готовых функций
Этот файл демонстрирует, как использовать функции из других модулей
"""

# Импортируем функции из готовых скриптов
from prompt_utils import prompt_llm
import json
import os

def test_basic_functionality():
    """Тестирует базовую функциональность API"""
    print("=== ТЕСТ 1: Базовая функциональность ===")
    
    # Простой запрос
    messages = [{"role": "user", "content": "Привет! Как дела?"}]
    response = prompt_llm(messages)
    print(f"Вопрос: Привет! Как дела?")
    print(f"Ответ: {response}")
    print("-" * 50)

def test_different_temperatures():
    """Тестирует влияние температуры на ответы"""
    print("=== ТЕСТ 2: Влияние температуры ===")
    
    question = "Напиши короткое стихотворение о коте"
    
    # Тестируем разные температуры
    temperatures = [0.1, 0.7, 1.0]
    
    for temp in temperatures:
        print(f"\n--- Температура: {temp} ---")
        # Создаем модифицированную функцию с разной температурой
        from openai import OpenAI
        
        client = OpenAI(
            base_url="https://api.proxyapi.ru/openai/v1",
            api_key="sk-Cpt0I1HB2rNekF9PNwxLOdFv0ewHdqp4"
        )
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}],
            temperature=temp
        )
        
        print(f"Ответ: {response.choices[0].message.content}")
    
    print("-" * 50)

def test_personas():
    """Тестирует использование различных персон"""
    print("=== ТЕСТ 3: Различные персоны ===")
    
    question = "Объясни, что такое программирование"
    
    personas = [
        "Ты опытный преподаватель программирования. Объясняй простым языком.",
        "Ты веселый робот, который любит шутки. Отвечай с юмором.",
        "Ты строгий профессор. Давай академические ответы.",
    ]
    
    for i, persona in enumerate(personas, 1):
        print(f"\n--- Персона {i}: {persona[:30]}... ---")
        messages = [
            {"role": "system", "content": persona},
            {"role": "user", "content": question}
        ]
        response = prompt_llm(messages)
        print(f"Ответ: {response[:200]}...")
    
    print("-" * 50)

def test_conversation_context():
    """Тестирует поддержание контекста разговора"""
    print("=== ТЕСТ 4: Контекст разговора ===")
    
    # Создаем историю разговора
    conversation = [
        {"role": "system", "content": "Ты дружелюбный помощник с хорошей памятью."},
        {"role": "user", "content": "Меня зовут Алексей, и я изучаю программирование."},
        {"role": "assistant", "content": "Приятно познакомиться, Алексей! Программирование - отличный выбор. Чем могу помочь?"},
        {"role": "user", "content": "Как меня зовут и что я изучаю?"}
    ]
    
    response = prompt_llm(conversation)
    print("История разговора:")
    for msg in conversation[:-1]:
        print(f"{msg['role']}: {msg['content']}")
    
    print(f"\nПоследний вопрос: {conversation[-1]['content']}")
    print(f"Ответ: {response}")
    print("-" * 50)

def test_structured_output():
    """Тестирует получение структурированного вывода"""
    print("=== ТЕСТ 5: Структурированный вывод ===")
    
    prompt = """
    Проанализируй следующий текст и верни результат в JSON формате:
    
    Текст: "Сегодня отличная погода! Солнце светит, птицы поют. Я очень рад."
    
    Формат ответа:
    {
        "настроение": "позитивное/негативное/нейтральное",
        "ключевые_слова": ["слово1", "слово2", "слово3"],
        "краткое_резюме": "краткое описание"
    }
    """
    
    messages = [{"role": "user", "content": prompt}]
    response = prompt_llm(messages)
    print("Запрос на структурированный вывод:")
    print(response)
    print("-" * 50)

def interactive_chat():
    """Интерактивный чат с пользователем"""
    print("=== ИНТЕРАКТИВНЫЙ ЧАТ ===")
    print("Введите 'выход' для завершения чата")
    
    # История разговора
    conversation = [
        {"role": "system", "content": "Ты дружелюбный AI-помощник, который помогает изучать программирование и AI."}
    ]
    
    while True:
        user_input = input("\nВы: ")
        
        if user_input.lower() in ['выход', 'exit', 'quit']:
            print("До свидания!")
            break
        
        # Добавляем сообщение пользователя
        conversation.append({"role": "user", "content": user_input})
        
        try:
            # Получаем ответ
            response = prompt_llm(conversation)
            print(f"AI: {response}")
            
            # Добавляем ответ в историю
            conversation.append({"role": "assistant", "content": response})
            
        except Exception as e:
            print(f"Ошибка: {e}")

def main():
    """Главная функция - запускает все тесты"""
    print("🚀 НАЧИНАЕМ ЭКСПЕРИМЕНТЫ С AI!")
    print("=" * 60)
    
    try:
        # Запускаем все тесты
        test_basic_functionality()
        test_different_temperatures()
        test_personas()
        test_conversation_context()
        test_structured_output()
        
        # Предлагаем интерактивный чат
        choice = input("\nХотите попробовать интерактивный чат? (да/нет): ")
        if choice.lower() in ['да', 'yes', 'y']:
            interactive_chat()
            
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        print("Проверьте настройки API ключа и интернет-соединение.")

if __name__ == "__main__":
    main() 