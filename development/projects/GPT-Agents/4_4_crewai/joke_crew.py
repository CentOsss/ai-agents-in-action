from textwrap import dedent
import os
from typing import List

import agentops
from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv
from langchain.tools import StructuredTool

# Инициализация AgentOps
agentops.init()

# Загрузка переменных окружения
load_dotenv()

def translate_text(text: str, target_language: str) -> str:
    """Переводит текст на указанный язык."""
    return f"Перевод на {target_language}: {text}"

def analyze_trends(topic: str) -> str:
    """Анализирует популярность темы в социальных сетях."""
    return f"Анализ популярности темы '{topic}'"

translate_tool = StructuredTool.from_function(
    func=translate_text,
    name="translate_text",
    description="Переводит текст на указанный язык."
)

analyze_trends_tool = StructuredTool.from_function(
    func=analyze_trends,
    name="analyze_trends",
    description="Анализирует популярность темы в социальных сетях."
)

# Создание агента-исследователя шуток
joke_researcher = Agent(
    role="Senior Joke Researcher",
    goal="Research what makes things funny about the following {topic}",
    verbose=True,
    memory=True,
    backstory=dedent(
        """
        Driven by slapstick humor, you are a seasoned joke researcher
        who knows what makes people laugh. You have a knack for finding
        the funny in everyday situations and can turn a dull moment into
        a laugh riot.
        """
    ),
    allow_delegation=True,
)

# Создание агента-писателя шуток
joke_writer = Agent(
    role="Joke Writer",
    goal="Write a humourous and funny joke on the following {topic}",
    verbose=True,
    memory=True,
    backstory=dedent(
        """
        You are a joke writer with a flair for humor. You can turn a
        simple idea into a laugh riot. You have a way with words and
        can make people laugh with just a few lines.
        """
    ),
    allow_delegation=False,
)

# Создание агента-переводчика
translator = Agent(
    role="Joke Translator",
    goal="Translate jokes while preserving their humor",
    verbose=True,
    memory=True,
    backstory=dedent(
        """
        You are a skilled translator with a deep understanding of
        cultural nuances and humor. You can translate jokes while
        maintaining their comedic value across different languages.
        """
    ),
    tools=[translate_tool],
    allow_delegation=False,
)

# Создание агента-аналитика
analyst = Agent(
    role="Humor Analyst",
    goal="Analyze joke popularity and trends",
    verbose=True,
    memory=True,
    backstory=dedent(
        """
        You are a data-driven analyst specializing in humor trends.
        You can identify what makes jokes popular and predict
        which topics will resonate with audiences.
        """
    ),
    tools=[analyze_trends_tool],
    allow_delegation=False,
)

# Создание задач
research_task = Task(
    description=dedent(
        """
        Identify what makes the following topic:{topic} so funny.
        Be sure to include the key elements that make it humourous.
        Also, provide an analysis of the current social trends,
        and how it impacts the perception of humor.
        """
    ),
    expected_output="A comprehensive 3 paragraphs long report on the latest jokes.",
    agent=joke_researcher,
)

write_task = Task(
    description=dedent(
        """
        Compose an insightful, humourous and socially aware joke on {topic}.
        Be sure to include the key elements that make it funny and
        relevant to the current social trends.
        """
    ),
    expected_output="A joke on {topic}.",
    agent=joke_writer,
    async_execution=False,
    output_file="the_best_joke.md",
)

translate_task = Task(
    description=dedent(
        """
        Translate the joke into the following languages: {languages}.
        Ensure the humor is preserved in each translation.
        """
    ),
    expected_output="Translations of the joke in specified languages.",
    agent=translator,
    async_execution=True,
)

analyze_task = Task(
    description=dedent(
        """
        Analyze the popularity and potential impact of the joke
        on the topic: {topic}. Consider current trends and audience
        preferences.
        """
    ),
    expected_output="Analysis report of joke popularity and trends.",
    agent=analyst,
    async_execution=True,
)

# Создание команды
crew = Crew(
    agents=[joke_researcher, joke_writer, translator, analyst],
    tasks=[research_task, write_task, translate_task, analyze_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True,
)

def run_joke_crew(topic: str, languages: List[str] = ["Spanish", "French", "German"]) -> str:
    """
    Запускает команду шутников с указанной темой и языками для перевода.
    
    Args:
        topic (str): Тема для шутки
        languages (List[str]): Список языков для перевода
        
    Returns:
        str: Результат работы команды
    """
    try:
        result = crew.kickoff(inputs={"topic": topic, "languages": languages})
        return result
    except Exception as e:
        print(f"Ошибка при выполнении команды: {str(e)}")
        return None

if __name__ == "__main__":
    # Пример использования
    result = run_joke_crew("AI engineer jokes")
    print("\nРезультат работы команды:")
    print("------------------------")
    print(result) 