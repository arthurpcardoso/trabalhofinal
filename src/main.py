from problem_agent import load_problems, get_problem_by_id
from execution_agent import run_code
from crew_agents import create_socratic_crew

def select_problem():
    """Exibe os problemas e permite que o usuário selecione um."""
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

def main():
    """Função principal que orquestra a interação com o usuário."""
    
    problem = select_problem()
    if not problem:
        return

    print("\n--- Desafio de Programação ---")
    print(f"Título: {problem['title']}")
    print(f"Descrição: {problem['description']}")
    print("---------------------------------")
    
    while True: # Loop para permitir que o usuário tente novamente
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
            continue

        print("\n--- Avaliando sua solução ---")
        results = run_code(user_code, problem['test_cases'])
        
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
            break # Encerra o loop principal se o problema for resolvido
        else:
            print("Sua solução ainda não está correta.")
            print("Você gostaria de conversar com o tutor socrático para receber ajuda? (s/n)")
            choice = input().lower()
            
            if choice == 's' and failed_test:
                print("\n--- O Tutor Socrático está pensando em uma dica... ---")
                
                # Cria e executa a tripulação socrática
                socratic_crew = create_socratic_crew(
                    problem['description'],
                    user_code,
                    failed_test
                )
                
                tutor_question = socratic_crew.kickoff()
                
                print(f"\nTutor: {tutor_question}")

            print("-------------------------------------\n")
            # O loop principal continua, permitindo uma nova submissão de código

if __name__ == "__main__":
    main()