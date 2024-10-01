import json
from tool.geraldo import gerar_resposta_json
from tool.fabio import analisa  # Importar a função analisa do arquivo fabio.py
from tool.baixar_img import baixar  # Função para baixar as imagens
from tool.auditoria import gerar_relatorio_auditoria  # Importar a função gerar_relatorio_auditoria do arquivo fabio.py

# Solicitar a URL e a profundidade ao usuário
url_alvo = input("Digite a URL do site para extração de links: ")
profundidade = 1  # Profundidade padrão

# Iniciar o processo de extração com a URL e profundidade fornecidas    
entrada = gerar_resposta_json(url_alvo, profundidade)
entrada_dict = json.loads(entrada)  # Converter a string JSON para dicionário Python

# Criar um dicionário para armazenar os resultados da análise
resultado_analises = {}
# Criar um conjunto para armazenar as URLs das imagens já baixadas
imagens_baixadas = set()

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
                baixar(f"{img_url}, {nome_arquivo}")
                
                # Adicionar a URL da imagem ao conjunto de imagens baixadas
                imagens_baixadas.add(img_url)
            # else:
                # print(f"Imagem já foi baixada: {img_url}")
        
        resultado_analises[link] = analise_resultado
    except Exception as e:
        print(f"Erro ao analisar {link}: {e}")



# Converter o dicionário de resultados em JSON
resultado_json = json.dumps(resultado_analises, indent=4)

# Exibir o resultado em formato JSON
# print(resultado_json)

gerar_relatorio_auditoria(resultado_analises)  # Gerar o relatório de auditoria

