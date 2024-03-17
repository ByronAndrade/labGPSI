import os
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

# Caminho para o diretório onde o script está sendo executado
diretorio_atual = os.path.dirname(os.path.realpath(__file__))

# Construir caminhos para os arquivos CSV
caminho_fotos = os.path.join(diretorio_atual, 'fotos_exif.csv')
caminho_fotos_de_fotos = os.path.join(diretorio_atual, 'fotos_de_fotos_exif.csv')

# Carregar os dados
df_fotos = pd.read_csv(caminho_fotos)
df_fotos_de_fotos = pd.read_csv(caminho_fotos_de_fotos)

# Converter 'Data e Hora' para datetime, facilitando análises temporais
df_fotos['Data e Hora'] = pd.to_datetime(df_fotos['Data e Hora'], format='%Y:%m:%d %H:%M:%S', errors='coerce')
df_fotos_de_fotos['Data e Hora'] = pd.to_datetime(df_fotos_de_fotos['Data e Hora'], format='%Y:%m:%d %H:%M:%S', errors='coerce')

# One-Hot Encoding para 'Modelo da Câmera', convertendo categorias em representação numérica
encoder = OneHotEncoder()
encoder.fit(pd.concat([df_fotos[['Modelo da Câmera']], df_fotos_de_fotos[['Modelo da Câmera']]]))

# Transformar e adicionar ao DataFrame as colunas one-hot encoded
for df in [df_fotos, df_fotos_de_fotos]:
    modelos_camera_encoded = encoder.transform(df[['Modelo da Câmera']]).toarray()  # Conversão para array denso
    for i, category in enumerate(encoder.categories_[0]):
        df[f'Modelo_{category}'] = modelos_camera_encoded[:, i]

# Normalização/Padronização de campos numéricos para trazer os dados para uma escala comum
scaler = StandardScaler()
num_fields = ['ISO', 'Abertura', 'Distância Focal']
scaler.fit(df_fotos[num_fields])  # Ajuste usando o conjunto de fotos originais

# Transformar ambos os conjuntos de dados
df_fotos[num_fields] = scaler.transform(df_fotos[num_fields])
df_fotos_de_fotos[num_fields] = scaler.transform(df_fotos_de_fotos[num_fields])

# Imputação de valores ausentes para campos numéricos com a média da coluna
imputer = SimpleImputer(strategy='mean')
df_fotos[num_fields] = imputer.fit_transform(df_fotos[num_fields])
df_fotos_de_fotos[num_fields] = imputer.transform(df_fotos_de_fotos[num_fields])

# Salvando os DataFrames preprocessados como novos arquivos CSV
caminho_salvar_fotos = os.path.join(diretorio_atual, 'fotos_preprocessadas.csv')
caminho_salvar_fotos_de_fotos = os.path.join(diretorio_atual, 'fotos_de_fotos_preprocessadas.csv')

df_fotos.to_csv(caminho_salvar_fotos, index=False)
df_fotos_de_fotos.to_csv(caminho_salvar_fotos_de_fotos, index=False)
