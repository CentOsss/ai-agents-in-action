import autogen
import time

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4o-mini"]
    }
)

# Для Задания 3 мы будем экспериментировать с cache_seed и max_round
# Попробуем с конкретным cache_seed для воспроизводимости и возможно меньшим max_round
llm_config = {"config_list": config_list, "cache_seed": 43} 

# 1. Агент пользователя
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "working_task3", 
        "use_docker": False,
    },
    system_message="""Агент пользователя. Инициируй чат. Код будет выполнен тобой.""" # Немного сокращенное сообщение
)

# 2. Агент-инженер
engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message="""Инженер. Ты пишешь Python-скрипты. 
    Старайся писать эффективный и чистый код. 
    Учитывай критику. Завершай сообщение с 'TERMINATE', когда код готов.""" # Сокращенное сообщение
)

# 3. Агент-критик
critic = autogen.AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="""Критик. Проверяй код Инженера на корректность и соответствие задаче. 
    Давай краткую, но ясную обратную связь. 
    Если все хорошо, подтверди и напиши 'TERMINATE'. Иначе, укажи что исправить.""" # Сокращенное сообщение
)

# 4. Групповой чат
groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, critic],
    messages=[],
    max_round=8  # Уменьшенное количество раундов для эксперимента
)

# 5. Менеджер группового чата
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# 6. Инициация чата (та же задача, что и в Задании 2 для сравнения влияния параметров)
task = """Напиши Python-скрипт, который:
1. Запрашивает у пользователя его имя.
2. Выводит приветственное сообщение с этим именем (например, 'Привет, [имя]!').
3. Код должен включать обработку ошибок на случай пустого ввода имени. В этом случае, скрипт должен вывести 'Имя не может быть пустым.'"""

print(f"Запускаем Задание 3 с задачей: {task}")
print(f"Параметры: max_round={groupchat.max_round}, cache_seed={llm_config['cache_seed']}\n")

start_time = time.time()

user_proxy.initiate_chat(
    manager,
    message=task
)

end_time = time.time()
execution_time = end_time - start_time

print("\nЗадание 3 завершено.")
print(f"Время выполнения: {execution_time:.2f} секунд.")
print(f"Проверьте директорию 'development/projects/GPT-Agents/4_3_group_chat/working_task3' на наличие сгенерированного файла.")
print("Обратите внимание, как cache_seed и max_round могли повлиять на диалог и время выполнения.") 