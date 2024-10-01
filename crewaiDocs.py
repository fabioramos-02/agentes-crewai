import os
from tokens import get_openai_api_key, get_serper_api_key, get_claude_api_key
from tools import extrair_urls_do_site  # Não chamar diretamente, apenas importar
from crewai import Agent, Task, Crew, Process

# Configurando as chaves de API
os.environ["OPENAI_API_KEY"] = get_openai_api_key()
os.environ["SERPER_API_KEY"] = get_serper_api_key()
os.environ["CLAUDE_KEY"] = get_claude_api_key()

# Instantiate tools
extrator_tools = extrair_urls_do_site  # Referência à tool, sem chamá-la


# Definindo o agente de extração de URLs
agente_extrator_de_urls = Agent(
    role='Responsável por extrair URLs de um site.',
    goal='Fazer o crawling do site alvo e extrair todas as URLs válidas, excluindo links externos e arquivos de mídia.',
    backstory="Especialista em web crawling com profundo entendimento das estruturas da web. que envia para o tools url_inicial, profundidade",
    memory=False,
    verbose=True,
    model='gpt-4o-mini',
    allow_delegation=False,
    tools=[extrator_tools]  # A ferramenta é passada aqui como referência
)


# Definindo a task para o agente de extração de URLs
task_extracao_urls = Task(
    description="Extrair todas as URLs válidas do site fornecido. enviando para o tools url_inicial, profundidade",
    expected_output="Uma dicionario json com todas as URLs válidas do site.",
    agent=agente_extrator_de_urls,
    async_execution=False
)

# Inicialização da Crew com o processo sequencial
crew = Crew(
    agents=[agente_extrator_de_urls],
    tasks=[task_extracao_urls],
    process=Process.sequential,
    verbose=False
)

# Solicitar a URL ao usuário
url_alvo = input("Digite a URL do site para extração de links: ")

# Iniciar o processo de extração com a URL fornecida
result = crew.kickoff(inputs={'url_inicial' : url_alvo, 'profundidade': 2})

# Exibir o resultado final no console
print("##### Resultado final: ########")
print(result)
