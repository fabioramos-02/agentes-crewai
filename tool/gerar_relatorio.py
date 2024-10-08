from docx import Document
from docx.shared import Inches
import os
from docx.shared import Pt, RGBColor

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
        table = doc.add_table(rows=2, cols=2)  # Duas linhas, uma para o nome e outra para a imagem e URL

        # Primeira linha: nome da imagem
        nome_cell = table.rows[0].cells[0]
        nome_cell.merge(table.rows[0].cells[1])  # Unir as duas colunas para o nome
        p_nome = nome_cell.add_paragraph()
        run_nome = p_nome.add_run(nome_arquivo)
        run_nome.bold = True  # Deixar o nome em negrito
        run_nome.font.size = Pt(12)  # Tamanho da fonte

        # Segunda linha: adicionar a imagem à primeira coluna
        img_cell = table.rows[1].cells[0]
        p_img = img_cell.add_paragraph()
        run_img = p_img.add_run()

        # Verifica se a imagem foi baixada corretamente
        if os.path.exists(caminho_imagem):
            run_img.add_picture(caminho_imagem, width=Inches(1.5))  # Adiciona a imagem com tamanho de 1.5 polegadas
        else:
            p_img.add_run("Imagem não disponível")  # Caso a imagem não tenha sido baixada corretamente

        # Segunda coluna: URL da imagem como link clicável
        url_cell = table.rows[1].cells[1]
        p_url = url_cell.add_paragraph()
        run_url = p_url.add_run(f"Link da Imagem: {imagem['img_url']}")
        run_url.font.color.rgb = RGBColor(0, 0, 255)  # Cor do link em azul
        run_url.underline = True  # Sublinhado
        p_url.hyperlink = imagem['img_url']  # Torna o texto um hyperlink

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
