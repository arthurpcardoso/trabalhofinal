
import subprocess
import json

def run_code(code, test_cases):
    results = []
    for case in test_cases:
        # Extrai o nome da função da descrição do problema
        # (uma abordagem simples, pode ser melhorada)
        try:
            func_name = code.split("def ")[1].split("(")[0]
            
            # Constrói o código para execução
            # Isso assume que a função retorna um valor
            input_args = ', '.join(map(str, case["input"]))
            exec_code = f"""
{code}
print({func_name}({input_args}))
"""
            
            process = subprocess.run(
                ['python', '-c', exec_code],
                capture_output=True,
                text=True,
                timeout=5 # Timeout para evitar loops infinitos
            )
            
            stdout = process.stdout.strip()
            stderr = process.stderr.strip()
            
            # Normaliza o tipo de dado do output esperado
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
