import os
from openai import OpenAI
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Инициализация клиента OpenAI
client = OpenAI()

def ask_gpt4(question, system_prompt="You are a helpful assistant.", temperature=0.7):
    """
    Функция для отправки запроса к GPT-4
    
    Args:
        question (str): Вопрос пользователя
        system_prompt (str): Системный промпт для настройки поведения модели
        temperature (float): Параметр вариативности ответа (0-1)
    
    Returns:
        str: Ответ модели
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=temperature,
            max_tokens=1000,
            presence_penalty=0.6,
            frequency_penalty=0.0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

def maintain_conversation(initial_question, max_turns=3):
    """
    Функция для поддержания диалога с GPT-4
    
    Args:
        initial_question (str): Начальный вопрос
        max_turns (int): Максимальное количество обменов репликами
    
    Returns:
        list: История диалога
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": initial_question}
    ]
    
    conversation_history = []
    
    for _ in range(max_turns):
        try:
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=messages,
                temperature=0.7
            )
            
            assistant_message = response.choices[0].message.content
            messages.append({"role": "assistant", "content": assistant_message})
            conversation_history.append(("assistant", assistant_message))
            
            # Здесь можно добавить логику для генерации следующего вопроса
            # или получения его от пользователя
            
        except Exception as e:
            conversation_history.append(("error", str(e)))
            break
    
    return conversation_history

if __name__ == "__main__":
    # Пример использования базового запроса
    question = "What is the capital of France?"
    answer = ask_gpt4(question)
    print(f"Вопрос: {question}")
    print(f"Ответ: {answer}")
    
    # Пример использования диалога
    print("\nНачинаем диалог:")
    conversation = maintain_conversation("Tell me about artificial intelligence.")
    for role, content in conversation:
        print(f"{role.upper()}: {content}") 