from docx import Document
from docx.shared import Inches
import os
from PIL import Image, ImageOps

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

# Função para adicionar fundo preto às imagens
def adicionar_fundo_preto(imagem_path):
    # Abrir a imagem
    img = Image.open(imagem_path)
    
    # Verificar se a imagem tem transparência (modo RGBA)
    if img.mode == 'RGBA':
        # Criar uma nova imagem com fundo preto
        fundo_preto = Image.new("RGB", img.size, (0, 0, 0))
        fundo_preto.paste(img, (0, 0), img)
    else:
        # Adicionar um fundo preto direto
        fundo_preto = ImageOps.expand(img, border=0, fill='black')
    
    # Salvar a imagem com fundo preto
    img_com_fundo_preto = os.path.join("img", "preto_" + os.path.basename(imagem_path))
    fundo_preto.save(img_com_fundo_preto)
    return img_com_fundo_preto

# Função para adicionar imagem e sua URL em duas colunas
def adicionar_imagens(doc, imagens):
    for imagem in imagens:
        nome = imagem['img_url'].split('/')[-1]  # Nome da imagem com base na URL
        imagem_path = os.path.join("img", nome)

        # Adicionar fundo preto à imagem
        imagem_com_fundo_preto = adicionar_fundo_preto(imagem_path)

        table = doc.add_table(rows=1, cols=2)  # Criar uma tabela com 2 colunas

        # Adicionar a imagem à primeira coluna dentro de um parágrafo
        img_cell = table.rows[0].cells[0].add_paragraph()
        img_cell.add_run().add_picture(imagem_com_fundo_preto, width=Inches(2))  # Adiciona a imagem com fundo preto

        # Colocar a URL na segunda coluna
        url_cell = table.rows[0].cells[1]
        url_cell.add_paragraph(f" {imagem['img_url']}")

        doc.add_paragraph('-' * 50)  # Separador

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
