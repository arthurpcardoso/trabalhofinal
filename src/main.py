from crewai import Agent, Task, Crew, Process
from tools import select_problem_tool, get_user_code_tool, run_code_tool, socratic_chat_tool
import os

# Ensure GOOGLE_API_KEY is set
if not os.environ.get("GOOGLE_API_KEY"):
    print("Erro: A variável de ambiente GOOGLE_API_KEY não está configurada.")
    print("Por favor, configure-a antes de executar o programa.")
    exit()

# Define Agents
problem_selector = Agent(
    role='Problem Selector',
    goal='Select a programming problem for the user to solve',
    backstory='An expert in curating programming challenges based on user input.',
    verbose=True,
    allow_delegation=False,
    tools=[select_problem_tool]
)

code_executor = Agent(
    role='Code Executor',
    goal='Execute user-provided code against predefined test cases and report results',
    backstory='A meticulous code runner that provides detailed feedback on code execution.',
    verbose=True,
    allow_delegation=False,
    tools=[get_user_code_tool, run_code_tool]
)

socratic_tutor = Agent(
    role='Socratic Tutor',
    goal='Guide the user to find solutions to programming problems through socratic questioning',
    backstory='A patient and insightful tutor who never gives direct answers, only guiding questions.',
    verbose=True,
    allow_delegation=False,
    tools=[socratic_chat_tool]
)

# Define Tasks
select_problem_task = Task(
    description=(
        "Select a programming problem for the user to solve. "
        "Use the `select_problem_tool` to interact with the user and get their choice."
    ),
    expected_output="A dictionary containing the selected problem's details.",
    agent=problem_selector,
)

get_user_code_task = Task(
    description=(
        "Present the selected problem to the user and get their code solution. "
        "Use the `get_user_code_tool` to interact with the user. "
        "The input to this tool should be the problem details from the previous task."
    ),
    expected_output="A string containing the user's code solution.",
    agent=code_executor,
    context=[select_problem_task]
)

execute_code_task = Task(
    description=(
        "Execute the provided user code against the problem's test cases and report results. "
        "Use the `run_code_tool` to perform the execution. "
        "The input to this tool should be the user's code and the problem details."
    ),
    expected_output="A dictionary indicating the success or failure of the code execution, including failed test details if any.",
    agent=code_executor,
    context=[get_user_code_task, select_problem_task]
)

socratic_chat_task = Task(
    description=(
        "If the code execution failed, engage in a socratic chat with the user to help them debug their code. "
        "Use the `socratic_chat_tool` to facilitate the conversation. "
        "The input to this tool should be the failed test information from the previous task."
    ),
    expected_output="A message indicating the chat session has ended.",
    agent=socratic_tutor,
    context=[execute_code_task],
    human_input=True # This task requires human input for the chat
)

# Create the Crew
crew = Crew(
    agents=[problem_selector, code_executor, socratic_tutor],
    tasks=[
        select_problem_task,
        get_user_code_task,
        execute_code_task,
        socratic_chat_task
    ],
    verbose=2, # You can set it to 1 or 2 to different logging levels
    process=Process.sequential # Ensures tasks run in order
)

# Kickoff the crew
if __name__ == "__main__":
    result = crew.kickoff()
    print("\n\n########################")
    print("## Crew finished tasks:")
    print(result)
    print("########################")