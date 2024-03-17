import os
import csv
from PIL import Image
import piexif
import exifread
import subprocess
import json

def extrair_exif_pillow(caminho_imagem):
    """Extrai os metadados EXIF usando a biblioteca Pillow."""
    try:
        img = Image.open(caminho_imagem)
        exif_data = img._getexif()
        if exif_data:
            return {piexif.TAGS.get(tag, tag): value for tag, value in exif_data.items()}
    except Exception as e:
        print(f'Erro ao processar {caminho_imagem} com Pillow: {e}')
    return {}
   

def extrair_exif_piexif(caminho_imagem):
    """Extrai os metadados EXIF usando a biblioteca piexif, tratando corretamente os tipos de dados."""
    try:
        exif_dict = piexif.load(caminho_imagem)
        exif_data = {}
        for ifd_name in exif_dict:
            if ifd_name == "thumbnail":
                continue  # Ignora os dados da miniatura
            for tag, value in exif_dict[ifd_name].items():
                # Verifica se o valor é um objeto bytes e tenta decodificá-lo
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8', errors='ignore')  # Ignora erros de decodificação
                    except UnicodeDecodeError:
                        value = "<dados binários não decodificáveis>"
                # Converte a tag em um nome legível, se possível
                decoded_tag = piexif.TAGS[ifd_name].get(tag, {'name': str(tag)}).get('name', str(tag))
                exif_data[decoded_tag] = value
        return exif_data
    except Exception as e:
        print(f'Erro ao processar {caminho_imagem} com piexif: {e}')
    return {}

    

def extrair_exif_exifread(caminho_imagem):
    """Extrai os metadados EXIF usando a biblioteca exifread."""
    try:
        with open(caminho_imagem, 'rb') as f:
            tags = exifread.process_file(f)
            return {tag: str(tags[tag]) for tag in tags}
    except Exception as e:
        print(f'Erro ao processar {caminho_imagem} com exifread: {e}')
    return {}

def extrair_exif_exiftool(caminho_imagem):
    """Extrai os metadados EXIF usando o comando exiftool."""
    try:
        processo = subprocess.Popen(['exiftool', '-json', caminho_imagem], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        saida, erro = processo.communicate()
        if saida:
            return json.loads(saida.decode('utf-8'))[0]
    except Exception as e:
        print(f'Erro ao processar {caminho_imagem} com exiftool: {e}')
    return {}

def gravar_exif_csv(dados_exif, nome_arquivo):
    """Grava os dados EXIF em um arquivo CSV."""
    keys = set().union(*(d.keys() for d in dados_exif))
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['caminho_imagem'] + list(keys)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for d in dados_exif:
            writer.writerow(d)

def main():
    pasta_fotos = os.path.join(os.path.dirname(__file__), 'fotos')
    fotos = [os.path.join(pasta_fotos, f) for f in os.listdir(pasta_fotos) if f.endswith(('jpg', 'jpeg', 'png'))]

    dados_exif = {
        'exif_pillow.csv': [extrair_exif_pillow(foto) for foto in fotos],
        'exif_piexif.csv': [extrair_exif_piexif(foto) for foto in fotos],
        'exif_exifread.csv': [extrair_exif_exifread(foto) for foto in fotos],
        'exif_exiftool.csv': [extrair_exif_exiftool(foto) for foto in fotos],
    }

    for nome_arquivo, dados in dados_exif.items():
        dados_com_caminho = [{**d, 'caminho_imagem': foto} for d, foto in zip(dados, fotos)]
        gravar_exif_csv(dados_com_caminho, nome_arquivo)

if __name__ == '__main__':
    main()
