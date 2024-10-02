from docx import Document

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

       

        doc.add_paragraph('-' * 50)

    # Salvar o documento DOCX
    doc.save(nome_arquivo)
    print(f"Relatório de auditoria gerado: {nome_arquivo}")
