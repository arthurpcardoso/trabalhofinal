from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# Configura a API Key do Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.environ.get("GOOGLE_API_KEY")
)

# --- Agente Tutor Socrático ---
socratic_tutor_agent = Agent(
    role='Socratic Tutor',
    goal='Help the user find the solution to the programming problem on their own.',
    backstory='A Socratic tutor that provides hints and asks questions without giving the answer.',
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# --- Tarefa de Tutoria Socrática ---
def create_socratic_tutoring_task(problem_description, user_code, error_info):
    return Task(
        description=f"""
        Act as a Socratic tutor to help the user solve the programming problem.
        The problem description is: {problem_description}
        The user's code is: {user_code}
        The test case that failed is: {error_info}
        The goal is to guide the user to the solution without giving them the answer directly.
        Start the conversation with a single, short, specific question that guides the student to think about the part of the code that likely contains the error.
        """,
        expected_output="A single, short, specific Socratic question to help the user.",
        agent=socratic_tutor_agent,
    )

# --- Tripulação Socrática ---
def create_socratic_crew(problem_description, user_code, error_info):
    task = create_socratic_tutoring_task(problem_description, user_code, error_info)
    return Crew(
        agents=[socratic_tutor_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=2
    )
