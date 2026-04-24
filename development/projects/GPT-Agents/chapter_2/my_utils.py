#!/usr/bin/env python3
"""
Мои собственные утилиты для работы с AI
Этот модуль можно импортировать в других скриптах
"""

from prompt_utils import prompt_llm
import json
import time
from datetime import datetime

def smart_ask(question, context=None, max_tokens=500, temperature=0.7):
    """
    Умная функция для задавания вопросов с дополнительными возможностями
    
    Args:
        question (str): Вопрос для AI
        context (str, optional): Дополнительный контекст
        max_tokens (int): Максимальное количество токенов в ответе
        temperature (float): Температура для генерации (0.0-1.0)
    
    Returns:
        str: Ответ от AI
    """
    # Формируем сообщения
    messages = []
    
    if context:
        messages.append({"role": "system", "content": context})
    
    messages.append({"role": "user", "content": question})
    
    # Используем готовую функцию, но с нашими параметрами
    response = prompt_llm(messages)
    
    return response

def batch_questions(questions_list, context=None, delay=1):
    """
    Задает несколько вопросов подряд с задержкой
    
    Args:
        questions_list (list): Список вопросов
        context (str, optional): Общий контекст для всех вопросов
        delay (int): Задержка между запросами в секундах
    
    Returns:
        list: Список ответов
    """
    results = []
    
    for i, question in enumerate(questions_list, 1):
        print(f"Обрабатываю вопрос {i}/{len(questions_list)}...")
        
        try:
            answer = smart_ask(question, context)
            results.append({
                "question": question,
                "answer": answer,
                "timestamp": datetime.now().isoformat()
            })
            
            # Задержка между запросами
            if i < len(questions_list):
                time.sleep(delay)
                
        except Exception as e:
            results.append({
                "question": question,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    return results

def analyze_text(text, analysis_type="sentiment"):
    """
    Анализирует текст с помощью AI
    
    Args:
        text (str): Текст для анализа
        analysis_type (str): Тип анализа (sentiment, keywords, summary)
    
    Returns:
        dict: Результат анализа
    """
    prompts = {
        "sentiment": f"""
        Проанализируй эмоциональную окраску текста и верни результат в JSON:
        
        Текст: "{text}"
        
        Формат ответа:
        {{
            "настроение": "позитивное/негативное/нейтральное",
            "уверенность": "высокая/средняя/низкая",
            "эмоции": ["радость", "грусть", "злость", "удивление", "страх"]
        }}
        """,
        
        "keywords": f"""
        Извлеки ключевые слова из текста и верни в JSON:
        
        Текст: "{text}"
        
        Формат ответа:
        {{
            "ключевые_слова": ["слово1", "слово2", "слово3"],
            "темы": ["тема1", "тема2"],
            "важность": "высокая/средняя/низкая"
        }}
        """,
        
        "summary": f"""
        Создай краткое резюме текста и верни в JSON:
        
        Текст: "{text}"
        
        Формат ответа:
        {{
            "краткое_резюме": "резюме в 1-2 предложениях",
            "главные_идеи": ["идея1", "идея2"],
            "длина_оригинала": количество_слов
        }}
        """
    }
    
    if analysis_type not in prompts:
        return {"error": f"Неизвестный тип анализа: {analysis_type}"}
    
    try:
        response = smart_ask(prompts[analysis_type])
        
        # Пытаемся извлечь JSON
        if "```json" in response:
            json_part = response.split("```json")[1].split("```")[0].strip()
        elif "{" in response and "}" in response:
            start = response.find("{")
            end = response.rfind("}") + 1
            json_part = response[start:end]
        else:
            json_part = response
        
        return json.loads(json_part)
        
    except json.JSONDecodeError:
        return {"error": "Не удалось распарсить JSON", "raw_response": response}
    except Exception as e:
        return {"error": str(e)}

def create_conversation_bot(personality, name="AI-Бот"):
    """
    Создает бота для разговора с заданной личностью
    
    Args:
        personality (str): Описание личности бота
        name (str): Имя бота
    
    Returns:
        function: Функция для общения с ботом
    """
    conversation_history = [
        {"role": "system", "content": f"Ты {name}. {personality}"}
    ]
    
    def chat(message):
        nonlocal conversation_history
        
        # Добавляем сообщение пользователя
        conversation_history.append({"role": "user", "content": message})
        
        # Получаем ответ
        response = prompt_llm(conversation_history)
        
        # Добавляем ответ в историю
        conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def get_history():
        return conversation_history.copy()
    
    def clear_history():
        nonlocal conversation_history
        conversation_history = [conversation_history[0]]  # Сохраняем только system message
    
    # Возвращаем объект с методами
    chat.get_history = get_history
    chat.clear_history = clear_history
    chat.name = name
    
    return chat

def save_conversation_to_file(conversation, filename):
    """
    Сохраняет разговор в файл
    
    Args:
        conversation (list): История разговора
        filename (str): Имя файла
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "conversation": conversation
            }, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False

def load_conversation_from_file(filename):
    """
    Загружает разговор из файла
    
    Args:
        filename (str): Имя файла
    
    Returns:
        list: История разговора
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("conversation", [])
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return []

# Пример использования модуля
if __name__ == "__main__":
    print("🛠️ ТЕСТИРОВАНИЕ СОБСТВЕННЫХ УТИЛИТ")
    print("=" * 50)
    
    # Тест 1: Умный вопрос
    print("=== Тест 1: Умный вопрос ===")
    answer = smart_ask(
        "Что такое Python?",
        context="Ты преподаватель программирования для начинающих."
    )
    print(f"Ответ: {answer[:200]}...")
    
    # Тест 2: Анализ текста
    print("\n=== Тест 2: Анализ текста ===")
    test_text = "Я очень рад, что изучаю программирование! Это так интересно и увлекательно!"
    sentiment = analyze_text(test_text, "sentiment")
    print(f"Анализ настроения: {sentiment}")
    
    # Тест 3: Создание бота
    print("\n=== Тест 3: Создание бота ===")
    teacher_bot = create_conversation_bot(
        "Ты добрый и терпеливый учитель программирования. Объясняешь сложные вещи простыми словами.",
        "Учитель-Бот"
    )
    
    response = teacher_bot("Привет! Расскажи о переменных в Python")
    print(f"Бот: {response[:200]}...")
    
    print("\n✅ Все тесты завершены!")
    print("Теперь вы можете импортировать эти функции в других скриптах!") 