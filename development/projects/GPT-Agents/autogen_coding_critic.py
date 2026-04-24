from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
import os

# --- НАСТРОЙКИ --- #
# Путь к файлу конфигурации OpenAI (должен быть в той же директории, что и скрипт)
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "OAI_CONFIG_LIST")
# Рабочая директория для сохранения сгенерированного кода и логов
WORK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "working_critic")
# Задача для инженера
TASK = """Write a Python script for a simple command-line calculator that can perform addition, subtraction, multiplication, and division. 
The calculator should take user input for two numbers and an operator. 
Ensure the code is well-commented and handles potential errors like division by zero or invalid input. 
Save the code to a file named 'calculator.py' in the working directory."""

# Создаем рабочую директорию, если она не существует
if not os.path.exists(WORK_DIR):
    os.makedirs(WORK_DIR)
    print(f"[INFO] Создана рабочая директория: {WORK_DIR}")

# --- ЗАГРУЗКА КОНФИГУРАЦИИ LLM --- #
print(f"[INFO] Загрузка конфигурации LLM из файла: {CONFIG_FILE_PATH}...")
if not os.path.exists(CONFIG_FILE_PATH):
    print(f"[ERROR] Файл конфигурации {CONFIG_FILE_PATH} не найден.")
    print("Пожалуйста, создайте его на основе OAI_CONFIG_LIST.example и заполните своими данными.")
    exit()

try:
    config_list = config_list_from_json(env_or_file=CONFIG_FILE_PATH)
    print("[INFO] Конфигурация LLM успешно загружена.")
except ValueError as e:
    print(f"[ERROR] Ошибка при загрузке OAI_CONFIG_LIST: {e}")
    print(f"Убедитесь, что файл {CONFIG_FILE_PATH} существует и имеет корректный JSON формат.")
    exit()
except Exception as e:
    print(f"[ERROR] Непредвиденная ошибка при загрузке конфигурации: {e}")
    exit()

# --- ОПРЕДЕЛЕНИЕ АГЕНТОВ --- #

# 1. Прокси-агент пользователя (UserProxyAgent)
print("[INFO] Создание прокси-агента пользователя (user_proxy)...")
user_proxy = UserProxyAgent(
    name="User_Proxy", # Явное имя для лучшей читаемости логов
    code_execution_config={
        "work_dir": WORK_DIR,
        "use_docker": False,  # Для простоты установим False. Рекомендуется True для безопасности.
        "last_n_messages": 1, # Критически важно для критика: берем только последнее сообщение с кодом
    },
    human_input_mode="NEVER", # Изменено на NEVER для полностью автоматического прогона примера. Можно вернуть "ALWAYS" для интерактива.
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    system_message="A human user. Interact with the Engineer to get the code, then trigger the Reviewer for code critique. Terminate the conversation once the review is complete or if the Engineer provides a TERMINATE message."
)
print("[INFO] Прокси-агент пользователя (user_proxy) создан.")

# 2. Агент-Инженер (AssistantAgent)
print("[INFO] Создание агента-инженера (Engineer)...")
engineer = AssistantAgent(
    name="Engineer",
    llm_config={"config_list": config_list, "cache_seed": 42, "temperature": 0.7},
    system_message='''You are a professional Python engineer, known for your expertise in software development. 
Your use your skills to create software applications and tools that are both functional and efficient. 
Your preference is to write clean, well-structured code that is easy to read and maintain. 
When asked to write a script, ensure it is complete and runnable. Provide the full Python code block.
If the task includes saving the file (e.g. "Save the code to a file named 'calculator.py'"), include the necessary Python code within your script to save itself to the specified filename in the current working directory using standard Python file operations.
After providing the complete script that includes the self-saving mechanism, clearly state that the script is complete, includes saving, and is ready. Do NOT use the word TERMINATE in your response containing the code. Just provide the code and a concluding remark.'''
)
print("[INFO] Агент-инженер (Engineer) создан.")

# 3. Агент-Критик (AssistantAgent)
print("[INFO] Создание агента-критика (Reviewer)...")
critic = AssistantAgent(
    name="Reviewer",
    llm_config={"config_list": config_list, "cache_seed": 43, "temperature": 0.8},
    system_message='''You are a code reviewer, known for your thoroughness and commitment to standards. 
Your task is to scrutinize code content for any harmful or substandard elements. 
You ensure that the code is secure, efficient, and adheres to Python best practices. 
Identify any issues or areas for improvement in the code and output them as a numbered list in markdown format. 
If the code is excellent and has no issues, state that explicitly.
If you believe the code is ready after your review, you can optionally include the word PERFECT_CODE at the end of your review.'''
)
print("[INFO] Агент-критик (Reviewer) создан.")

