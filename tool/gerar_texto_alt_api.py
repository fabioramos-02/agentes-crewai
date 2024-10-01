import os
import openai
from tokens import get_openai_api_key

# Configurar sua chave de API da OpenAI
openai.api_key = get_openai_api_key()

# Contexto padrão para a descrição da imagem
contexto = """
As imagens que você está analisando serão utilizadas em um site governamental. Elas desempenham um papel informativo ou visual que complementa o conteúdo principal do site. O público alvo inclui cidadãos comuns que acessam o site para obter informações ou realizar serviços relacionados ao governo.
As descrições das imagens devem ser simples, claras e objetivas, utilizando uma linguagem cidadã, que seja inclusiva e fácil de entender para todas as faixas etárias e níveis de instrução. A descrição deve transmitir o propósito da imagem, sem se aprofundar em detalhes técnicos ou complexos, e deve garantir que usuários com deficiência visual possam entender o contexto da imagem através de leitores de tela.

Exemplos de Imagens Comuns:

Logotipos de órgãos governamentais.
Banners com mensagens institucionais ou avisos importantes.
Ícones de navegação ou serviços públicos (como 'Atendimento', 'Ouvidoria', 'Serviços Online').
Fotografias ilustrativas relacionadas a eventos ou programas governamentais.
Gráficos ou tabelas que transmitem informações visuais (deve-se descrever o que o gráfico ou tabela representa).
Instruções para Geração de Texto Alternativo:

Objetividade: A descrição deve focar no que a imagem representa de maneira direta.
Propósito: A descrição deve refletir o propósito da imagem, seja decorativo, informativo ou funcional.
Evitar Redundância: Se o contexto do conteúdo ao redor da imagem já deixa claro a mensagem da imagem, o texto alternativo pode ser simples e breve.
Evitar Detalhes Técnicos: Não use termos muito específicos ou técnicos. Mantenha a linguagem simples e direta.
"""

# Função para gerar texto alternativo usando a API GPT-4
def gerar_texto_alternativo_com_api(imagem_nome, contexto):
    """
    Gera texto alternativo para uma imagem usando o modelo GPT da OpenAI.
    
    Args:
        imagem_nome (str): O nome da imagem para a qual o texto alternativo será gerado.
        contexto (str): O contexto em que a imagem será usada, por padrão governamental.
    
    Returns:
        str: Texto alternativo gerado para a imagem.
    """
    # Contexto da solicitação para o GPT
    prompt = f"Você é um especialista em acessibilidade. Descreva a imagem '{imagem_nome}' de maneira clara e objetiva para ser usada em um site governamental. A descrição deve ser simples e incluir o contexto da imagem, sem usar termos técnicos complexos."
    
    try:
        # Chamar a API do OpenAI usando ChatCompletion
        resposta = openai.ChatCompletion.create(
            model="gpt-4",  # ou gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "Você é um especialista em acessibilidade de sites governamentais."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100,
            n=1,
            temperature=0.7,
        )
        
        # Acessar o texto gerado na estrutura correta
        texto_alternativo = resposta['choices'][0]['message']['content'].strip()
        return texto_alternativo
    
    except Exception as e:
        print(f"Erro ao gerar texto alternativo para {imagem_nome}: {e}")
        return None

# Função para processar todas as imagens na pasta 'img' e gerar textos alternativos
def processar_imagens_na_pasta(pasta_img="img"):
    """
    Processa todas as imagens da pasta e gera textos alternativos usando a API GPT.
    
    Args:
        pasta_img (str): O caminho para a pasta onde as imagens estão armazenadas.
    """
    # Verificar se a pasta existe
    if not os.path.exists(pasta_img):
        print(f"Pasta '{pasta_img}' não encontrada!")
        return

    # Criar ou abrir um arquivo para armazenar as descrições
    with open("descricoes_imagens.txt", "w", encoding="utf-8") as arquivo_descricoes:
        # Iterar sobre os arquivos na pasta
        for imagem_nome in os.listdir(pasta_img):
            caminho_imagem = os.path.join(pasta_img, imagem_nome)
            
            # Verificar se é um arquivo de imagem (exemplo com extensões comuns)
            if imagem_nome.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # Gerar o texto alternativo para a imagem
                texto_alternativo = gerar_texto_alternativo_com_api(imagem_nome, contexto)
                
                if texto_alternativo:
                    # Escrever a descrição no arquivo de texto
                    arquivo_descricoes.write(f"Imagem: {imagem_nome}\n")
                    arquivo_descricoes.write(f"Texto Alternativo: {texto_alternativo}\n\n")
                    print(f"Texto alternativo gerado para {imagem_nome}: {texto_alternativo}")
                else:
                    print(f"Não foi possível gerar texto alternativo para {imagem_nome}")
            else:
                print(f"{imagem_nome} não é uma imagem válida.")
