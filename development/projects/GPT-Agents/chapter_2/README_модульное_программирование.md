# 📚 Модульное программирование с AI

## 🎯 Что такое модульное программирование?

**Модульное программирование** - это подход к разработке, при котором программа разбивается на отдельные модули (файлы), каждый из которых отвечает за определенную функциональность.

## ✅ Преимущества модульного подхода

### 1. **Переиспользование кода**
```python
# Вместо копирования кода в каждый файл
from prompt_utils import prompt_llm  # Используем готовую функцию

# Теперь можем использовать в любом количестве файлов
response = prompt_llm(messages)
```

### 2. **Разделение ответственности**
- `prompt_utils.py` - работа с API
- `my_utils.py` - наши собственные утилиты
- `my_experiments.py` - эксперименты и тесты

### 3. **Легкость тестирования**
```python
# Можем тестировать отдельные функции
from my_utils import analyze_text

result = analyze_text("Тестовый текст", "sentiment")
assert result["настроение"] == "позитивное"
```

### 4. **Читаемость и поддержка**
- Код организован логически
- Легко найти нужную функцию
- Проще вносить изменения

## 🔧 Как создать собственный модуль

### Шаг 1: Создайте файл с функциями
```python
# my_utils.py
def smart_ask(question, context=None):
    """Умная функция для вопросов"""
    # Ваш код здесь
    return response
```

### Шаг 2: Импортируйте в другом файле
```python
# main.py
from my_utils import smart_ask

# Используйте функцию
answer = smart_ask("Что такое Python?")
```

## 📁 Структура проекта

```
chapter_2/
├── .env                              # Конфигурация API
├── prompt_utils.py                   # Готовые утилиты для API
├── my_utils.py                       # Ваши собственные утилиты
├── my_ai_experiments.py              # Базовые эксперименты
├── my_advanced_experiments.py        # Продвинутые эксперименты
├── example_using_my_utils.py         # Примеры использования
└── README_модульное_программирование.md
```

## 🎨 Примеры использования

### Базовый импорт
```python
from prompt_utils import prompt_llm
from my_utils import smart_ask, analyze_text
```

### Импорт с переименованием
```python
from my_utils import smart_ask as ask_ai
from my_utils import create_conversation_bot as create_bot
```

### Импорт всего модуля
```python
import my_utils

# Использование через точку
result = my_utils.smart_ask("Вопрос")
```

## 🚀 Созданные нами утилиты

### 1. `smart_ask()` - Умные вопросы
```python
# Простой вопрос
answer = smart_ask("Что такое Python?")

# Вопрос с контекстом
answer = smart_ask(
    "Что такое Python?",
    context="Объясни ребенку 10 лет"
)
```

### 2. `analyze_text()` - Анализ текста
```python
# Анализ настроения
sentiment = analyze_text("Я рад!", "sentiment")

# Извлечение ключевых слов
keywords = analyze_text("Изучаю Python", "keywords")

# Создание резюме
summary = analyze_text("Длинный текст...", "summary")
```

### 3. `create_conversation_bot()` - Создание ботов
```python
# Создаем бота
bot = create_conversation_bot(
    "Ты дружелюбный помощник",
    "Помощник"
)

# Общаемся
response = bot("Привет!")
```

### 4. `batch_questions()` - Пакетные вопросы
```python
questions = [
    "Что такое переменная?",
    "Что такое функция?",
    "Что такое класс?"
]

results = batch_questions(questions, context="Объясни просто")
```

## 💡 Лучшие практики

### 1. **Документирование функций**
```python
def smart_ask(question, context=None):
    """
    Умная функция для задавания вопросов
    
    Args:
        question (str): Вопрос для AI
        context (str, optional): Контекст
    
    Returns:
        str: Ответ от AI
    """
```

### 2. **Обработка ошибок**
```python
try:
    response = prompt_llm(messages)
    return response
except Exception as e:
    return f"Ошибка: {e}"
```

### 3. **Валидация входных данных**
```python
def analyze_text(text, analysis_type="sentiment"):
    if analysis_type not in ["sentiment", "keywords", "summary"]:
        return {"error": "Неизвестный тип анализа"}
```

### 4. **Конфигурация через переменные**
```python
# В начале файла
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 500

def smart_ask(question, temperature=DEFAULT_TEMPERATURE):
    # Используем конфигурацию
```

## 🔍 Отладка и тестирование

### Запуск модуля напрямую
```python
# В конце файла my_utils.py
if __name__ == "__main__":
    # Код для тестирования
    print("Тестирование модуля...")
    test_function()
```

### Проверка импорта
```python
# Проверяем, что функция доступна
from my_utils import smart_ask
print(smart_ask.__doc__)  # Показывает документацию
```

## 📊 Сравнение подходов

| Подход | Преимущества | Недостатки |
|--------|-------------|------------|
| Один большой файл | Просто начать | Сложно поддерживать |
| Модульный подход | Организованно, переиспользуемо | Нужно планировать структуру |
| Копирование кода | Быстро | Дублирование, ошибки |

## 🎯 Заключение

Модульное программирование - это **стандартная практика** в разработке:

✅ **Да, это нормально** - использовать готовые функции  
✅ **Да, это правильно** - создавать собственные модули  
✅ **Да, это эффективно** - переиспользовать код  

### Следующие шаги:
1. Изучите готовые модули в проекте
2. Создавайте собственные утилиты
3. Комбинируйте разные подходы
4. Документируйте свой код

**Помните**: Хороший программист не тот, кто пишет все с нуля, а тот, кто умеет эффективно использовать существующие решения!

---

## 🔧 Команды для запуска

```bash
# Активация виртуального окружения
source ~/.venv/bin/activate

# Переход в директорию проекта
cd development/projects/GPT-Agents/gn0me-try/chapter_2

# Запуск различных скриптов
python my_ai_experiments.py          # Базовые эксперименты
python my_advanced_experiments.py    # Продвинутые эксперименты
python my_utils.py                   # Тестирование утилит
python example_using_my_utils.py     # Примеры использования
``` 