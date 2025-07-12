
import json
import os

# Constrói o caminho para o arquivo de problemas
# Isso torna o script executável de qualquer lugar
DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 
    'data', 
    'problems.json'
)

def load_problems():
    """Carrega todos os problemas do arquivo JSON."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def get_problem_by_id(problem_id):
    """Retorna um problema específico pelo seu ID."""
    problems = load_problems()
    for problem in problems:
        if problem['id'] == problem_id:
            return problem
    return None
