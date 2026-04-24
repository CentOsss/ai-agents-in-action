# Команда шутников с CrewAI

Этот проект демонстрирует создание команды агентов с помощью CrewAI для генерации и перевода шуток.

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
# или
.venv\Scripts\activate  # для Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` с необходимыми переменными окружения:
```
OPENAI_API_KEY=your_api_key_here
```

## Структура проекта

- `joke_crew.py` - основной файл с реализацией команды шутников
- `test_joke_crew.py` - тесты для проверки функциональности
- `example.py` - примеры использования команды
- `requirements.txt` - зависимости проекта

## Использование

### Базовое использование

```python
from joke_crew import run_joke_crew

# Генерация шуток на английском
result = run_joke_crew("AI engineer jokes")
print(result)

# Генерация шуток с переводом на другие языки
languages = ["Spanish", "French", "German"]
result = run_joke_crew("AI engineer jokes", languages)
print(result)
```

### Запуск тестов

```bash
python -m unittest test_joke_crew.py
```

### Запуск примеров

```bash
python example.py
```

## Компоненты команды

1. **Исследователь шуток** - ищет и анализирует шутки по заданной теме
2. **Писатель шуток** - создает новые шутки на основе исследования
3. **Переводчик** - переводит шутки на указанные языки
4. **Аналитик** - анализирует популярность тем в социальных сетях

## Особенности

- Последовательное выполнение задач
- Кэширование результатов
- Ограничение количества запросов
- Обработка ошибок
- Поддержка множества языков

## Требования

- Python 3.8+
- OpenAI API ключ
- CrewAI
- LangChain
- Другие зависимости из requirements.txt 