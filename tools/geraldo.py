import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote
import urllib3

# Suprimir o aviso de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def extrair_links(url, profundidade=2, visitados=None):
    if visitados is None:
        visitados = set()  # Mantém o controle de URLs visitadas para garantir unicidade

    if profundidade == 0:
        return set()  # Para a recursão quando a profundidade máxima é atingida

    # Headers para simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        # Tentar fazer a requisição com um timeout de 10 segundos e ignorar possíveis problemas com SSL
        response = requests.get(url, headers=headers, timeout=10, verify=False)

        # Verificar o tipo de conteúdo
        content_type = response.headers.get('Content-Type', '')
        print(f"Tipo de conteúdo recebido: {content_type}")

        # Se o conteúdo não for HTML, ignorar
        if "text/html" not in content_type:
            print(f"Ignorando conteúdo não-HTML: {url}")
            return set()

        # Forçar codificação para UTF-8
        response.encoding = 'utf-8'

        # Analisar o HTML usando o parser 'html.parser' (padrão do Python)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todas as tags <a> e extrair os links
        links = soup.find_all('a')
        hrefs = set()  # Usar um conjunto para garantir links únicos

        for link in links:
            href = link.get('href')

            # Verificar se o href é válido e não é None
            if href:
                # Ignorar links com caracteres indesejados como '@'
                if '@' in href or 'javascript:' in href:
                    continue

                # Substituir '%23' por '#' na URL
                href = href.replace('%23', '#')

                # Ignorar arquivos .pdf, .docx, .doc    
                if href.endswith(('.pdf', '.docx', '.doc', '.png', '.jpg', '.jpeg')):
                    continue

                # Codificar caracteres especiais na URL
                href = quote(href, safe=':/?&=#')

                # Converter links relativos para absolutos
                href = urljoin(url, href)

                # Filtrar links externos e duplicados
                if urlparse(href).netloc == urlparse(url).netloc and href not in visitados:
                    hrefs.add(href)
                    visitados.add(href)  # Marca o link como visitado

        # Recursivamente buscar os links dentro dos links encontrados
        for href in hrefs.copy():  # Usamos .copy() para evitar modificar o conjunto enquanto iteramos
            print(f"Visitando: {href}")
            hrefs.update(extrair_links(href, profundidade - 1, visitados))  # Reduz a profundidade em cada iteração

        return hrefs
    except requests.exceptions.Timeout:
        print("Erro: Tempo de requisição excedido.")
        return set()

    except requests.exceptions.RequestException as e:
        print(f"Erro durante a requisição: {e}")
        return set()


# Solicitar a URL do usuário
url_inicial = input("Digite o URL do site que você deseja buscar os links: ")

# Verificar se a URL começa com http:// ou https://
if not url_inicial.startswith(('http://', 'https://')):
    url_inicial = 'http://' + url_inicial  # Adicionar http:// se estiver faltando

# Solicitar a profundidade de busca
profundidade = int(input("Digite a profundidade de busca (número de níveis de links): "))

# Executar o crawler com o URL fornecido
todos_os_links = extrair_links(url_inicial, profundidade=profundidade)

# Solicitar o nome do arquivo .txt
nome_arquivo = input("Digite o nome do arquivo .txt para salvar os links: ") + '.txt'

# Salvar os links únicos em um arquivo .txt
with open(nome_arquivo, 'w') as arquivo:
    for link in todos_os_links:
        arquivo.write(link + '\n')

print(f"\nTodos os links únicos foram salvos no arquivo '{nome_arquivo}'")
