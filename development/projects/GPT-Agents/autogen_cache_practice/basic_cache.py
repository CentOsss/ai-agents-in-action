import autogen
from autogen import Cache
import os
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
    code_execution_config={"use_docker": False}
)

# Задача для агентов
task = "Давайте обсудим преимущества кэширования в AutoGen. Начни с основных концепций."

# Запуск диалога с кэшированием
with Cache.disk(cache_seed=42) as cache:
    print("Начинаем диалог с кэшированием...")
    res = user_proxy.initiate_chat(
        recipient=assistant,
        message=task,
        max_turns=2,
        summary_method="last_msg",
        cache=cache
    )
    print("\nДиалог завершен. Проверьте папку .cache в текущей директории.") 