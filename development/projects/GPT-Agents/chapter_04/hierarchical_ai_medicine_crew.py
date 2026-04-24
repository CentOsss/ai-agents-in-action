import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from textwrap import dedent

# Загрузка переменных окружения из .env файла
# Убедитесь, что .env файл находится в той же директории, что и скрипт, 
# или укажите полный путь к .env файлу в load_dotenv()
load_dotenv() 

# Настройка LLM
# OPENAI_API_KEY, OPENAI_API_BASE, OPENAI_MODEL_NAME должны быть установлены в .env
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_base = os.getenv("OPENAI_API_BASE")
openai_model_name = os.getenv("OPENAI_MODEL_NAME")

if not all([openai_api_key, openai_api_base, openai_model_name]):
    print("Ошибка: Не все переменные окружения OpenAI установлены.")
    print("Пожалуйста, проверьте ваш .env файл в директории development/projects/GPT-Agents/chapter_04/")
    print(f"OPENAI_API_KEY: {'Установлен' if openai_api_key else 'НЕ УСТАНОВЛЕН'}")
    print(f"OPENAI_API_BASE: {'Установлен' if openai_api_base else 'НЕ УСТАНОВЛЕН'}")
    print(f"OPENAI_MODEL_NAME: {'Установлен' if openai_model_name else 'НЕ УСТАНОВЛЕН'}")
    exit()

llm = ChatOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    model=openai_model_name 
)

print("LLM настроен успешно.")

# 1. Создание агентов
print("Создание агентов...")
team_manager = Agent(
    role='Менеджер команды',
    goal='Координировать работу команды писателей и обеспечивать высокое качество контента на тему "Искусственный интеллект в медицине".',
    backstory=dedent("""\
        Вы опытный менеджер проектов с фокусом на создание технического контента. 
        Ваша задача - эффективно распределять задачи между исследователем и писателем, 
        контролировать качество их работы и обеспечивать своевременную сдачу материала.
        Вы стремитесь к тому, чтобы финальный продукт был точным, информативным и интересным для целевой аудитории."""
    ),
    verbose=True,
    allow_delegation=True, 
    llm=llm
)

