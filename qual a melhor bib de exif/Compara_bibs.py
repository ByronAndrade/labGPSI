import pandas as pd
import os

# Obtendo o diretório do script atual
diretorio_script = os.path.dirname(os.path.abspath(__file__))

# Definindo os nomes dos arquivos CSV de origem
arquivos = {
    'Pillow': 'exif_pillow.csv',
    'ExifRead': 'exif_exifread.csv',
    'Piexif': 'exif_piexif.csv',
    'ExifTool': 'exif_exiftool.csv'
}

def carregar_dados(arquivos):
    dados = {}
    for biblioteca, arquivo in arquivos.items():
        caminho_completo = os.path.join(diretorio_script, arquivo)
        try:
            df = pd.read_csv(caminho_completo)
            # Normaliza os nomes das colunas para garantir consistência
            df.columns = [col.strip().title() for col in df.columns]
            if 'Caminho_Imagem' not in df.columns:
                raise ValueError(f"O arquivo {arquivo} não contém a coluna 'Caminho_Imagem'.")
            dados[biblioteca] = df
        except FileNotFoundError:
            print(f'Erro: Arquivo {arquivo} não encontrado.')
        except pd.errors.EmptyDataError:
            print(f'Erro: Arquivo {arquivo} está vazio ou malformado.')
        except ValueError as e:
            print(e)
    return dados

def processar_e_gerar_relatorios(dados):
    # Inicializa o DataFrame final com as colunas 'Caminho_Imagem'
    tags_unicas = pd.DataFrame(columns=['Caminho_Imagem'])
    sufixo = 1  # Para colunas duplicadas

    for biblioteca, df in dados.items():
        # Renomeia colunas para evitar conflitos
        df_renomeado = df.rename(columns={col: f"{col}_{biblioteca}" for col in df.columns if col != 'Caminho_Imagem'})

        # Merge dos dados, combinando pela coluna 'Caminho_Imagem'
        if tags_unicas.empty:
            tags_unicas = df_renomeado
        else:
            tags_unicas = pd.merge(tags_unicas, df_renomeado, on='Caminho_Imagem', how='outer')

    # Identificar diferenças
    colunas_imagem = [col for col in tags_unicas.columns if col != 'Caminho_Imagem']
    diferencas = []
    for _, row in tags_unicas.iterrows():
        diferencas_row = {}
        for col in colunas_imagem:
            valor = row[col]
            if pd.notnull(valor):
                if col in diferencas_row:
                    if diferencas_row[col] != valor:
                        diferencas_row[col] = 'Diferente'
                else:
                    diferencas_row[col] = valor
        diferencas.append(diferencas_row)
    
    tags_unicas_diferencas = pd.DataFrame(diferencas)
    tags_unicas_diferencas.insert(0, 'Caminho_Imagem', tags_unicas['Caminho_Imagem'])

    # Geração do CSV detalhado com todas as informações
    tags_unicas.to_csv('comparacao_detalhada.csv', index=False)
    tags_unicas_diferencas.to_csv('diferencas_detalhadas.csv', index=False)

if __name__ == "__main__":
    dados = carregar_dados(arquivos)
    if dados:  # Verifica se algum dado foi carregado antes de prosseguir
        processar_e_gerar_relatorios(dados)
