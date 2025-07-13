import json
import os
import subprocess
from crewai.tools import tool

DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 
    'data', 
    'problems.json'
)

@tool("Problem Loader Tool")
def load_problems():
    """Carrega todos os problemas do arquivo JSON."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return "Arquivo de problemas não encontrado."

@tool("Problem Retriever Tool")
def get_problem_by_id(problem_id: int):
    """Retorna um problema específico pelo seu ID."""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            problems = json.load(f)
        for problem in problems:
            if problem['id'] == problem_id:
                return problem
        return "Problema com o ID especificado não encontrado."
    except FileNotFoundError:
        return "Arquivo de problemas não encontrado."

@tool("Code Executor Tool")
def run_code(code: str, test_cases: list):
    """Executa um código Python com uma lista de casos de teste."""
    results = []
    for case in test_cases:
        try:
            func_name = code.split("def ")[1].split("(")[0]
            input_args = ', '.join(map(str, case["input"]))
            exec_code = f"""
{code}
print({func_name}({input_args}))
"""
            process = subprocess.run(
                ['python', '-c', exec_code],
                capture_output=True,
                text=True,
                timeout=5
            )
            stdout = process.stdout.strip()
            stderr = process.stderr.strip()
            expected_output = str(case["output"])
            results.append({
                "input": case["input"],
                "expected": expected_output,
                "got": stdout,
                "stderr": stderr,
                "success": stdout == expected_output and not stderr
            })
        except Exception as e:
            results.append({
                "input": case["input"],
                "expected": case["output"],
                "got": "",
                "stderr": str(e),
                "success": False
            })
    return results