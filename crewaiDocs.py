import json
from tool.rastreador_de_url import gerar_resposta_json
from tool.analisa_imagem import analisa  # Importar a função analisa do arquivo
from tool.baixar_img import baixar  # Função para baixar as imagens
from tool.gerar_relatorio import gerar_relatorio_auditoria  # Importar a função gerar_relatorio_auditoria do arquivo
from tool.pdf import gerar_relatorio_pdf  # Importar a função de gerar relatório PDF
import os

def main():
    # Solicitar a URL e a profundidade ao usuário
    url_alvo = input("Digite a URL do site para extração de links: ")

    # Perguntar se o usuário deseja definir um nível de profundidade
    while True:
        escolha = input("Deseja fornecer um nível de profundidade? (s/n): ").strip().lower()
        if escolha == 's':
            profundidade = int(input("Informe a profundidade (Ex: 1, 2, 3...): "))
            break
        elif escolha == 'n':
            profundidade = float('inf')  # Define profundidade como infinita para percorrer todo o site
            break
        else:
            print("Entrada inválida. Por favor, digite 's' para sim e 'n' para não.")

    # Iniciar o processo de extração com a URL e profundidade fornecidas    
    entrada = gerar_resposta_json(url_alvo, profundidade)
    entrada_dict = json.loads(entrada)  # Converter a string JSON para dicionário Python

    # Criar um dicionário para armazenar os resultados da análise
    resultado_analises = {}
    # Criar um conjunto para armazenar as URLs das imagens já baixadas
    imagens_baixadas = set()

    # Caminho para a pasta de imagens
    pasta_img = "img"

    # Criar a pasta se não existir
    os.makedirs(pasta_img, exist_ok=True)

    for url_info in entrada_dict['urls']:
        link = url_info['link']
        try:
            analise_resultado = analisa(link)
            
            # Verificar se há imagens sem o atributo 'alt' e tentar baixá-las
            for imagem in analise_resultado['detalhes_imagens_sem_alt']:
                img_url = imagem['img_url']
                
                # Verificar se a URL já foi baixada
                if img_url not in imagens_baixadas:
                    nome_arquivo = img_url.split('/')[-1]  # Nome da imagem com base na URL
                    
                    # Baixar a imagem e salvar na pasta 'img'
                    baixar(img_url, nome_arquivo)
                    
                    # # Gerar o texto alternativo usando a função da API GPT
                    # texto_alternativo = gerar_texto_alternativo_com_api(nome_arquivo, contexto="governamental")
                    
                    # # Exibir o texto alternativo gerado
                    # print(f"Sugestão de texto alternativo para {nome_arquivo}: {texto_alternativo}")
                    
                    # Adicionar a URL da imagem ao conjunto de imagens baixadas
                    imagens_baixadas.add(img_url)
            
            resultado_analises[link] = analise_resultado
        except Exception as e:
            print(f"Erro ao analisar {link}: {e}")

    # Converter o dicionário de resultados em JSON
    # resultado_json = json.dumps(resultado_analises, indent=4)

    # Gerar o relatório de auditoria
    gerar_relatorio_auditoria(resultado_analises)
    print("Relatórios de auditoria gerados com sucesso!")

if __name__ == "__main__":
    main()
