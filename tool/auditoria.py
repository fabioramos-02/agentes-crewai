import json

# Função para gerar um relatório de auditoria
def gerar_relatorio_auditoria(resultado_analises: str, nome_arquivo='auditoria.txt') -> str:
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write("Relatório de Auditoria\n")
        arquivo.write("="*50 + "\n\n")

        # Iterar sobre os resultados da análise
        for url, detalhes in resultado_analises.items():
            arquivo.write(f"URL Analisada: {url}\n")
            arquivo.write(f"Total de Imagens: {detalhes['total_imagens']}\n")
            arquivo.write(f"Imagens com 'alt': {detalhes['imagens_com_alt']}\n")
            arquivo.write(f"Imagens sem 'alt': {detalhes['qtd_imagens_sem_alt']}\n")

            if detalhes['qtd_imagens_sem_alt'] > 0:
                arquivo.write("Detalhes das imagens sem 'alt':\n")
                for imagem in detalhes['detalhes_imagens_sem_alt']:
                    arquivo.write(f"- URL da Imagem: {imagem['img_url']}\n")
                    arquivo.write(f"  Tag Completa: {imagem['tag_completa']}\n")
            else:
                arquivo.write("Todas as imagens possuem atributo 'alt'.\n")

            arquivo.write("\n" + "-"*50 + "\n\n")

    print(f"Relatório de auditoria gerado: {nome_arquivo}")