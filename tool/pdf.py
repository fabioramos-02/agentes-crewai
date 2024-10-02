import requests
import os
from fpdf import FPDF
from bs4 import BeautifulSoup

# Função para baixar a imagem
def baixar_imagem(img_url, nome_arquivo):
    try:
        resposta = requests.get(img_url, stream=True)
        resposta.raise_for_status()

        # Caminho completo para salvar a imagem
        caminho_arquivo = os.path.join("img", nome_arquivo)
        os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

        # Escrever o conteúdo da imagem no arquivo
        with open(caminho_arquivo, 'wb') as arquivo:
            for chunk in resposta.iter_content(1024):
                arquivo.write(chunk)

        return caminho_arquivo
    except Exception as e:
        print(f"Erro ao baixar a imagem {img_url}: {e}")
        return None

# Função para analisar as imagens de uma página
def analyze_images(html, site_url):
    soup = BeautifulSoup(html, 'html.parser')
    imagens_sem_alt = []
    total_imagens = 0
    imagens_com_alt = 0

    for img in soup.find_all('img'):
        total_imagens += 1
        alt_text = img.get('alt')
        img_url = img.get('src')

        if not img_url.startswith('http'):
            img_url = site_url + img_url  # Constrói URL completa caso seja relativa

        nome_arquivo = f"imagem_{total_imagens}.jpg"
        caminho_arquivo = baixar_imagem(img_url, nome_arquivo)

        if not alt_text or alt_text.strip() == "":
            imagens_sem_alt.append({
                'img_url': img_url,
                'tag_completa': str(img).replace('"', "'"),
                'caminho_arquivo': caminho_arquivo if caminho_arquivo else ''  # Valor padrão se o download falhar
            })
        else:
            imagens_com_alt += 1

    return imagens_sem_alt, total_imagens, imagens_com_alt

# Função para gerar o relatório PDF
def gerar_relatorio_pdf(resultado_analises, nome_arquivo='auditoria.pdf'):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'Relatório de Auditoria de Imagens', ln=True, align='C')
    pdf.ln(10)

    for url, detalhes in resultado_analises.items():
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(200, 10, f"URL Analisada: {url}", ln=True)
        
        pdf.set_font('Arial', '', 12)
        pdf.cell(200, 10, f"Total de Imagens: {detalhes['total_imagens']}", ln=True)
        pdf.cell(200, 10, f"Imagens com 'alt': {detalhes['imagens_com_alt']}", ln=True)
        pdf.cell(200, 10, f"Imagens sem 'alt': {detalhes['qtd_imagens_sem_alt']}", ln=True)

        if detalhes['qtd_imagens_sem_alt'] > 0:
            pdf.cell(200, 10, "Detalhes das imagens sem 'alt':", ln=True)
            pdf.ln(5)

            for imagem in detalhes['detalhes_imagens_sem_alt']:
                pdf.cell(200, 10, f"- URL da Imagem: {imagem['img_url']}", ln=True)
                pdf.cell(200, 10, "  Tag Completa:", ln=True)
                pdf.multi_cell(0, 10, imagem['tag_completa'])

                # Se a imagem foi baixada corretamente, adiciona ao PDF
                if imagem['caminho_arquivo']:
                    pdf.image(imagem['caminho_arquivo'], w=50)
                pdf.ln(10)

        pdf.ln(10)

    pdf.output(nome_arquivo)
    print(f"Relatório de auditoria gerado: {nome_arquivo}")

# Função para realizar a análise de um site e gerar o PDF
def analisa_e_gera_pdf(url):
    try:
        if not url:
            print("Erro: O parâmetro 'url' é obrigatorio.")
            return

        response = requests.get(url)
        html_content = response.content

        imagens_sem_alt, total_imagens, imagens_com_alt = analyze_images(html_content, url)

        resultado_analise = {
            url: {
                "total_imagens": total_imagens,
                "imagens_com_alt": imagens_com_alt,
                "qtd_imagens_sem_alt": len(imagens_sem_alt),
                "detalhes_imagens_sem_alt": imagens_sem_alt
            }
        }

        # Gerar relatório em PDF
        gerar_relatorio_pdf(resultado_analise)

    except Exception as e:
        print(f"Erro: {str(e)}")