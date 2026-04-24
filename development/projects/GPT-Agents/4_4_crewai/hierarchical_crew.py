import os
from textwrap import dedent

import agentops
from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Инициализация AgentOps
agentops.init()

# Загрузка переменных окружения
load_dotenv()

# Настройка LLM
# Убедитесь, что OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL_NAME установлены в .env
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_base = os.getenv("OPENAI_API_BASE")
openai_model_name = os.getenv("OPENAI_MODEL_NAME")

if not all([openai_api_key, openai_api_base, openai_model_name]):
    print("Ошибка: Не все переменные окружения OpenAI установлены.")
    print("Пожалуйста, проверьте ваш .env файл в директории development/projects/GPT-Agents/4_4_crewai/")
    print(f"OPENAI_API_KEY: {'Установлен' if openai_api_key else 'НЕ УСТАНОВЛЕН'}")
    print(f"OPENAI_API_BASE: {'Установлен' if openai_api_base else 'НЕ УСТАНОВЛЕН'}")
    print(f"OPENAI_MODEL_NAME: {'Установлен' if openai_model_name else 'НЕ УСТАНОВЛЕН'}")
    exit()

llm = ChatOpenAI(
    api_key=openai_api_key, # Используем api_key вместо openai_api_key для ChatOpenAI
    base_url=openai_api_base,
    model=openai_model_name # Используем model вместо model_name для ChatOpenAI
)

print("LLM настроен успешно.")

# Создание менеджера команды
team_manager = Agent(
    role="Менеджер команды",
    goal="Координировать работу команды писателей и обеспечивать высокое качество контента на тему \"Искусственный интеллект в медицине\".",
    verbose=True,
    memory=True,
    backstory=dedent(
        """
        Вы опытный менеджер проектов с фокусом на создание технического контента. 
        Ваша задача - эффективно распределять задачи между исследователем и писателем, 
        контролировать качество их работы и обеспечивать своевременную сдачу материала.
        Вы стремитесь к тому, чтобы финальный продукт был точным, информативным и интересным для целевой аудитории.
        """
    ),
    allow_delegation=True,
    llm=llm
)

# Создание исследователя
researcher = Agent(
    role="Старший научный сотрудник",
    goal="Находить, анализировать и структурировать самую актуальную и достоверную информацию по теме \"Искусственный интеллект в медицине\".",
    verbose=True,
    memory=True,
    backstory=dedent(
        """
        Вы ведущий специалист по поиску и анализу информации в области высоких технологий и медицины. 
        Вы умеете работать с научными публикациями, отчетами исследовательских центров и новостными статьями. 
        Ваша цель - предоставить исчерпывающую и хорошо структурированную базу знаний для писателя.
        """
    ),
    allow_delegation=False,
    llm=llm
)

# Создание писателя
writer = Agent(
    role="Профессиональный технический писатель",
    goal="Создавать увлекательные, глубокие и технически точные статьи на тему \"Искусственный интеллект в медицине\" на основе предоставленных исследований.",
    verbose=True,
    memory=True,
    backstory=dedent(
        """
        Вы талантливый технический писатель, способный превращать сложные концепции в понятный и интересный текст. 
        Вы пишете для аудитории, которая может включать как специалистов, так и людей, только начинающих знакомство с темой. 
        Ваша задача - создать статью, которая будет одновременно информативной и легко читаемой.
        """
    ),
    allow_delegation=False,
    llm=llm
)

# Создание задачи для менеджера
management_task = Task(
    description=dedent(
        """
        Coordinate the team's efforts to create content about {topic}.
        Review and approve the research and writing tasks.
        Ensure the final content meets quality standards.
        """
    ),
    expected_output="A comprehensive content plan and quality review report.",
    agent=team_manager,
)

# Создание задачи для исследователя
research_task = Task(
    description=dedent(
        """
        Провести всестороннее и глубокое исследование на тему '{topic}'.
        Сфокусируйтесь на следующих аспектах:
        1.  Последние достижения (например, в диагностике, разработке лекарств, роботизированной хирургии).
        2.  Ключевые проблемы и вызовы (этические дилеммы, безопасность данных, стоимость внедрения).
        3.  Будущие перспективы и прогнозы развития на ближайшие 5-10 лет.
        4.  Конкретные примеры успешного применения ИИ в медицине.
        Ваша задача - собрать факты, статистику, цитаты экспертов и ссылки на авторитетные источники.
        """
    ),
    expected_output=dedent(
        """
        Детальный структурированный отчет по теме '{topic}', включающий:
        - Обзор последних достижений с примерами.
        - Анализ ключевых проблем и вызовов.
        - Прогноз будущих перспектив.
        - Список использованных авторитетных источников (не менее 5).
        - Ключевые статистические данные и цитаты.
        """
    ),
    agent=researcher,
)

# Создание задачи для писателя
writing_task = Task(
    description=dedent(
        """
        Написать высококачественную, увлекательную и информативную статью на тему '{topic}', 
        основываясь на предоставленных результатах исследования.
        Статья должна быть структурирована следующим образом:
        1.  Введение (актуальность темы, краткий обзор статьи).
        2.  Основная часть (несколько разделов, раскрывающих ключевые аспекты ИИ в медицине, 
            согласно исследованию: достижения, проблемы, перспективы).
        3.  Заключение (основные выводы, взгляд в будущее).
        Статья должна быть написана доступным языком, но с сохранением технической точности. 
        Используйте данные и примеры из отчета исследователя.
        """
    ),
    expected_output=dedent(
        """
        Готовая к публикации статья в формате markdown объемом не менее 800 слов по теме '{topic}'.
        Статья должна быть хорошо структурирована, содержать подзаголовки, списки (при необходимости) 
        и быть написана ясным и привлекательным языком. 
        Финальный результат сохранить в файл.
        """
    ),
    agent=writer,
    context=[research_task], # Эта задача начнется после research_task
    output_file="hierarchical_ai_in_medicine_article.md"
)

# Создание иерархической команды
crew = Crew(
    agents=[team_manager, researcher, writer],
    tasks=[management_task, research_task, writing_task],
    process=Process.hierarchical,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True,
    manager_llm=llm, # Явно указываем LLM для менеджера иерархического процесса
    verbose=2
)

# Запуск команды
result = crew.kickoff(inputs={"topic": "Искусственный интеллект в медицине"})
print("\nРезультат работы команды:")
print("------------------------")
print(result)

print("\n\n==========================================")
print("Завершение работы иерархической команды.")
print("Итоговый результат:")
print(result)
print(f"Статья должна быть сохранена в файле: hierarchical_ai_in_medicine_article.md в директории development/projects/GPT-Agents/4_4_crewai/")
print("==========================================\n") 