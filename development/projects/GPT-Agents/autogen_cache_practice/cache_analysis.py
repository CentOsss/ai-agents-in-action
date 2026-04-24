import autogen
from autogen import Cache
import os
import time
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
    max_consecutive_auto_reply=3,
    code_execution_config={"use_docker": False}  # Отключаем использование Docker
)

def run_dialog_with_cache(cache_seed):
    task = f"Обсудим тему кэширования в AutoGen. Это диалог с cache_seed={cache_seed}"
    
    with Cache.disk(cache_seed=cache_seed) as cache:
        print(f"\nЗапуск диалога с cache_seed={cache_seed}")
        res = user_proxy.initiate_chat(
            recipient=assistant,
            message=task,
            max_turns=3,
            summary_method="last_msg",
            cache=cache
        )
    
    # Анализ размера кэша
    cache_dir = ".cache"
    if os.path.exists(cache_dir):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(cache_dir):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        print(f"Размер кэша для cache_seed={cache_seed}: {total_size/1024:.2f} KB")

# Запуск диалогов с разными значениями cache_seed
for seed in [42, 123, 456]:
    run_dialog_with_cache(seed)
    time.sleep(1)  # Пауза между диалогами 