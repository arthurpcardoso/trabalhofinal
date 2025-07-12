import google.generativeai as genai
import os

# Configura a API Key do Gemini
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def start_socratic_chat(problem_description, user_code, error_info):
    """
    Inicia uma sessão de chat socrático com o Gemini.

    Args:
        problem_description (str): A descrição do problema.
        user_code (str): O código que o aluno enviou.
        error_info (dict): Um dicionário com detalhes do teste que falhou.

    Returns:
        genai.ChatSession: Uma sessão de chat iniciada.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # --- PROMPT INICIAL PARA O MODELO DE LINGUAGEM ---
    initial_prompt = f"""
    Você é um tutor de programação socrático. Sua missão é ajudar estudantes de programação a encontrarem a solução por conta própria, através de um diálogo, sem nunca dar a resposta diretamente.
    
    O estudante está tentando resolver o seguinte problema:
    ---
    {problem_description}
    ---
    
    O código que ele escreveu foi:
    ---
    {user_code}
    ---
    
    Ao rodar o código com o input `{error_info['input']}`, o resultado esperado era `{error_info['expected']}`, mas o código produziu `{error_info['got']}`.
    Se houve um erro de execução, ele foi: {error_info['stderr']}

    Analise o código e o erro. Inicie a conversa com uma única pergunta curta e específica que guie o estudante a pensar sobre a parte do código que provavelmente contém o erro. 
    
    **REGRAS IMPORTANTES:**
    1.  **NUNCA** dê a resposta ou a solução direta.
    2.  **SEMPRE** responda com uma pergunta que o faça pensar.
    3.  Mantenha as perguntas curtas e focadas.
    4.  Baseie suas perguntas no código e no erro apresentado.
    5.  Se o estudante fizer uma pergunta, responda com outra pergunta que o ajude a encontrar a resposta por si mesmo.
    6.  Se o estudante corrigir o código, você receberá o novo código e o novo erro para continuar a conversa.
    """
    
    chat = model.start_chat(history=[])
    # Envia o prompt inicial para obter a primeira pergunta
    chat.send_message(initial_prompt) 
    return chat

def get_socratic_question(chat_session, user_response):
    """
    Continua a conversa socrática enviando a resposta do usuário e obtendo a próxima pergunta.

    Args:
        chat_session (genai.ChatSession): A sessão de chat ativa.
        user_response (str): A resposta do usuário à pergunta anterior.

    Returns:
        str: A próxima pergunta socrática gerada pelo LLM.
    """
    try:
        # Envia a resposta do usuário para o chat
        response = chat_session.send_message(user_response)
        
        if response and response.text:
            return response.text.strip()
        else:
            return "Não consegui gerar uma nova pergunta. Tente responder novamente."
    except Exception as e:
        return f"Ocorreu um erro ao tentar continuar a conversa: {e}."
