from docx import Document
from docx.shared import Inches
import os
from tool.gerar_texto_alt_api import gerar_texto_alternativo_com_api

# Função para gerar um relatório de auditoria no formato DOCX com imagens, URLs e textos alternativos
def gerar_relatorio_auditoria(resultado_analises: dict, nome_arquivo='auditoria_relatorio.docx'):
    contexto = """
    As imagens que você está analisando serão utilizadas em um site governamental...
    gere um texto alternativo para cada imagem que seja claro, simples e objetivo.
    """
    
    pasta_img = "img"
    
    # Criar um novo documento DOCX
    doc = Document()
    doc.add_heading('Relatório de Auditoria', 0)

    # Iterar sobre os resultados da análise
    for url, detalhes in resultado_analises.items():
        doc.add_heading(f'URL Analisada: {url}', level=1)
        doc.add_paragraph(f"Total de Imagens: {detalhes['total_imagens']}")
        doc.add_paragraph(f"Imagens com 'alt': {detalhes['imagens_com_alt']}")
        doc.add_paragraph(f"Imagens sem 'alt': {detalhes['qtd_imagens_sem_alt']}")

        if detalhes['qtd_imagens_sem_alt'] > 0:
            doc.add_heading('Detalhes das imagens sem "alt":', level=2)
            for imagem in detalhes['detalhes_imagens_sem_alt']:
                img_url = imagem['img_url']
                nome_arquivo = img_url.split('/')[-1]
                caminho_imagem = os.path.join(pasta_img, nome_arquivo)

                # Verificar se o arquivo da imagem foi baixado corretamente
                if os.path.exists(caminho_imagem):
                    # Adicionar a imagem ao documento
                    doc.add_paragraph(f"Imagem da URL: {img_url}")
                    doc.add_picture(caminho_imagem, width=Inches(3))  # Tamanho ajustável

                    # Gerar o texto alternativo com a API
                    texto_alt = gerar_texto_alternativo_com_api(nome_arquivo, contexto)
                    if texto_alt:
                        doc.add_paragraph(f"Texto Alternativo Sugerido: {texto_alt}")
                    else:
                        doc.add_paragraph("Não foi possível gerar texto alternativo para esta imagem.")
                else:
                    doc.add_paragraph(f"Imagem não encontrada localmente: {nome_arquivo}")

        else:
            doc.add_paragraph("Todas as imagens possuem atributo 'alt'.")

        doc.add_paragraph('-' * 50)

    # Salvar o documento DOCX
    doc.save(nome_arquivo)
    print(f"Relatório de auditoria gerado: {nome_arquivo}")
