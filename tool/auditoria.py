from docx import Document
from docx.shared import Inches  # Adicionar esta linha para importar o objeto Inches
import os

# Função para criar uma tabela no documento
def adicionar_tabela(doc, detalhes):
    table = doc.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Total de Imagens'
    hdr_cells[1].text = 'Imagens com "alt"'
    hdr_cells[2].text = 'Imagens sem "alt"'

    # Preencher a tabela com os dados
    row_cells = table.add_row().cells
    row_cells[0].text = str(detalhes['total_imagens'])
    row_cells[1].text = str(detalhes['imagens_com_alt'])
    row_cells[2].text = str(detalhes['qtd_imagens_sem_alt'])

    doc.add_paragraph()

# Função para adicionar imagem e sua URL
def adicionar_imagens(doc, imagens):
    for imagem in imagens:
        nome = imagem['img_url'].split('/')[-1]  # Nome da imagem com base na URL'
        doc.add_paragraph('IMAGEM ANEXADA')
        doc.add_picture(os.path.join("img", nome), width=Inches(2))  # Usar Inches corretamente
        doc.add_paragraph(f"URL da Imagem: {imagem['img_url']}")
        doc.add_paragraph('-' * 50)

# Função principal para gerar o relatório
def gerar_relatorio_auditoria(resultado_analises: dict, nome_arquivo='auditoria_relatorio.docx'):
    doc = Document()
    doc.add_heading('Relatório de Auditoria', 0)
    
    for url, detalhes in resultado_analises.items():
        doc.add_heading(f'URL Analisada: {url}', level=1)
        
        # Adicionar Tabela com Resumo de Imagens
        adicionar_tabela(doc, detalhes)
        
        # Adicionar imagens sem 'alt' com suas URLs
        adicionar_imagens(doc, detalhes['detalhes_imagens_sem_alt'])
        
    doc.save(nome_arquivo)
    print(f"Relatório de auditoria gerado: {nome_arquivo}")
