import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4o-mini"]
    }
)

llm_config = {"config_list": config_list, "cache_seed": 42} # Используем другой cache_seed или None

# 1. Агент пользователя
user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "working_task2",
        "use_docker": False,
    },
    system_message="""Агент пользователя. Инициируй чат с задачей. Выполняй код, если это необходимо."""
)

# 2. Агент-инженер
engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message="""Инженер. Твоя задача - написать Python-скрипт согласно требованиям. 
    Сначала напиши начальную версию кода. 
    Затем, учти обратную связь от Критика для улучшения кода. 
    Когда код будет готов и протестирован (мысленно), добавь 'TERMINATE' в конце своего сообщения."""
)

# 3. Агент-критик
critic = autogen.AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="""Критик. Твоя задача - проверять код, написанный Инженером. 
    Убедись, что код решает поставленную задачу, корректен и включает обработку ошибок, если это указано в задаче. 
    Предоставляй четкую и конструктивную обратную связь Инженеру. 
    Если код соответствует всем требованиям, напиши 'Код соответствует требованиям. TERMINATE'. 
    Если есть замечания, четко их изложи и НЕ добавляй TERMINATE."""
)

# 4. Групповой чат
groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, critic],
    messages=[],
    max_round=12  # Немного больше раундов для возможной итерации
)

# 5. Менеджер группового чата
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# 6. Инициация чата с более сложной задачей
task = """Напиши Python-скрипт, который:
1. Запрашивает у пользователя его имя.
2. Выводит приветственное сообщение с этим именем (например, 'Привет, [имя]!').
3. Код должен включать обработку ошибок на случай пустого ввода имени (например, если пользователь просто нажимает Enter). В этом случае, скрипт должен вывести сообщение типа 'Имя не может быть пустым.'"""

print(f"Запускаем Задание 2 с задачей: {task}\n")

user_proxy.initiate_chat(
    manager,
    message=task
)

print("\nЗадание 2 завершено.")
print(f"Проверьте директорию 'development/projects/GPT-Agents/4_3_group_chat/working_task2' на наличие сгенерированного файла.") 