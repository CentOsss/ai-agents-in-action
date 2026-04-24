#!/usr/bin/env python3
"""
Пример использования собственных утилит
Демонстрирует, как импортировать и использовать функции из my_utils.py
"""

# Импортируем наши собственные функции!
from my_utils import (
    smart_ask, 
    batch_questions, 
    analyze_text, 
    create_conversation_bot,
    save_conversation_to_file,
    load_conversation_from_file
)

def demo_smart_ask():
    """Демонстрация умного вопроса"""
    print("=== ДЕМО: Умный вопрос ===")
    
    # Обычный вопрос
    answer1 = smart_ask("Что такое искусственный интеллект?")
    print(f"Обычный вопрос: {answer1[:150]}...")
    
    # Вопрос с контекстом
    answer2 = smart_ask(
        "Что такое искусственный интеллект?",
        context="Ты объясняешь 10-летнему ребенку. Используй простые слова и примеры."
    )
    print(f"С контекстом: {answer2[:150]}...")
    print("-" * 50)

def demo_batch_questions():
    """Демонстрация пакетных вопросов"""
    print("=== ДЕМО: Пакетные вопросы ===")
    
    questions = [
        "Что такое переменная в программировании?",
        "Что такое функция в программировании?",
        "Что такое цикл в программировании?"
    ]
    
    context = "Ты преподаватель программирования. Отвечай кратко и понятно."
    
    results = batch_questions(questions, context, delay=0.5)
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Вопрос {i} ---")
        print(f"Q: {result['question']}")
        if 'answer' in result:
            print(f"A: {result['answer'][:100]}...")
        else:
            print(f"Ошибка: {result['error']}")
    
    print("-" * 50)

def demo_text_analysis():
    """Демонстрация анализа текста"""
    print("=== ДЕМО: Анализ текста ===")
    
    texts = [
        "Я в восторге от изучения программирования! Это так увлекательно и интересно!",
        "Программирование - это сложно, но я стараюсь понять основы.",
        "Сегодня изучал Python. Создал свою первую программу для расчета площади круга."
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"\n--- Текст {i} ---")
        print(f"Исходный текст: {text}")
        
        # Анализ настроения
        sentiment = analyze_text(text, "sentiment")
        print(f"Настроение: {sentiment}")
        
        # Анализ ключевых слов
        keywords = analyze_text(text, "keywords")
        print(f"Ключевые слова: {keywords}")
    
    print("-" * 50)

def demo_conversation_bot():
    """Демонстрация разговорного бота"""
    print("=== ДЕМО: Разговорный бот ===")
    
    # Создаем бота-помощника по программированию
    coding_bot = create_conversation_bot(
        "Ты дружелюбный помощник по программированию. Отвечаешь кратко и по делу.",
        "КодБот"
    )
    
    # Серия вопросов
    questions = [
        "Привет! Как дела?",
        "Расскажи про Python",
        "Как создать список в Python?",
        "А как добавить элемент в список?",
        "Спасибо за помощь!"
    ]
    
    print(f"Разговор с {coding_bot.name}:")
    
    for question in questions:
        response = coding_bot(question)
        print(f"\n👤 Пользователь: {question}")
        print(f"🤖 {coding_bot.name}: {response}")
    
    # Сохраняем разговор
    history = coding_bot.get_history()
    save_conversation_to_file(history, "conversation_example.json")
    print(f"\n💾 Разговор сохранен в файл conversation_example.json")
    
    print("-" * 50)

def demo_conversation_loading():
    """Демонстрация загрузки разговора"""
    print("=== ДЕМО: Загрузка разговора ===")
    
    # Загружаем сохраненный разговор
    loaded_conversation = load_conversation_from_file("conversation_example.json")
    
    if loaded_conversation:
        print("Загруженный разговор:")
        for msg in loaded_conversation:
            role = msg['role']
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            print(f"{role}: {content}")
    else:
        print("Не удалось загрузить разговор")
    
    print("-" * 50)

def interactive_demo():
    """Интерактивная демонстрация"""
    print("=== ИНТЕРАКТИВНАЯ ДЕМОНСТРАЦИЯ ===")
    print("Выберите, что хотите попробовать:")
    print("1. Умный вопрос")
    print("2. Анализ текста")
    print("3. Чат с ботом")
    print("4. Выход")
    
    while True:
        choice = input("\nВведите номер (1-4): ").strip()
        
        if choice == "1":
            question = input("Введите ваш вопрос: ")
            context = input("Введите контекст (или нажмите Enter): ")
            
            if context.strip():
                answer = smart_ask(question, context)
            else:
                answer = smart_ask(question)
            
            print(f"\nОтвет: {answer}")
        
        elif choice == "2":
            text = input("Введите текст для анализа: ")
            analysis_type = input("Тип анализа (sentiment/keywords/summary): ").strip()
            
            if analysis_type not in ["sentiment", "keywords", "summary"]:
                analysis_type = "sentiment"
            
            result = analyze_text(text, analysis_type)
            print(f"\nРезультат анализа: {result}")
        
        elif choice == "3":
            personality = input("Опишите личность бота: ")
            name = input("Имя бота: ")
            
            bot = create_conversation_bot(personality, name)
            
            print(f"\nЧат с {name} начат! Введите 'выход' для завершения.")
            
            while True:
                user_msg = input(f"\nВы: ")
                if user_msg.lower() in ['выход', 'exit']:
                    break
                
                response = bot(user_msg)
                print(f"{name}: {response}")
        
        elif choice == "4":
            print("До свидания!")
            break
        
        else:
            print("Неверный выбор. Попробуйте еще раз.")

def main():
    """Главная функция"""
    print("🎯 ДЕМОНСТРАЦИЯ СОБСТВЕННЫХ УТИЛИТ")
    print("=" * 60)
    
    # Запускаем все демонстрации
    demo_smart_ask()
    demo_batch_questions()
    demo_text_analysis()
    demo_conversation_bot()
    demo_conversation_loading()
    
    # Предлагаем интерактивный режим
    choice = input("\nХотите попробовать интерактивный режим? (да/нет): ")
    if choice.lower() in ['да', 'yes', 'y']:
        interactive_demo()
    
    print("\n🎉 Демонстрация завершена!")
    print("\n📝 Что вы узнали:")
    print("✅ Как создавать собственные модули")
    print("✅ Как импортировать функции из других файлов")
    print("✅ Как использовать готовые функции в своем коде")
    print("✅ Как создавать переиспользуемые утилиты")

if __name__ == "__main__":
    main() 