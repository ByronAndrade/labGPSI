import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração inicial do Seaborn
sns.set(style="whitegrid")

# Funções auxiliares
def extrair_nome_tag(col):
    """Extrai o nome da tag de uma coluna, removendo a referência à biblioteca."""
    if '_' in col:
        return '_'.join(col.split('_')[:-1])
    return col

def analisar_tags_exclusivas(detalhes):
    """Analisa e retorna as tags exclusivas de cada biblioteca."""
    tags_bibliotecas = {}
    for col in detalhes.columns:
        if col == 'Caminho_Imagem':
            continue
        biblioteca = col.split('_')[-1]
        tag = extrair_nome_tag(col)
        tags_bibliotecas.setdefault(biblioteca, set()).add(tag)
    exclusivas = {bib: tags.difference(set.union(*(tags_bibliotecas[b] for b in tags_bibliotecas if b != bib))) for bib, tags in tags_bibliotecas.items()}
    return exclusivas

def verificar_consistencia(row):
    """Verifica se todos os valores não nulos na linha são iguais."""
    valores_unicos = set(row.dropna().unique())
    return len(valores_unicos) == 1 if valores_unicos else False
    
# Função auxiliar para extrair as tags exclusivas e interseções
def analisar_exclusividade_e_intersecao(detalhes):
    # Separando os nomes das colunas por biblioteca
    colunas_por_bib = {bib: [col for col in detalhes if col.endswith(bib)] for bib in ['Pillow', 'ExifRead', 'Piexif', 'ExifTool']}
    tags_por_bib = {bib: set(map(extrair_nome_tag, cols)) for bib, cols in colunas_por_bib.items()}
    
    # Encontrando tags exclusivas
    exclusivas = {bib: tags.difference(set.union(*(tags_por_bib[b] for b in tags_por_bib if b != bib))) for bib, tags in tags_por_bib.items()}
    
    # Encontrando a interseção (tags comuns entre todas as bibliotecas)
    intersecao = set.intersection(*tags_por_bib.values())
    bib_com_maior_intersecao = max(tags_por_bib, key=lambda bib: len(tags_por_bib[bib].intersection(intersecao)))
    
    return exclusivas, bib_com_maior_intersecao
    
    
# Função auxiliar para extrair o nome da tag
def extrair_nome_tag(col):
    return '_'.join(col.split('_')[:-1])

# Carregamento dos dados
detalhes = pd.read_csv('comparacao_detalhada.csv')

# Análise
tags_exclusivas = analisar_tags_exclusivas(detalhes)
detalhes_sem_imagem = detalhes.drop('Caminho_Imagem', axis=1)
consistencia_tags = detalhes_sem_imagem.apply(verificar_consistencia)
tags_consistentes = consistencia_tags[consistencia_tags].index.tolist()
frequencia_tags = detalhes_sem_imagem.notnull().sum().sort_values(ascending=False)
variabilidade_tags = detalhes_sem_imagem.nunique().sort_values(ascending=False)

exclusivas, bib_com_maior_intersecao = analisar_exclusividade_e_intersecao(detalhes)

# Visualizações e Resultados
plt.figure(figsize=(10, 6))
sns.barplot(x=list(tags_exclusivas.keys()), y=[len(tags) for tags in tags_exclusivas.values()])
plt.title('Quantidade de Tags EXIF Únicas por Biblioteca')
plt.xlabel('Biblioteca')
plt.ylabel('Quantidade de Tags Únicas')
plt.show()

print("Frequência das Tags (Top 10):")
print(frequencia_tags.head(10))
print("\nTags com o mesmo valor nas 4 bibliotecas:")
print(tags_consistentes)
print("\nVariabilidade dos Valores das Tags (Top 10):")
print(variabilidade_tags.head(10))

# Imprimindo as tags únicas por biblioteca
for bib, tags in exclusivas.items():
    print(f"Tags únicas de {bib}: {', '.join(sorted(tags)) if tags else 'Nenhuma'}")

print(f"\nBiblioteca com a maior interseção de EXIFs: {bib_com_maior_intersecao}")