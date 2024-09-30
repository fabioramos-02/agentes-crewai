import os
from tokens import get_openai_api_key, get_serper_api_key, get_claude_api_key
from tools import call_claude_api
from crewai import Agent, Task, Crew, Process
from crewai_tools import YoutubeVideoSearchTool, SerperDevTool

os.environ["OPENAI_API_KEY"] = get_openai_api_key()
os.environ["SERPER_API_KEY"] = get_serper_api_key()
os.environ["CLAUDE_KEY"] = get_claude_api_key()

# Tools
youtube_tool = YoutubeVideoSearchTool()
serper_dev = SerperDevTool()
claude_tool = call_claude_api

extrator_de_urls  = Agent(
    role='Responsável por extrair URLs de um site.',
    goal='Fazer o crawling do site alvo e extrair todas as URLs válidas, excluindo links externos e arquivos de mídia.',
    backstory="Especialista em web crawling com profundo entendimento das estruturas da web, capaz de navegar eficientemente pelo DOM para extrair informações necessárias, evitando links inválidos ou redundantes.",
    memory=False,
    verbose=True,
    model='gpt-4o-mini',
    allow_delegation = False
)

agente_de_filtragem = Agent(
    role='Filtrar as URLs extraídas com base em critérios específicos.',
    goal='Encontrar conteúdos na internet sobre o tema abordado para complementarmos a documentação',
    backstory="Pesquisador senior com vasta experiencia em buscas avançadas de conteudo na internet.",
    memory=False,
    verbose=True,
    max_iter=10,
    allow_delegation = False,
    model='gpt-4o-mini',
    tools=[serper_dev]
)

agente_buscador  = Agent(
    role='Buscar Imagens sem alt Text',
    goal='Revisar a documentação gerada pelos Agentes e gerar um documento unico em Markdown',
    backstory="Especialista em revisão de documentos e livros, dominio em Markdown e como deixar um visual mais agradavel",
    memory=False,
    verbose=False,
    max_iter=10,
    model='gpt-4o-mini',
    allow_delegation = False
)

# agente_de_sugestao  = Agent(
#     role='Analisar as Imagens anexadas e sugerir melhorias ou revisões para os links encontrados.',
#     goal='Propor ajustes baseados na análise das URLs, seja removendo links desatualizados ou propondo melhores fontes.',
#     backstory="Experiente em análise de conteúdo da web e melhoria contínua, sugerindo sempre as melhores práticas para manter a qualidade da documentação e análise.",
#     memory=False,
#     verbose=True,
#     max_iter=10,
#     allow_delegation = False,
#     model='gpt-4o-mini'
#     #tools=[claude_tool]
# )

agente_BI  = Agent(
    role='Processar e organizar as informações obtidas para gerar insights.',
    goal='Criar relatórios detalhados com base nos dados extraídos e filtrados, identificando padrões e oportunidades de melhoria.',
    backstory="Especialista em inteligência de negócios, com vasta experiência na geração de relatórios e análise de grandes volumes de dados.",
    memory=False,
    verbose=False,
    max_iter=10,
    model='gpt-4o-mini',
    allow_delegation = False
)
agente_revisor  = Agent(
    role='Revisar as informações coletadas e sugerir correções.',
    goal='Garantir que a documentação final esteja correta e bem estruturada, de acordo com as melhores práticas de redação.',
    backstory="Especialista em revisão de documentos, com grande atenção aos detalhes e capacidade de identificar erros ou inconsistências.",
    memory=False,
    verbose=False,
    max_iter=10,
    model='gpt-4o-mini',
    allow_delegation = False
)

task_documentation = Task(
    description="Documentar a transcrição a seguir: {transcript}",
    expected_output="Uma documentação em Markdown bem detalhada.",
    agent=documentation_specialist,
    async_execution=False
)

task_internet_researcher = Task(
    description="Encontrar conteudos sobre o tema abordado na transcrição",
    expected_output="Extração do conteudo das pesquisas que tenham relação com o resultado, gerar formato de Bullet Points resumidos e unificar as documentações gerando um markdown",
    agent=ai_internet_researcher,
    async_execution=False
)

task_reviewer = Task(
    description="Revisar a documentação gerada anteriormente e propor melhorias",
    expected_output="Juntar as documentações geradas e gerar um Markdown revisado e melhorado, adicionar as referencias utilizadas no final",
    agent=doc_reviewer,
    async_execution=False
)

databricks_reviewer = Task(
    description="Revisar a documentação no nivel técnico",
    expected_output="Documentação em Markdown revisada e melhorada tecnicamente, complementar informações tecnicas se for necessário, ajustar termos e jargões para o publico tecnico",
    agent=databricks_specialist,
    async_execution=False
)

crew = Crew(
    agents=[extrator_de_urls,agente_de_filtragem,agente_buscador,agente_BI],
    tasks=[task_documentation,task_reviewer, task_internet_researcher, databricks_reviewer],
    process=Process.sequential,
    verbose=False
)

print("## Iniciando Crew")
print('-------------------------------')
transcript = open("transcript.txt", "r").read()
result = crew.kickoff(inputs={'transcript': transcript})
print("#################")
print("#####  Resultado final: ########")


# Converter o resultado para uma string e salvar no arquivo
with open("resultado_final.md", "w", encoding="utf-8") as f:
    f.write(str(result))

print("Resultado final salvo em resultado_final.md")
