import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np  # Importando o numpy para possíveis transformações

# Definir estilos para os gráficos
sns.set(style="whitegrid")

def carregar_e_combinar_dados(caminho_fotos, caminho_fotos_de_fotos):
    # Carrega os dados
    df_fotos = pd.read_csv(caminho_fotos)
    df_fotos_de_fotos = pd.read_csv(caminho_fotos_de_fotos)
    
    # Adiciona uma coluna para identificar o tipo
    df_fotos['Tipo'] = 'Original'
    df_fotos_de_fotos['Tipo'] = 'Foto de Foto'
    
    # Combina os dois DataFrames
    return pd.concat([df_fotos, df_fotos_de_fotos], ignore_index=True)

def plotar_distribuicao_caracteristicas(df, caracteristicas_exif):
    for caracteristica in caracteristicas_exif:
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x=caracteristica, hue='Tipo', kde=True, element="step", stat="density", common_norm=False)
        plt.title(f'Distribuição de {caracteristica}')
        plt.xlabel(caracteristica)
        plt.ylabel('Densidade')
        plt.legend()
        plt.show()

def plotar_boxplots(df, caracteristicas_exif):
    for caracteristica in caracteristicas_exif:
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='Tipo', y=caracteristica)
        plt.title(f'Boxplot de {caracteristica}')
        plt.show()

def plotar_dispersao(df, x, y):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=x, y=y, hue='Tipo', style='Tipo', alpha=0.7)
    plt.title(f'Relação entre {x} e {y}')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()

def verificar_arquivo(caminho):
    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {caminho}")
        return False
    return True

def main():
    diretorio_atual = os.getcwd()
    caminho_fotos = os.path.join(diretorio_atual, 'fotos_preprocessadas.csv')
    caminho_fotos_de_fotos = os.path.join(diretorio_atual, 'fotos_de_fotos_preprocessadas.csv')

    # Verifica se os arquivos existem antes de proceder
    if not verificar_arquivo(caminho_fotos) or not verificar_arquivo(caminho_fotos_de_fotos):
        return  # Encerra a execução se algum arquivo não for encontrado

    df = carregar_e_combinar_dados(caminho_fotos, caminho_fotos_de_fotos)

    caracteristicas_exif = ['ISO', 'Abertura', 'Distância Focal']
    plotar_distribuicao_caracteristicas(df, caracteristicas_exif)
    plotar_boxplots(df, caracteristicas_exif)
    plotar_dispersao(df, 'ISO', 'Abertura')

if __name__ == "__main__":
    main()
