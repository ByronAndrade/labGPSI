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

# Converter 'Data e Hora' para datetime
# O formato de data nos seus dados é 'AAAA:MM:DD HH:MM:SS'
df_fotos['Data e Hora'] = pd.to_datetime(df_fotos['Data e Hora'], format='%Y:%m:%d %H:%M:%S', errors='coerce')
df_fotos_de_fotos['Data e Hora'] = pd.to_datetime(df_fotos_de_fotos['Data e Hora'], format='%Y:%m:%d %H:%M:%S', errors='coerce')

# One-Hot Encoding para 'Modelo da Câmera'
encoder = OneHotEncoder()  # Removido o argumento sparse=False
encoder.fit(pd.concat([df_fotos[['Modelo da Câmera']], df_fotos_de_fotos[['Modelo da Câmera']]]))

# Transformar e adicionar ao DataFrame
for df in [df_fotos, df_fotos_de_fotos]:
    modelos_camera_encoded = encoder.transform(df[['Modelo da Câmera']]).toarray()  # Assegura a conversão para array denso
    for i, category in enumerate(encoder.categories_[0]):
        df[f'Modelo_{category}'] = modelos_camera_encoded[:, i]


# Normalização/Padronização de campos numéricos
scaler = StandardScaler()
# Atualize esta lista com as colunas numéricas que realmente existem no seu DataFrame
num_fields = ['ISO', 'Abertura', 'Distância Focal']  # 'Brilho' foi removido pois não está presente nos dados fornecidos
# Fit no conjunto de fotos originais
scaler.fit(df_fotos[num_fields])

# Transformar ambos os conjuntos
df_fotos[num_fields] = scaler.transform(df_fotos[num_fields])
df_fotos_de_fotos[num_fields] = scaler.transform(df_fotos_de_fotos[num_fields])

# Imputação de valores ausentes para campos numéricos (opcional)
imputer = SimpleImputer(strategy='mean')
df_fotos[num_fields] = imputer.fit_transform(df_fotos[num_fields])
df_fotos_de_fotos[num_fields] = imputer.transform(df_fotos_de_fotos[num_fields])

# Os DataFrames agora estão preparados para análise e comparação

# Salvar os DataFrames pré-processados como novos arquivos CSV usando caminhos relativos
caminho_salvar_fotos = os.path.join(diretorio_atual, 'fotos_preprocessadas.csv')
caminho_salvar_fotos_de_fotos = os.path.join(diretorio_atual, 'fotos_de_fotos_preprocessadas.csv')

df_fotos.to_csv(caminho_salvar_fotos, index=False)
df_fotos_de_fotos.to_csv(caminho_salvar_fotos_de_fotos, index=False)
