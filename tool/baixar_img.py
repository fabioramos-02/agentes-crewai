import requests
import os

def baixar(img_url, nome_arquivo):
    try:
        # Realizar o download da imagem
        resposta = requests.get(img_url, stream=True)
        resposta.raise_for_status()  # Verificar se o download foi bem-sucedido

        # Caminho completo para salvar a imagem na pasta img
        caminho_arquivo = os.path.join("img", nome_arquivo)

        # Escrever o conteúdo da imagem em um arquivo
        with open(caminho_arquivo, 'wb') as arquivo:
            for chunk in resposta.iter_content(1024):
                arquivo.write(chunk)
        # print(f"Imagem baixada e salva: {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao baixar a imagem {img_url}: {e}")
