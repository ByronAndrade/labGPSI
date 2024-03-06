import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define o caminho para o diretório onde o script está sendo executado
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Constrói caminhos para os arquivos CSV
caminho_fotos = os.path.join(diretorio_atual, 'fotos_preprocessadas.csv')
caminho_fotos_de_fotos = os.path.join(diretorio_atual, 'fotos_de_fotos_preprocessadas.csv')

# Carrega os dados
df_fotos = pd.read_csv(caminho_fotos)
df_fotos_de_fotos = pd.read_csv(caminho_fotos_de_fotos)

# Análise Exploratória de Dados (EDA)
print("Descrição das Fotos Originais:")
print(df_fotos.describe())
print("\nDescrição das Fotos de Fotos:")
print(df_fotos_de_fotos.describe())

# Comparar a distribuição de características EXIF usando gráficos
caracteristicas_exif = ['ISO', 'Abertura', 'Distância Focal']

for caracteristica in caracteristicas_exif:
    plt.figure(figsize=(10, 6))
    sns.histplot(df_fotos[caracteristica], color='blue', kde=True, label='Fotos Originais', element="step", stat="density", common_norm=False)
    sns.histplot(df_fotos_de_fotos[caracteristica], color='red', kde=True, label='Fotos de Fotos', element="step", stat="density", common_norm=False)
    plt.title(f'Distribuição de {caracteristica}')
    plt.legend()
    plt.xlabel(caracteristica)
    plt.ylabel('Densidade')
    plt.show()


# Boxplots para comparação das características EXIF
for caracteristica in caracteristicas_exif:
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=pd.concat([df_fotos.assign(Tipo='Original'), df_fotos_de_fotos.assign(Tipo='Foto de Foto')]), 
                x='Tipo', y=caracteristica)
    plt.title(f'Boxplot de {caracteristica}')
    plt.show()

# Gráficos de dispersão para explorar relações entre pares de características
# Como exemplo, vamos explorar a relação entre ISO e Abertura
plt.figure(figsize=(10, 6))
sns.scatterplot(data=pd.concat([df_fotos.assign(Tipo='Original'), df_fotos_de_fotos.assign(Tipo='Foto de Foto')]),
                x='ISO', y='Abertura', hue='Tipo', style='Tipo', alpha=0.7)
plt.title('Relação entre ISO e Abertura')
plt.xlabel('ISO')
plt.ylabel('Abertura')
plt.show()
