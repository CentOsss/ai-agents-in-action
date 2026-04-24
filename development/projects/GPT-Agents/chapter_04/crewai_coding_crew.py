from textwrap import dedent
from crewai import Agent, Task, Crew, Process
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Убедитесь, что OPENAI_API_KEY загружен. 
# Промпт курса также указывает OPENAI_API_BASE и модель gpt-4o-mini
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") # Это уже должно быть сделано load_dotenv
# os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE", "https://bothub.chat/api/v2/openai/v1/")
# os.environ["OPENAI_MODEL_NAME"] = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")


# Для AgentOps, если используется:
# AGENTSOPS_API_KEY = os.getenv("AGENTSOPS_API_KEY")
# if AGENTSOPS_API_KEY:
#     os.environ["AGENTSOPS_API_KEY"] = AGENTSOPS_API_KEY
# else:
#     print("AGENTSOPS_API_KEY не найден в .env файле. AgentOps не будет использоваться.")

# Для LangSmith, если используется:
# LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
# if LANGCHAIN_API_KEY:
#     os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
#     os.environ["LANGCHAIN_TRACING_V2"] = "true"
#     os.environ["LANGCHAIN_PROJECT"] = "CrewAI Coding Crew Sequential"
# else:
#     print("LANGCHAIN_API_KEY не найден в .env файле. LangSmith не будет использоваться.")


print("## Welcome to the Game Crew")
print("-------------------------------")
game = input("What is the game you would like to build? What will be the mechanics?\n")

# Агенты
senior_engineer_agent = Agent(
    role="Senior Software Engineer",
    goal="Create software as needed",
    backstory=dedent(
        '''You are a Senior Software Engineer at a leading tech think tank.
        Your expertise in programming in python. and do your best to
        produce perfect code'''
    ),
    allow_delegation=False,
    verbose=True,
    # llm=ChatOpenAI() # Можно явно указать LLM, если требуется特定настройка или она отличается от глобальной
)

qa_engineer_agent = Agent(
    role="Software Quality Control Engineer",
    goal="create prefect code, by analizing the code that is given for errors",
    backstory=dedent(
        '''You are a software engineer that specializes in checking code
        for errors. You have an eye for detail and a knack for finding
        hidden bugs. You check for missing imports, variable declarations,
        mismatched brackets and syntax errors. You also check for security
        vulnerabilities, and logic errors'''
    ),
    allow_delegation=False,
    verbose=True,
    # llm=ChatOpenAI()
)

chief_qa_engineer_agent = Agent(
    role="Chief Software Quality Control Engineer",
    goal="Ensure that the code does the job that it is supposed to do",
    backstory=dedent(
        '''You are a Chief Software Quality Control Engineer at a leading tech think tank.
        You are responsible for ensuring that the code that is written does
        the job that it is supposed to do. You are responsible for checking
        the code for errors and ensuring that it is of the highest quality.'''
    ),
    allow_delegation=True, # Только главный QA инженер может делегировать задачи.
    verbose=True,
    # llm=ChatOpenAI()
)

# Задачи
code_task = Task(
    description=dedent(f'''You will create a game using python, these are the instructions:
    Instructions
    ------------
    {game}
    You will write the code for the game using python.'''),
    expected_output="Your Final answer must be the full python code, only the python code and nothing else.",
    agent=senior_engineer_agent,
)

qa_task = Task(
    description=dedent(f'''You are helping create a game using python, these are the instructions:
    Instructions
    ------------
    {game}
    Using the code you got, check for errors. Check for logic errors,
    syntax errors, missing imports, variable declarations, mismatched brackets,
    and security vulnerabilities.'''),
    expected_output="Output a list of issues you found in the code.",
    agent=qa_engineer_agent,
)

evaluate_task = Task(
    description=dedent(f'''You are helping create a game using python, these are the instructions:
    Instructions
    ------------
    {game}
    You will look over the code to insure that it is complete and
    does the job that it is supposed to do.'''),
    expected_output="Your Final answer must be the corrected a full python code, only the python code and nothing else.",
    agent=chief_qa_engineer_agent,
)

# Команда
crew = Crew(
    agents=[senior_engineer_agent, qa_engineer_agent, chief_qa_engineer_agent],
    tasks=[code_task, qa_task, evaluate_task],
    verbose=True,
    process=Process.sequential, # Процесс последовательный
)

# Запуск работы команды
print("\n\n######################")
print("## Starting Game Crew Kickoff!")
print("######################\n")
result = crew.kickoff()

print("\n\n######################")
print("## Game Crew Work Result:")
print("######################\n")
print(result)
