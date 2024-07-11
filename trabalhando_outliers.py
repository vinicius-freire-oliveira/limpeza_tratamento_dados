import matplotlib.pyplot as plt    # Importa a biblioteca matplotlib para plotagem
import numpy as np                 # Importa a biblioteca numpy para operações numéricas
import pandas as pd                # Importa a biblioteca pandas para manipulação de dados
import json                        # Importa a biblioteca json para trabalhar com arquivos JSON
import seaborn as sns              # Importa a biblioteca seaborn para visualização estatística

# Abre o arquivo JSON 'dataset-telecon.json' como um arquivo bruto e carrega os dados em json_bruto
with open("dataset-telecon.json") as f:
  json_bruto = json.load(f)

# Imprime o conteúdo bruto do arquivo JSON
print(json_bruto)

# Normaliza os dados do arquivo JSON bruto e carrega em um DataFrame
dados_normalizados = pd.json_normalize(json_bruto)

# Imprime as primeiras linhas do DataFrame normalizado para verificar a estrutura dos dados
print(dados_normalizados.head())

# Imprime informações sobre o DataFrame para verificar os tipos de dados e se há valores nulos
print(dados_normalizados.info())

# Substitui valores vazios ('' e ' ') na coluna 'conta.cobranca.Total' por NaN utilizando numpy
dados_normalizados['conta.cobranca.Total'] = dados_normalizados['conta.cobranca.Total'].replace(['', ' '], np.nan)

# Imprime as primeiras linhas onde a coluna 'conta.cobranca.Total' está vazia
print(dados_normalizados[dados_normalizados['conta.cobranca.Total'] == ' '].head())

# Imprime colunas específicas onde a coluna 'conta.cobranca.Total' está vazia
print(dados_normalizados[dados_normalizados['conta.cobranca.Total'] == ' '][
    ['cliente.tempo_servico', 'conta.contrato', 'conta.cobranca.mensal', 'conta.cobranca.Total']
])

# Obtém os índices onde a coluna 'conta.cobranca.Total' está vazia
idx = dados_normalizados[dados_normalizados['conta.cobranca.Total'] == ' '].index

# Preenche os valores vazios na coluna 'conta.cobranca.Total' com o valor da coluna 'conta.cobranca.mensal' multiplicado por 24
dados_normalizados.loc[idx, "conta.cobranca.Total"] = dados_normalizados.loc[idx, "conta.cobranca.mensal"] * 24

# Preenche os valores na coluna 'cliente.tempo_servico' nos índices onde 'conta.cobranca.Total' estava vazio com 24
dados_normalizados.loc[idx, "cliente.tempo_servico"] = 24

# Imprime colunas específicas onde 'conta.cobranca.Total' estava vazio após preenchimento
print(dados_normalizados.loc[idx][
    ['cliente.tempo_servico', 'conta.contrato', 'conta.cobranca.mensal', 'conta.cobranca.Total']
])

# Converte a coluna 'conta.cobranca.Total' para o tipo float
dados_normalizados['conta.cobranca.Total'] = dados_normalizados['conta.cobranca.Total'].astype(float)

# Imprime informações atualizadas sobre o DataFrame para verificar tipos de dados após conversão
print(dados_normalizados.info())

# Itera sobre todas as colunas do DataFrame para verificar valores únicos e tipagem
for col in dados_normalizados.columns:
    print(f"Coluna: {col}")
    print(dados_normalizados[col].unique())
    print("-" * 30)

# Filtra linhas onde a coluna 'Churn' está vazia ('')
print(dados_normalizados.query("Churn == ''"))

# Filtra e cria um novo DataFrame excluindo linhas onde 'Churn' está vazio ('')
dados_sem_vazio = dados_normalizados[dados_normalizados['Churn'] != ''].copy()

# Imprime informações sobre o novo DataFrame após filtragem
print(dados_sem_vazio.info())

# Reinicia o índice do DataFrame filtrado e imprime o DataFrame
dados_sem_vazio.reset_index(drop=True, inplace=True)
print(dados_sem_vazio)

# Verifica duplicatas no DataFrame e imprime resultados booleanos para cada linha
print(dados_sem_vazio.duplicated())

# Calcula e imprime a quantidade de duplicatas no DataFrame
print(dados_sem_vazio.duplicated().sum())

# Cria uma série booleana para identificar duplicatas no DataFrame
filtro_duplicadas = dados_sem_vazio.duplicated()
print(filtro_duplicadas)

# Imprime linhas duplicadas com base na série booleana
print(dados_sem_vazio[filtro_duplicadas])

# Remove duplicatas do DataFrame original e imprime a quantidade de duplicatas restantes
dados_sem_vazio.drop_duplicates(inplace=True)
print(dados_sem_vazio.duplicated().sum())

# Verifica valores nulos no DataFrame e imprime uma matriz booleana
print(dados_sem_vazio.isna())

# Calcula e imprime a quantidade de valores nulos em cada coluna do DataFrame
print(dados_sem_vazio.isna().sum())

# Calcula e imprime a quantidade total de valores nulos no DataFrame
print(dados_sem_vazio.isna().sum().sum())

