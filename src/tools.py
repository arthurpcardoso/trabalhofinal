from crewai_tools import Tool
from problem_agent import load_problems, get_problem_by_id
from execution_agent import run_code
from tutor_agent import start_socratic_chat, get_socratic_question

def _select_problem_function():
    problems = load_problems()
    if not problems:
        print("Nenhum problema encontrado.")
        return None

    print("--- Escolha um Problema ---")
    levels = {}
    for problem in problems:
        level = problem.get('level', 'N/A')
        if level not in levels:
            levels[level] = []
        levels[level].append(problem)

    for level, problem_list in levels.items():
        print(f"\n--- Nível: {level.capitalize()} ---")
        for problem in problem_list:
            print(f"  {problem['id']}: {problem['title']}")

    while True:
        try:
            problem_id = int(input("\nDigite o ID do problema que você quer resolver: "))
            problem = get_problem_by_id(problem_id)
            if problem:
                return problem
            else:
                print("ID do problema inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

select_problem_tool = Tool(
    name="Select Problem",
    func=_select_problem_function,
    description="Selects a programming problem for the user to solve."
)

def _get_user_code_function(problem_details):
    print("\n--- Desafio de Programação ---")
    print(f"Título: {problem_details['title']}")
    print(f"Descrição: {problem_details['description']}")
    print("---------------------------------")

    print("Por favor, insira sua solução abaixo. Use \"END\" em uma linha nova para finalizar.")
    user_code_lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        user_code_lines.append(line)
    
    user_code = "\n".join(user_code_lines)
    if not user_code.strip():
        print("Nenhum código inserido. Tente novamente.")
        return None
    return user_code

get_user_code_tool = Tool(
    name="Get User Code",
    func=_get_user_code_function,
    description="Gets the user's code solution for a given problem."
)

def _run_code_function(user_code, problem_details):
    print("\n--- Avaliando sua solução ---")
    results = run_code(user_code, problem_details['test_cases'])
    
    all_passed = True
    failed_test = None
    for result in results:
        status = "PASSOU" if result['success'] else "FALHOU"
        print(f"- Teste com input {result['input']}: {status}")
        if not result['success']:
            all_passed = False
            if not failed_test:
                failed_test = result
            print(f"  - Esperado: {result['expected']}")
            print(f"  - Recebido: {result['got']}")
            if result['stderr']:
                print(f"  - Erro: {result['stderr']}")

    print("---------------------------------")
    if all_passed:
        print("Parabéns! Você resolveu o problema com sucesso!")
        return {"status": "success", "message": "Problem solved."}
    else:
        print("Sua solução ainda não está correta.")
        return {"status": "failure", "failed_test": failed_test, "user_code": user_code, "problem_details": problem_details}

run_code_tool = Tool(
    name="Run Code",
    func=_run_code_function,
    description="Executes user-provided code against predefined test cases and reports results."
)

def _socratic_chat_function(failed_test_info):
    print("Você gostaria de conversar com o tutor socrático para receber ajuda? (s/n)")
    choice = input().lower()
    
    if choice == 's' and failed_test_info:
        print("\n--- Chat com o Tutor Socrático ---")
        print("Para sair do chat e tentar um novo código, digite 'SAIR'.")
        
        chat_session = start_socratic_chat(
            failed_test_info['problem_details']['description'],
            failed_test_info['user_code'],
            failed_test_info['failed_test']
        )
        
        tutor_question = chat_session.history[-1].parts[0].text
        print(f"\nTutor: {tutor_question}")

        while True:
            user_response = input("Você: ")
            if user_response.strip().upper() == 'SAIR':
                print("\nOk! Vamos tentar novamente.")
                break
            
            tutor_question = get_socratic_question(chat_session, user_response)
            print(f"\nTutor: {tutor_question}")
    
    print("-------------------------------------\n")
    return "Chat session ended."

socratic_chat_tool = Tool(
    name="Socratic Chat",
    func=_socratic_chat_function,
    description="Engages in a socratic chat with the user to help them debug their code."
)
