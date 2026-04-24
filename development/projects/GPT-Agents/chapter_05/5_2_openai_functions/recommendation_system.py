import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Инициализация клиента OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

def recommend(topic, rating="good"):
    """
    Функция для предоставления рекомендаций по различным темам.
    
    Args:
        topic (str): Тема для рекомендации (например, "movie", "book", "game")
        rating (str): Рейтинг рекомендации (good, bad, terrible)
    
    Returns:
        str: JSON-строка с рекомендацией, содержащая:
            - topic: тема рекомендации
            - recommendation: название рекомендуемого предмета
            - rating: рейтинг рекомендации
            - description: краткое описание
    """
    if "movie" in topic.lower():
        return json.dumps({
            "topic": "movie",
            "recommendation": "The Matrix",
            "rating": rating,
            "description": "Классический научно-фантастический фильм о виртуальной реальности"
        })
    elif "book" in topic.lower():
        return json.dumps({
            "topic": "book",
            "recommendation": "1984",
            "rating": rating,
            "description": "Антиутопический роман Джорджа Оруэлла"
        })
    elif "game" in topic.lower():
        return json.dumps({
            "topic": "game",
            "recommendation": "The Witcher 3",
            "rating": rating,
            "description": "Эпическая RPG с открытым миром"
        })
    else:
        return json.dumps({
            "topic": topic,
            "recommendation": "unknown",
            "rating": rating,
            "description": "Нет рекомендаций для данной темы"
        })

def run_conversation(user_message):
    """
    Функция для выполнения диалога с LLM и обработки рекомендаций.
    
    Args:
        user_message (str): Сообщение пользователя, содержащее запрос на рекомендацию
    
    Returns:
        str: Ответ системы в формате JSON-строки с рекомендацией
    
    Процесс работы:
    1. Определение структуры функции для LLM
    2. Отправка запроса к API OpenAI
    3. Обработка ответа и вызов соответствующей функции
    4. Возврат результата пользователю
    """
    # Определение структуры функции для LLM
    # Это описание того, как LLM должен использовать функцию recommend
    tools = [{
        "type": "function",
        "function": {
            "name": "recommend",
            "description": "Provide a recommendation for any topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to get a recommendation for."
                    },
                    "rating": {
                        "type": "string",
                        "description": "The rating that was given.",
                        "enum": ["good", "bad", "terrible"]  # Допустимые значения рейтинга
                    }
                },
                "required": ["topic"]  # Обязательный параметр
            }
        }
    }]
    
    # Создание запроса к API OpenAI
    # Используем модель gpt-3.5-turbo-1106, которая поддерживает функции
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}],
        tools=tools,  # Передаем описание функции
        tool_choice="auto"  # Позволяем модели самостоятельно решать, использовать ли функцию
    )

    # Обработка ответа от API
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # Если модель решила использовать функцию
    if tool_calls:
        # Словарь доступных функций
        available_functions = {
            "recommend": recommend
        }
        
        # Обработка каждого вызова функции
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            # Парсинг аргументов функции из JSON
            function_args = json.loads(tool_call.function.arguments)
            
            # Вызов функции с полученными аргументами
            function_response = function_to_call(
                topic=function_args.get("topic"),
                rating=function_args.get("rating")
            )

            # Сохранение информации о вызове функции и её результате
            response_message.tool_calls = tool_calls
            response_message.content = function_response

    return response_message.content

def main():
    """
    Основная функция для тестирования системы рекомендаций.
    
    Процесс тестирования:
    1. Определение набора тестовых сообщений
    2. Последовательный запуск каждого теста
    3. Вывод результатов в консоль
    """
    # Набор тестовых сообщений для проверки различных сценариев
    test_messages = [
        "Can you recommend me a good movie?",  # Запрос фильма
        "What book should I read?",            # Запрос книги
        "Can you suggest a terrible game?",    # Запрос игры с плохим рейтингом
        "What's a good restaurant in the city?" # Запрос без соответствующей категории
    ]
    
    print("Тестирование системы рекомендаций:")
    print("-" * 50)
    
    # Запуск тестов и вывод результатов
    for message in test_messages:
        print(f"\nЗапрос: {message}")
        response = run_conversation(message)
        print(f"Ответ: {response}")
        print("-" * 50)

if __name__ == "__main__":
    main() 