# Imprime linhas onde há valores nulos em qualquer coluna do DataFrame
print(dados_sem_vazio[dados_sem_vazio.isna().any(axis=1)])

# Cria um filtro para identificar linhas onde 'cliente.tempo_servico' é nulo
filtro = dados_sem_vazio['cliente.tempo_servico'].isna()

# Imprime linhas onde 'cliente.tempo_servico' é nulo, exibindo colunas específicas
print(dados_sem_vazio[filtro][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']])

# Calcula e imprime o resultado de 5957.90 dividido por 90.45 arredondado para cima usando numpy
print(np.ceil(5957.90/90.45))

# Preenche os valores nulos em 'cliente.tempo_servico' com o resultado do cálculo anterior
dados_sem_vazio['cliente.tempo_servico'].fillna(
    np.ceil(
        dados_sem_vazio['conta.cobranca.Total'] / dados_sem_vazio['conta.cobranca.mensal']
    ), inplace=True
)

# Imprime novamente linhas onde 'cliente.tempo_servico' era nulo, exibindo colunas específicas
print(dados_sem_vazio[filtro][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']])

# Imprime a quantidade de valores nulos em cada coluna do DataFrame após preenchimento
print(dados_sem_vazio.isna().sum())

# Imprime contagem de valores únicos na coluna 'conta.contrato'
print(dados_sem_vazio['conta.contrato'].value_counts())

# Define uma lista de colunas para dropar ('conta.contrato', 'conta.faturamente_eletronico', 'conta.metodo_pagamento')
colunas_dropar = ['conta.contrato', 'conta.faturamente_eletronico', 'conta.metodo_pagamento']

# Calcula e imprime a quantidade de linhas onde pelo menos uma das colunas_dropar é nula
print(dados_sem_vazio[colunas_dropar].isna().any(axis=1).sum())

# Cria um novo DataFrame sem linhas onde pelo menos uma das colunas_dropar é nula e imprime as primeiras linhas
df_sem_nulo = dados_sem_vazio.dropna(subset=colunas_dropar).copy()
print(df_sem_nulo.head())

# Reinicia o índice do novo DataFrame e imprime as primeiras linhas
df_sem_nulo.reset_index(drop=True, inplace=True)
print(df_sem_nulo.head())

# Imprime informações estatísticas do DataFrame sem valores nulos
print(df_sem_nulo.describe())

# Cria um gráfico de caixa (boxplot) para 'cliente.tempo_servico' usando seaborn e matplotlib
sns.boxplot(x=df_sem_nulo['cliente.tempo_servico'])
plt.show()

# Calcula quartis e limites para detecção de outliers
Q1 = df_sem_nulo['cliente.tempo_servico'].quantile(.25)
Q3 = df_sem_nulo['cliente.tempo_servico'].quantile(.75)
IQR = Q3-Q1
limite_inferior = Q1 - 1.5*IQR
limite_superior = Q3 + 1.5*IQR

# Identifica índices dos outliers
outliers_index = (df_sem_nulo['cliente.tempo_servico'] < limite_inferior) | (df_sem_nulo['cliente.tempo_servico'] > limite_superior)
print(outliers_index)

# Imprime os valores dos outliers
print(df_sem_nulo[outliers_index]['cliente.tempo_servico'])

# Cria uma cópia do DataFrame sem outliers
df_sem_out = df_sem_nulo.copy()

# Substitui os valores dos outliers por valores calculados a partir de 'conta.cobranca.Total' e 'conta.cobranca.mensal'
df_sem_out.loc[outliers_index, 'cliente.tempo_servico'] = np.ceil(
    df_sem_out.loc[outliers_index, 'conta.cobranca.Total'] /
    df_sem_out.loc[outliers_index, 'conta.cobranca.mensal']
)

# Plota novamente o gráfico de caixa após remoção e substituição de outliers
sns.boxplot(x=df_sem_out['cliente.tempo_servico'])
plt.show()

# Imprime os dados dos outliers substituídos
print(df_sem_out[outliers_index][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']])

# Imprime os valores dos outliers após substituição
print(df_sem_out[outliers_index]['cliente.tempo_servico'])

# Calcula novamente quartis e limites para detecção de outliers após substituição
Q1 = df_sem_out['cliente.tempo_servico'].quantile(.25)
Q3 = df_sem_out['cliente.tempo_servico'].quantile(.75)
IQR = Q3-Q1
limite_inferior = Q1 - 1.5*IQR
limite_superior = Q3 + 1.5*IQR

# Identifica índices dos novos outliers após substituição
outliers_index = (df_sem_out['cliente.tempo_servico'] < limite_inferior) | (df_sem_out['cliente.tempo_servico'] > limite_superior)
print(outliers_index)

# Imprime linhas do DataFrame com novos outliers identificados
print(df_sem_out[outliers_index])

# Remove os novos outliers do DataFrame
df_sem_out = df_sem_out[~outliers_index]
print(df_sem_out)

# Plota novamente o gráfico de caixa após remoção final de outliers
sns.boxplot(x=df_sem_out['cliente.tempo_servico'])
plt.show()

# Reinicia o índice do DataFrame final sem outliers
df_sem_out.reset_index(drop=True, inplace=True)

# Imprime o DataFrame final sem outliers
print(df_sem_out)
