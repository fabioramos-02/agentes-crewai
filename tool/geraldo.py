import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote
import json
def extrair_links(url, profundidade=2, visitados=None, nivel_atual=0, urls_analizados=None):
    if visitados is None:
        visitados = set()  # Mantém o controle de URLs visitadas para garantir unicidade
    if urls_analizados is None:
        urls_analizados = set()  # Mantém os sites analisados

    if profundidade == 0:
        return [], urls_analizados  # Retornar uma lista vazia

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)

        content_type = response.headers.get('Content-Type', '')
        if "text/html" not in content_type:
            return [], urls_analizados  # Retornar uma lista vazia em vez de set

        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        hrefs = set()

        for link in links:
            href = link.get('href')
            if href:
                if '@' in href or 'javascript:' in href:
                    continue
                href = href.replace('%23', '#')
                if href.endswith(('.pdf', '.docx', '.doc', '.png', '.jpg', '.jpeg')):
                    continue
                href = quote(href, safe=':/?&=#')
                href = urljoin(url, href)
                if urlparse(href).netloc == urlparse(url).netloc and href not in visitados:
                    hrefs.add(href)
                    visitados.add(href)

        urls_analizados.add(url)
        for href in hrefs.copy():
            novos_hrefs, novos_urls_analizados = extrair_links(href, profundidade - 1, visitados, nivel_atual + 1, urls_analizados)
            hrefs.update(novos_hrefs)
            urls_analizados.update(novos_urls_analizados)

        return list(hrefs), urls_analizados  # Converter o set para lista aqui
    except requests.exceptions.Timeout:
        return [], urls_analizados  # Retornar lista vazia em caso de timeout
    except requests.exceptions.RequestException as e:
        return [], urls_analizados  # Retornar lista vazia em caso de erro

def gerar_resposta_json(url_inicial, profundidade):
    # Executar o crawler com o URL fornecido
    todos_os_links, urls_analizados = extrair_links(url_inicial, profundidade=profundidade)

    # Filtrar links válidos
    links_validos = [link for link in todos_os_links if urlparse(link).scheme in ['http', 'https']]

    # Criar o dicionário para gerar o JSON
    resultado_json = {
        "url": url_inicial,
        "quantidade_valida": len(links_validos),
        "urls": [{"link": link} for link in links_validos]
    }

    # Retornar o JSON gerado
    return json.dumps(resultado_json, indent=4)
