import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4o-mini"]
    }
)

llm_config = {"config_list": config_list, "cache_seed": 41} # cache_seed=None для отключения кэширования

# 1. Создание агента пользователя (UserProxyAgent)
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "working_task1", # Директория для сохранения кода и результатов
        "use_docker": False,  # Не использовать Docker в этом примере
    },
    system_message="""Вы пользовательский агент. Вы инициируете чат и выполняете код, предоставленный другими агентами."""
)

# 2. Создание агента-инженера (AssistantAgent)
engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message="""Инженер. Ты пишешь Python код для решения задач. 
    Убедись, что код написан правильно и соответствует заданию.
    После написания кода, добавь 'TERMINATE' в конце своего сообщения."""
)

# 3. Создание агента-критика (AssistantAgent)
critic = autogen.AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="""Критик. Ты проверяешь код, написанный Инженером. 
    Обрати внимание на возможные ошибки, стиль кода и соответствие заданию. 
    Предоставь конструктивную обратную связь Инженеру. 
    Если код хороший и выполняет задачу, скажи 'Код выглядит хорошо. TERMINATE'.
    Если есть замечания, укажи их и НЕ добавляй TERMINATE."""
)

# 4. Создание группового чата (GroupChat)
groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, critic],
    messages=[],
    max_round=10  # Максимальное количество раундов
)

# 5. Создание менеджера группового чата (GroupChatManager)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# 6. Инициация чата
task = "Напиши Python-скрипт, который выводит 'Hello, Group Chat!'"

print(f"Запускаем Задание 1 с задачей: {task}\n")

user_proxy.initiate_chat(
    manager,
    message=task
)

print("\nЗадание 1 завершено.")
print(f"Проверьте директорию 'development/projects/GPT-Agents/4_3_group_chat/working_task1' на наличие сгенерированного файла.") 