researcher = Agent(
    role='Старший научный сотрудник',
    goal='Находить, анализировать и структурировать самую актуальную и достоверную информацию по теме "Искусственный интеллект в медицине".',
    backstory=dedent("""\
        Вы ведущий специалист по поиску и анализу информации в области высоких технологий и медицины. 
        Вы умеете работать с научными публикациями, отчетами исследовательских центров и новостными статьями. 
        Ваша цель - предоставить исчерпывающую и хорошо структурированную базу знаний для писателя."""
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)

writer = Agent(
    role='Профессиональный технический писатель',
    goal='Создавать увлекательные, глубокие и технически точные статьи на тему "Искусственный интеллект в медицине" на основе предоставленных исследований.',
    backstory=dedent("""\
        Вы талантливый технический писатель, способный превращать сложные концепции в понятный и интересный текст. 
        Вы пишете для аудитории, которая может включать как специалистов, так и людей, только начинающих знакомство с темой. 
        Ваша задача - создать статью, которая будет одновременно информативной и легко читаемой."""
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)
print("Агенты созданы.")

# 2. Определение задач
print("Определение задач...")
topic_for_tasks = "Искусственный интеллект в медицине"

# ----- НАЧАЛО: ЛОГИРОВАНИЕ И УПРОЩЕНИЕ ЗАДАЧ -----
print("\nDEBUG: Исходные описания задач:")
original_research_description = dedent(f"""\
    Провести всестороннее и глубокое исследование на тему '{topic_for_tasks}'.
    Сфокусируйтесь на следующих аспектах:
    1.  Последние достижения (например, в диагностике, разработке лекарств, роботизированной хирургии).
    2.  Ключевые проблемы и вызовы (этические дилеммы, безопасность данных, стоимость внедрения).
    3.  Будущие перспективы и прогнозы развития на ближайшие 5-10 лет.
    4.  Конкретные примеры успешного применения ИИ в медицине.
    Ваша задача - собрать факты, статистику, цитаты экспертов и ссылки на авторитетные источники."""
)
original_research_expected_output = dedent(f"""\
    Детальный структурированный отчет по теме '{topic_for_tasks}', включающий:
    - Обзор последних достижений с примерами.
    - Анализ ключевых проблем и вызовов.
    - Прогноз будущих перспектив.
    - Список использованных авторитетных источников (не менее 5).
    - Ключевые статистические данные и цитаты."""
)
original_writing_description = dedent(f"""\
    Написать высококачественную, увлекательную и информативную статью на тему '{topic_for_tasks}', 
    основываясь на предоставленных результатах исследования.
    Статья должна быть структурирована следующим образом:
    1.  Введение (актуальность темы, краткий обзор статьи).
    2.  Основная часть (несколько разделов, раскрывающих ключевые аспекты ИИ в медицине, 
        согласно исследованию: достижения, проблемы, перспективы).
    3.  Заключение (основные выводы, взгляд в будущее).
    Статья должна быть написана доступным языком, но с сохранением технической точности. 
    Используйте данные и примеры из отчета исследователя."""
)
original_writing_expected_output = dedent(f"""\
    Готовая к публикации статья в формате markdown объемом не менее 800 слов по теме '{topic_for_tasks}'.
    Статья должна быть хорошо структурирована, содержать подзаголовки, списки (при необходимости) 
    и быть написана ясным и привлекательным языком. 
    Финальный результат сохранить в файл."""
)

# Экспериментальное упрощение описаний
simplified_research_description = f"Провести исследование на тему '{topic_for_tasks}'. Собрать факты, статистику, примеры, проблемы и перспективы. Нужны ссылки на источники."
simplified_research_expected_output = f"Отчет по исследованию темы '{topic_for_tasks}' с основными выводами и источниками."

simplified_writing_description = f"Написать статью на тему '{topic_for_tasks}' на основе предоставленного исследования. Статья должна быть информативной и структурированной."
simplified_writing_expected_output = f"Готовая статья в markdown по теме '{topic_for_tasks}'."

print(f"DEBUG: Тип simplified_research_description: {type(simplified_research_description)}")
print(f"DEBUG: simplified_research_description: {simplified_research_description}")
print(f"DEBUG: Тип simplified_research_expected_output: {type(simplified_research_expected_output)}")
print(f"DEBUG: simplified_research_expected_output: {simplified_research_expected_output}")

print(f"DEBUG: Тип simplified_writing_description: {type(simplified_writing_description)}")
print(f"DEBUG: simplified_writing_description: {simplified_writing_description}")
print(f"DEBUG: Тип simplified_writing_expected_output: {type(simplified_writing_expected_output)}")
print(f"DEBUG: simplified_writing_expected_output: {simplified_writing_expected_output}")
# ----- КОНЕЦ: ЛОГИРОВАНИЕ И УПРОЩЕНИЕ ЗАДАЧ -----

# Используем УПРОЩЕННЫЕ описания для отладки основной проблемы
research_task = Task(
  description=simplified_research_description, 
  expected_output=simplified_research_expected_output, 
  agent=researcher
)

# ----- НАЧАЛО: ИЗМЕНЕНИЕ ПУТИ ВЫХОДНОГО ФАЙЛА -----
output_directory = "result"
output_filename = "hierarchical_ai_in_medicine_article.md"
full_output_path = os.path.join(output_directory, output_filename)

print(f"DEBUG: Планируемый путь для сохранения статьи: {os.path.join(os.getcwd(), full_output_path)}")
# ----- КОНЕЦ: ИЗМЕНЕНИЕ ПУТИ ВЫХОДНОГО ФАЙЛА -----

writing_task = Task(
  description=simplified_writing_description,
  expected_output=simplified_writing_expected_output,
  agent=writer,
  context=[research_task],
  output_file=full_output_path # Используем новый путь
)
print("Задачи определены (с упрощенными описаниями и новым путем вывода).")

# ----- НАЧАЛО: ЛОГИРОВАНИЕ ИНСТРУМЕНТОВ МЕНЕДЖЕРА -----
print("\nDEBUG: Инструменты агента team_manager:")
if hasattr(team_manager, 'tools') and team_manager.tools:
    for tool_idx, tool in enumerate(team_manager.tools):
        print(f"  Инструмент {tool_idx + 1}:")
        print(f"    Name: {getattr(tool, 'name', 'N/A')}")
        print(f"    Description: {getattr(tool, 'description', 'N/A')}")
        if hasattr(tool, 'args_schema') and tool.args_schema:
            try:
                # Pydantic v2 uses model_json_schema(), Pydantic v1 used schema_json()
                if hasattr(tool.args_schema, 'model_json_schema'):
                    print(f"    Args Schema: {tool.args_schema.model_json_schema(indent=2)}")
                elif hasattr(tool.args_schema, 'schema_json'): # Fallback for Pydantic v1
                    print(f"    Args Schema: {tool.args_schema.schema_json(indent=2)}")
                else:
                    print("    Args Schema: (не удалось получить json схему)")
            except Exception as e:
                print(f"    Не удалось напечатать схему для {getattr(tool, 'name', 'N/A')}: {e}")
        else:
            print(f"    (Явная args_schema не найдена для {getattr(tool, 'name', 'N/A')})")
else:
    print("  У агента team_manager нет явно определенных инструментов в списке .tools.")

if team_manager.allow_delegation:
    print("  Агент team_manager ИМЕЕТ allow_delegation=True. Это подразумевает доступ к встроенному инструменту делегирования.")
    print("  Ошибка Pydantic возникает при попытке этого встроенного инструмента валидировать свои аргументы 'task' и 'context'.")
    print("  Инструмент ожидает, что 'task' и 'context' будут простыми строками.")
else:
    print("  Агент team_manager НЕ ИМЕЕТ allow_delegation=True.")
# ----- КОНЕЦ: ЛОГИРОВАНИЕ ИНСТРУМЕНТОВ МЕНЕДЖЕРА -----

# 3. Настройка команды (теперь последовательной)
print("Настройка ПОСЛЕДОВАТЕЛЬНОЙ команды...")
sequential_crew = Crew(
    agents=[team_manager, researcher, writer], # team_manager здесь для полноты, но в sequential его роль меньше
    tasks=[research_task, writing_task], 
    process=Process.sequential, # ИЗМЕНЕНО на sequential
    # manager_llm=llm, # УДАЛЕНО, т.к. не требуется для sequential в таком виде
    verbose=True 
)
print("Команда настроена (последовательный процесс).")

# 4. Запуск команды
print(f"\nЗапускаем ПОСЛЕДОВАТЕЛЬНУЮ команду для создания контента на тему: '{topic_for_tasks}'")
result = None
try:
    os.makedirs(output_directory, exist_ok=True)
    print(f"DEBUG: Директория '{output_directory}' проверена/создана.")
    result = sequential_crew.kickoff(inputs={'topic': topic_for_tasks})
except Exception as e:
    print(f"AN EXCEPTION OCCURRED DURING CREW KICKOFF: {e}")
    import traceback
    traceback.print_exc()

print("\n\n==========================================")
print("Завершение работы ПОСЛЕДОВАТЕЛЬНОЙ команды.")
print("Итоговый результат:")
print(result)
# ----- НАЧАЛО: ОБНОВЛЕНИЕ ПРИНТА О ИМЕНИ ФАЙЛА -----
final_article_path_to_print = os.path.join(os.getcwd(), full_output_path)
print(f"Статья должна быть сохранена в файле: {final_article_path_to_print}")
# ----- КОНЕЦ: ОБНОВЛЕНИЕ ПРИНТА О ИМЕНИ ФАЙЛА -----
print("==========================================\n") 