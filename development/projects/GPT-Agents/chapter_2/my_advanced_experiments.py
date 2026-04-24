#!/usr/bin/env python3
"""
Продвинутые эксперименты с AI - использование готовых модулей
Демонстрирует импорт и использование функций из разных файлов
"""

# Импортируем функции из разных готовых скриптов
from prompt_utils import prompt_llm
import json
import os

# Попробуем импортировать функции из других файлов
try:
    # Если есть функции в других скриптах, импортируем их
    import sys
    sys.path.append('.')  # Добавляем текущую директорию в путь
except ImportError as e:
    print(f"Некоторые модули недоступны: {e}")

class AIAssistant:
    """Класс для создания AI-помощника с различными возможностями"""
    
    def __init__(self, personality="Ты дружелюбный и полезный AI-помощник."):
        self.personality = personality
        self.conversation_history = [
            {"role": "system", "content": personality}
        ]
    
    def ask(self, question):
        """Задать вопрос AI"""
        # Добавляем вопрос в историю
        self.conversation_history.append({"role": "user", "content": question})
        
        # Получаем ответ, используя готовую функцию
        response = prompt_llm(self.conversation_history)
        
        # Добавляем ответ в историю
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def clear_history(self):
        """Очистить историю разговора"""
        self.conversation_history = [
            {"role": "system", "content": self.personality}
        ]
    
    def get_history_length(self):
        """Получить количество сообщений в истории"""
        return len(self.conversation_history)

def create_coding_assistant():
    """Создает специализированного помощника по программированию"""
    coding_personality = """
    Ты опытный программист и наставник с 10-летним стажем.
    Твои принципы:
    1. Всегда объясняй код подробно
    2. Приводи практические примеры
    3. Указывай на потенциальные ошибки
    4. Предлагай улучшения
    5. Отвечай на русском языке
    """
    return AIAssistant(coding_personality)

def create_translator():
    """Создает помощника-переводчика"""
    translator_personality = """
    Ты профессиональный переводчик.
    Переводи тексты точно и естественно.
    Сохраняй стиль и контекст оригинала.
    """
    return AIAssistant(translator_personality)

def test_specialized_assistants():
    """Тестирует специализированных помощников"""
    print("=== ТЕСТ: Специализированные помощники ===")
    
    # Создаем помощника по программированию
    coding_assistant = create_coding_assistant()
    
    print("--- Помощник по программированию ---")
    code_question = "Как создать список в Python и добавить в него элементы?"
    code_answer = coding_assistant.ask(code_question)
    print(f"Вопрос: {code_question}")
    print(f"Ответ: {code_answer[:300]}...")
    
    # Создаем переводчика
    translator = create_translator()
    
    print("\n--- Переводчик ---")
    translate_question = "Переведи на английский: 'Привет, как дела? Надеюсь, у тебя все хорошо!'"
    translate_answer = translator.ask(translate_question)
    print(f"Вопрос: {translate_question}")
    print(f"Ответ: {translate_answer}")
    
    print("-" * 50)

def test_conversation_flow():
    """Тестирует поток разговора с сохранением контекста"""
    print("=== ТЕСТ: Поток разговора ===")
    
    assistant = AIAssistant("Ты помощник, который помнит все детали разговора.")
    
    # Серия связанных вопросов
    questions = [
        "Меня зовут Иван, и я работаю программистом в компании TechCorp.",
        "Какие языки программирования популярны сейчас?",
        "Как ты думаешь, какой язык лучше изучить мне для карьерного роста?",
        "Напомни, как меня зовут и где я работаю?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n--- Вопрос {i} ---")
        print(f"Пользователь: {question}")
        answer = assistant.ask(question)
        print(f"AI: {answer}")
    
    print(f"\nВсего сообщений в истории: {assistant.get_history_length()}")
    print("-" * 50)

def test_json_processing():
    """Тестирует обработку JSON данных"""
    print("=== ТЕСТ: Обработка JSON ===")
    
    # Создаем помощника для работы с данными
    data_assistant = AIAssistant("""
    Ты специалист по обработке данных.
    Всегда возвращай результат в валидном JSON формате.
    Будь точным и структурированным.
    """)
    
    request = """
    Проанализируй эту информацию о сотруднике и верни в JSON:
    
    "Иван Петров, 28 лет, программист, зарплата 150000 рублей, опыт 5 лет, знает Python, JavaScript, SQL"
    
    Формат:
    {
        "имя": "...",
        "возраст": число,
        "профессия": "...",
        "зарплата": число,
        "опыт_лет": число,
        "навыки": ["...", "...", "..."]
    }
    """
    
    response = data_assistant.ask(request)
    print("Запрос на обработку данных:")
    print(response)
    
    # Попробуем распарсить JSON
    try:
        # Извлекаем JSON из ответа (может быть в блоке кода)
        if "```json" in response:
            json_part = response.split("```json")[1].split("```")[0].strip()
        elif "{" in response and "}" in response:
            start = response.find("{")
            end = response.rfind("}") + 1
            json_part = response[start:end]
        else:
            json_part = response
            
        parsed_data = json.loads(json_part)
        print("\n✅ JSON успешно распарсен:")
        for key, value in parsed_data.items():
            print(f"  {key}: {value}")
    except json.JSONDecodeError:
        print("❌ Не удалось распарсить JSON")
    
    print("-" * 50)

def test_prompt_variations():
    """Тестирует различные вариации промптов"""
    print("=== ТЕСТ: Вариации промптов ===")
    
    base_question = "Объясни, что такое машинное обучение"
    
    # Разные способы формулировки
    prompts = [
        # Простой промпт
        [{"role": "user", "content": base_question}],
        
        # С контекстом
        [
            {"role": "system", "content": "Ты преподаватель для студентов первого курса."},
            {"role": "user", "content": base_question}
        ],
        
        # С примерами (few-shot)
        [
            {"role": "user", "content": f"""
            Вопрос: Что такое программирование?
            Ответ: Программирование - это процесс создания инструкций для компьютера.
            
            Вопрос: {base_question}
            Ответ:"""}
        ],
        
        # Структурированный промпт
        [
            {"role": "user", "content": f"""
            Задача: {base_question}
            
            Требования:
            1. Объяснение простыми словами
            2. Один практический пример
            3. Не более 100 слов
            
            Ответ:"""}
        ]
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n--- Вариация {i} ---")
        response = prompt_llm(prompt)
        print(f"Ответ: {response[:200]}...")
    
    print("-" * 50)

def main():
    """Главная функция"""
    print("🔬 ПРОДВИНУТЫЕ ЭКСПЕРИМЕНТЫ С AI!")
    print("=" * 60)
    
    try:
        test_specialized_assistants()
        test_conversation_flow()
        test_json_processing()
        test_prompt_variations()
        
        print("\n🎉 Все тесты завершены успешно!")
        print("\n📚 Что вы изучили:")
        print("- Создание классов для работы с AI")
        print("- Специализированные помощники")
        print("- Поддержание контекста разговора")
        print("- Обработка структурированных данных")
        print("- Различные техники промптинга")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main() 