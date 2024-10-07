import os
from fpdf import FPDF

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
                nome = imagem['img_url'].split('/')[-1]  # Nome da imagem com base na URL
                caminho_arquivo = os.path.join("img", nome)

                # Verificar se o arquivo já existe na pasta "img"
                if os.path.exists(caminho_arquivo):
                    try:
                        pdf.image(caminho_arquivo, w=50)  # Ajustar o tamanho conforme necessário
                    except Exception as e:
                        print(f"Erro ao adicionar a imagem {nome_arquivo} ao PDF: {e}")
                else:
                    pdf.cell(200, 10, f"Imagem não encontrada: {nome_arquivo}", ln=True)
                pdf.ln(10)

        pdf.ln(10)

    pdf.output(nome_arquivo)
    print(f"Relatório de auditoria gerado: {nome_arquivo}")