# --- ФУНКЦИЯ ДЛЯ ОБРАБОТКИ КОДА КРИТИКОМ --- #
def review_code_for_critic(recipient, messages, sender, config_passed_to_callback):
    print(f"\n[CALLBACK] review_code_for_critic: Вызвана для {recipient.name} от {sender.name}.")
    
    # Ищем последнее сообщение от инженера (роль assistant, имя Engineer)
    engineer_code_message_content = None
    for msg in reversed(messages):
        if msg.get("role") == "assistant" and msg.get("name") == "Engineer":
            engineer_code_message_content = msg.get("content", "").strip()
            break

    if engineer_code_message_content:
        # Извлекаем код из markdown-блока, если он есть
        code_blocks = []
        in_code_block = False
        current_block = []
        for line in engineer_code_message_content.splitlines():
            if line.strip().startswith("```python"):
                in_code_block = True
                current_block = []
                continue
            elif line.strip() == "```" and in_code_block:
                in_code_block = False
                code_blocks.append("\n".join(current_block))
                current_block = []
                continue
            if in_code_block:
                current_block.append(line)
        if not code_blocks and len(engineer_code_message_content.splitlines()) > 1:
            code_to_review = engineer_code_message_content
        elif code_blocks:
            code_to_review = "\n".join(code_blocks)
        else:
            code_to_review = None
        if code_to_review:
            print(f"[CALLBACK] Извлечённый код для ревью (первые 300 символов):\n{code_to_review[:300]}...")
            review_prompt = (
                f"Please review the following Python code. Focus on clarity, efficiency, security, and adherence to Python best practices. "
                f"Provide your feedback as a numbered list in markdown format. If the code is excellent, please state so and optionally include PERFECT_CODE at the end.\n\n"
                f"```python\n{code_to_review}\n```"
            )
            return review_prompt
        else:
            print("[CALLBACK] Не удалось извлечь блок кода Python из сообщения инженера.")
            return "TERMINATE"
    else:
        print("[CALLBACK] Код от инженера не найден для ревью (сообщение было пустым или TERMINATE).")
        return "TERMINATE"

# --- РЕГИСТРАЦИЯ ВЛОЖЕННОГО ЧАТА --- #
print("[INFO] Регистрация вложенного чата для критика...")
user_proxy.register_nested_chats(
    [
        {
            "recipient": critic,
            "message": review_code_for_critic, 
            "summary_method": "last_msg",
            "max_turns": 1, 
            "config": {"engineer_agent_ref": engineer} # <--- ДОБАВЛЕНО: передаем инстанс инженера
        }
    ],
    trigger=engineer,  
)
print("[INFO] Вложенный чат зарегистрирован.")

# --- ИНИЦИАЦИЯ ОСНОВНОГО ЧАТА --- #
print(f"\n[INFO] Запускаем основной чат с задачей:\n{TASK}")

print("[DEBUG] Перед запуском initiate_chat")
res = user_proxy.initiate_chat(
    recipient=engineer,
    message=TASK,
    max_turns=3,  # User_Proxy -> Engineer, Engineer -> User_Proxy (код) -> Critic -> User_Proxy (ревью), User_Proxy -> (выполняет, завершает)
    summary_method="last_msg"
)
print("[DEBUG] После initiate_chat")

# --- ВЫВОД РЕЗУЛЬТАТОВ --- #
print("\n--- ИТОГОВЫЙ РЕЗУЛЬТАТ ЧАТА ---")
if res.summary:
    print(f"[SUMMARY] Краткий итог: {res.summary}")

if res.cost:
    print(f"[COST] Затраты на выполнение: {res.cost}")

print("\n--- ПОЛНАЯ ИСТОРИЯ ЧАТА ---")
if res.chat_history:
    for i, msg in enumerate(res.chat_history):
        print(f"\nСообщение {i+1}: От "
              f"'{msg.get('name', msg.get('role'))}' к "
              f"'{res.chat_history[i+1].get('name', res.chat_history[i+1].get('role')) if i+1 < len(res.chat_history) else 'N/A'}'")
        print(f"Роль: {msg.get('role')}")
        content = msg.get("content")
        print(f"Содержимое:\n{content}")
        print("-" * 30)
else:
    print("[INFO] История чата пуста.")

print("\n[INFO] Работа скрипта autogen_coding_critic.py завершена.")
print("[DEBUG] Конец скрипта autogen_coding_critic.py") 