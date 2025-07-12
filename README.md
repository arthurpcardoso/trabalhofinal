# Tutor Socrático de Python

Este projeto é um sistema multiagente em linha de comando (CLI) que atua como um tutor de programação Python para iniciantes. O sistema apresenta problemas de algoritmos, avalia as soluções do aluno e, em vez de dar respostas diretas, faz perguntas socráticas para guiar o aluno à solução correta.

## Como Funciona

O sistema utiliza um modelo de linguagem da Google (Gemini) para gerar perguntas socráticas personalizadas. Quando um aluno submete uma solução incorreta, o sistema analisa o código, o erro e o contexto do problema. Com base nessa análise, o "agente tutor" formula uma pergunta que estimula o aluno a refletir sobre a lógica do seu código e a identificar o erro por conta própria.

## Arquitetura

O projeto é dividido em três agentes principais, cada um com uma responsabilidade clara:

- **Agente de Problemas (`problem_agent.py`):** Responsável por carregar e fornecer os problemas de programação a partir de um arquivo `problems.json`.
- **Agente de Execução (`execution_agent.py`):** Executa o código do aluno em um ambiente seguro e compara a saída com os casos de teste esperados para verificar a corretude da solução.
- **Agente Tutor (`tutor_agent.py`):** O coração do sistema. Este agente se comunica com a API do Gemini para gerar perguntas socráticas. Ele envia o contexto do problema, o código do aluno e os detalhes do erro para o modelo de linguagem e recebe de volta uma pergunta para guiar o aluno.

O fluxo de interação é orquestrado pelo `main.py`, que atua como o ponto de entrada da aplicação.

## Como Executar

### Pré-requisitos

- Python 3.6+
- Uma chave de API do Google Gemini

### Passos

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie um ambiente virtual e instale as dependências:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows, use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```
   *(Nota: O arquivo `requirements.txt` precisa ser criado. Com base no código, ele deve conter `google-generativeai`)*

3. **Configure sua chave de API:**
   - Renomeie o arquivo `.env.example` para `.env`.
   - Abra o arquivo `.env` e adicione sua chave de API do Google Gemini:
     ```
     GOOGLE_API_KEY="SUA_CHAVE_DE_API_AQUI"
     ```

4. **Execute o programa:**
   ```bash
   python src/main.py
   ```

O programa irá apresentar um desafio de programação. Escreva sua solução no terminal e digite "END" em uma nova linha para submeter. Se a solução estiver incorreta, o sistema oferecerá ajuda do tutor socrático.