import autogen
from autogen import Cache
import time
import os
import shutil
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Конфигурация агентов
config_list = [
    {
        "model": "gpt-4",
        "api_key": os.getenv("OPENAI_API_KEY"),
        "base_url": os.getenv("OPENAI_API_BASE")
    }
]

# Создание агентов
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list}
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
    code_execution_config={"use_docker": False}  # Отключаем использование Docker
)

def clean_cache():
    if os.path.exists(".cache"):
        shutil.rmtree(".cache")

def run_without_cache():
    print("\nЗапуск без кэширования...")
    start_time = time.time()
    
    task = "Объясни концепцию кэширования в AutoGen"
    res = user_proxy.initiate_chat(
        recipient=assistant,
        message=task,
        max_turns=2,
        summary_method="last_msg"
    )
    
    end_time = time.time()
    return end_time - start_time

def run_with_cache():
    print("\nЗапуск с кэшированием...")
    start_time = time.time()
    
    task = "Объясни концепцию кэширования в AutoGen"
    with Cache.disk(cache_seed=42) as cache:
        res = user_proxy.initiate_chat(
            recipient=assistant,
            message=task,
            max_turns=2,
            summary_method="last_msg",
            cache=cache
        )
    
    end_time = time.time()
    return end_time - start_time

# Очистка кэша перед началом
clean_cache()

# Запуск без кэширования
time_without_cache = run_without_cache()
print(f"Время выполнения без кэширования: {time_without_cache:.2f} секунд")

# Запуск с кэшированием
time_with_cache = run_with_cache()
print(f"Время выполнения с кэшированием: {time_with_cache:.2f} секунд")

# Повторный запуск с кэшированием
time_with_cache_second = run_with_cache()
print(f"Время выполнения с кэшированием (второй запуск): {time_with_cache_second:.2f} секунд")

print("\nАнализ результатов:")
print(f"Ускорение при первом запуске с кэшем: {time_without_cache/time_with_cache:.2f}x")
print(f"Ускорение при втором запуске с кэшем: {time_without_cache/time_with_cache_second:.2f}x") 