from docx import Document
from docx.shared import Inches
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

# Função para adicionar imagens e suas URLs em uma tabela com duas colunas
def adicionar_imagens(doc, imagens):
    for imagem in imagens:
        nome_arquivo = imagem['img_url'].split('/')[-1]  # Nome da imagem com base na URL
        caminho_imagem = os.path.join("img", nome_arquivo)  # Caminho para a imagem

        # Criar uma tabela com 2 colunas
        table = doc.add_table(rows=1, cols=2)

        # Adicionar a imagem à primeira coluna
        img_cell = table.rows[0].cells[0]
        p = img_cell.add_paragraph()
        run = p.add_run()

        # Verifica se a imagem foi baixada corretamente
        if os.path.exists(caminho_imagem):
            run.add_picture(caminho_imagem, width=Inches(1.5))  # Adiciona a imagem com tamanho de 1.5 polegadas
        else:
            p.add_run("Imagem não disponível")  # Caso a imagem não tenha sido baixada corretamente

        # Colocar a URL diretamente na segunda coluna
        url_cell = table.rows[0].cells[1]
        p_url = url_cell.add_paragraph()
        p_url.add_run(imagem['img_url'])  # Exibe a URL diretamente

# Função principal para gerar o relatório
def gerar_relatorio_auditoria(resultado_analises: dict, nome_arquivo='auditoria_relatorio.docx'):
    doc = Document()
    doc.add_heading('Relatório de Auditoria', 0)
    
    for url, detalhes in resultado_analises.items():
        doc.add_heading(f'URL Analisada: {url}', level=1)
        
        # Adicionar Tabela com Resumo de Imagens
        adicionar_tabela(doc, detalhes)
        
        # Adicionar imagens sem 'alt' com suas URLs em duas colunas
        adicionar_imagens(doc, detalhes['detalhes_imagens_sem_alt'])
        
    doc.save(nome_arquivo)
    print(f"Relatório de auditoria gerado: {nome_arquivo}")
