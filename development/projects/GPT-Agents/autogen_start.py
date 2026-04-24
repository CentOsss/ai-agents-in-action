from autogen import ConversableAgent, UserProxyAgent, config_list_from_json
import logging # Опционально для более детального вывода
import os

# Опционально: Настройка логирования для просмотра деталей работы AutoGen
# logging.basicConfig(level=logging.INFO)

# Определяем путь к OAI_CONFIG_LIST относительно текущего скрипта
# Это делает скрипт более переносимым, если OAI_CONFIG_LIST лежит рядом.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_PATH = os.path.join(SCRIPT_DIR, "OAI_CONFIG_LIST")

WORK_DIR = os.path.join(SCRIPT_DIR, "coding_work_dir")

# Создаем рабочую директорию, если она не существует
if not os.path.exists(WORK_DIR):
    os.makedirs(WORK_DIR)
    print(f"Создана рабочая директория: {WORK_DIR}")

try:
    # 1. Загрузка конфигурации LLM из файла OAI_CONFIG_LIST
    print(f"Загрузка конфигурации LLM из файла: {CONFIG_FILE_PATH}...")
    if not os.path.exists(CONFIG_FILE_PATH):
        print(f"ОШИБКА: Файл конфигурации {CONFIG_FILE_PATH} не найден.")
        print("Пожалуйста, создайте его на основе OAI_CONFIG_LIST.example и заполните своими данными.")
        exit()
        
    config_list = config_list_from_json(
        env_or_file=CONFIG_FILE_PATH
    )
    print("Конфигурация LLM успешно загружена.")

except ValueError as e:
    print(f"Ошибка при загрузке OAI_CONFIG_LIST: {e}")
    print(f"Убедитесь, что файл {CONFIG_FILE_PATH} существует и имеет корректный JSON формат.")
    exit()
except Exception as e:
    print(f"Непредвиденная ошибка при загрузке конфигурации: {e}")
    exit()

# 2. Создание агента-ассистента (ConversableAgent)
print("Создание агента-ассистента...")
assistant = ConversableAgent(
    name="assistant",
    llm_config={"config_list": config_list, "cache_seed": 42} # cache_seed для воспроизводимости
)
print("Агент-ассистент создан.")

# 3. Создание прокси-агента пользователя (UserProxyAgent)
print("Создание прокси-агента пользователя...")
user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config={
        "work_dir": WORK_DIR,
        "use_docker": False, # Для простоты начнем без Docker
    },
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE")
)
print("Прокси-агент пользователя создан.")

# 4. Инициация чата
# Пример задачи из книги (Листинг 4.6)
# task_message = "write a solution for fizz buzz in one line?"

# Пример задачи из практического задания этого курса
task_message = "Write a python script to calculate the nth Fibonacci number and save it to a file named fibonacci.py in the 'coding_work_dir' directory. Then run the script for n=10 and tell me the result."

print(f"\nИнициация чата с задачей: {task_message}")

user_proxy.initiate_chat(
    assistant,
    message=task_message
)

print("\nЧат завершен.") 