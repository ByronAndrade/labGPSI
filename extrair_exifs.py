import os
from PIL import Image
import pandas as pd

# Função para extrair os dados EXIF de uma única imagem e converter para um dicionário mais legível
def extrair_exif(caminho_imagem):
    try:
        imagem = Image.open(caminho_imagem)
        exif_data = imagem._getexif()
        imagem.close()
        if exif_data is not None:
            exif = {
                "Modelo da Câmera": exif_data.get(272),
                "Data e Hora": exif_data.get(36867),
                "ISO": exif_data.get(34855),
                "Exposição": exif_data.get(33434),
                "Abertura": exif_data.get(33437),
                "Distância Focal": exif_data.get(37386),
                "Flash": exif_data.get(37385),
            }
            return {k: v for k, v in exif.items() if v is not None}
        else:
            return {}
    except IOError as e:
        print(f"Erro ao abrir {caminho_imagem}: {e}. Pode não ser uma imagem ou o arquivo está corrompido.")
        return {}

# Função para processar todas as imagens em uma pasta e salvar os dados em um CSV
def processar_pasta(pasta, nome_arquivo_csv):
    dados_exif = []
    for raiz, dirs, arquivos in os.walk(pasta):
        for nome_arquivo in arquivos:
            if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                caminho_completo = os.path.join(raiz, nome_arquivo)
                exif = extrair_exif(caminho_completo)
                exif["Nome Arquivo"] = nome_arquivo
                dados_exif.append(exif)
    
    df = pd.DataFrame(dados_exif)
    df.to_csv(nome_arquivo_csv, index=False)

# Caminho para o diretório onde o script está sendo executado
diretorio_atual = os.path.dirname(os.path.realpath(__file__))

# Caminhos para as pastas utilizando caminhos relativos
pasta_fotos = os.path.join(diretorio_atual, 'fotos')
pasta_fotos_de_fotos = os.path.join(diretorio_atual, 'fotos_de_fotos')

# Nomes dos arquivos CSV de saída utilizando caminhos relativos
arquivo_csv_fotos = os.path.join(diretorio_atual, 'fotos_exif.csv')
arquivo_csv_fotos_de_fotos = os.path.join(diretorio_atual, 'fotos_de_fotos_exif.csv')

# Processar cada pasta e salvar em CSV
processar_pasta(pasta_fotos, arquivo_csv_fotos)
processar_pasta(pasta_fotos_de_fotos, arquivo_csv_fotos_de_fotos)
