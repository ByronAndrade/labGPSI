import pandas as pd

def valor_numerico(valor):
    try:
        return float(valor)
    except ValueError:
        return None

def comparar_valores(valor1, valor2):
    num1 = valor_numerico(valor1)
    num2 = valor_numerico(valor2)
    if num1 is not None and num2 is not None:
        return num1 - num2  # Retorna a diferença se ambos os valores são numéricos
    else:
        return 'Diferente' if valor1 != valor2 else 'Igual'  # Compara como strings

def comparar_exifs_e_subtrair(csv_1, csv_2, csv_saida):
    df1 = pd.read_csv(csv_1)
    df2 = pd.read_csv(csv_2)

    # Garantir que as colunas de valor sejam strings para evitar problemas de leitura
    df1['Valor'] = df1['Valor'].astype(str)
    df2['Valor'] = df2['Valor'].astype(str)

    df_merged = pd.merge(df1, df2, on=["Imagem", "Tag"], suffixes=('_1', '_2'), how='outer')
    df_merged['Comparacao'] = df_merged.apply(lambda row: comparar_valores(row['Valor_1'], row['Valor_2']), axis=1)
    
    df_merged.to_csv(csv_saida, index=False)  # Grava o resultado no novo arquivo CSV

# Exemplo de uso
comparar_exifs_e_subtrair('dados_exif_1.csv', 'dados_exif_2.csv', 'resultado_comparacao_exif.csv')
