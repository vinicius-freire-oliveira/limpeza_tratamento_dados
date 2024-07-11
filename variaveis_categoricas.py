import pandas as pd                 # Importa a biblioteca pandas para manipulação de dados
import numpy as np                  # Importa a biblioteca numpy para operações numéricas
import matplotlib.pyplot as plt     # Importa matplotlib.pyplot para visualizações gráficas
import json                         # Importa a biblioteca json para trabalhar com arquivos JSON
import seaborn as sns               # Importa seaborn para visualizações estatísticas mais avançadas

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

# Verifica duplicatas no DataFrame filtrado e imprime
print(dados_sem_vazio.duplicated())

# Conta o número de duplicatas no DataFrame filtrado
print(dados_sem_vazio.duplicated().sum())

# Cria uma série booleana indicando as duplicatas no DataFrame filtrado
filtro_duplicadas = dados_sem_vazio.duplicated()
print(filtro_duplicadas)

# Imprime as linhas duplicadas no DataFrame filtrado
print(dados_sem_vazio[filtro_duplicadas])

# Remove as duplicatas do DataFrame filtrado e imprime o número de duplicatas restantes
dados_sem_vazio.drop_duplicates(inplace=True)
print(dados_sem_vazio.duplicated().sum())

# Verifica se há valores nulos no DataFrame filtrado e imprime
print(dados_sem_vazio.isna())

# Conta os valores nulos em cada coluna do DataFrame filtrado e imprime
print(dados_sem_vazio.isna().sum())

# Soma o número total de valores nulos no DataFrame filtrado e imprime
print(dados_sem_vazio.isna().sum().sum())

# Imprime as linhas do DataFrame filtrado que contêm valores nulos
print(dados_sem_vazio[dados_sem_vazio.isna().any(axis=1)])

# Imprime colunas específicas do DataFrame filtrado
print(dados_sem_vazio[['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']])

# Realiza uma operação matemática simples e arredonda para cima o resultado
print(np.ceil(5957.90/90.45))

# Preenche os valores nulos na coluna 'cliente.tempo_servico' com base em um cálculo matemático
dados_sem_vazio['cliente.tempo_servico'].fillna(
    np.ceil(
        dados_sem_vazio['conta.cobranca.Total'] / dados_sem_vazio['conta.cobranca.mensal']
    ), inplace=True
)

# Define um filtro para valores de 'cliente.tempo_servico' maiores que 10
filtro = dados_sem_vazio['cliente.tempo_servico'] > 10

# Imprime colunas específicas do DataFrame filtrado pelo filtro definido
print(dados_sem_vazio[filtro][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']])

# Verifica novamente se há valores nulos no DataFrame filtrado e imprime contagens por coluna
print(dados_sem_vazio.isna().sum())

# Imprime contagens de valores únicos na coluna 'conta.contrato' do DataFrame filtrado
print(dados_sem_vazio['conta.contrato'].value_counts())

# Define uma lista de colunas a serem verificadas quanto a valores nulos e imprime a contagem de linhas com valores nulos
colunas_dropar = ['conta.contrato', 'conta.faturamente_eletronico', 'conta.metodo_pagamento']
print(dados_sem_vazio[colunas_dropar].isna().any(axis=1).sum())

# Cria um novo DataFrame excluindo linhas onde há valores nulos nas colunas especificadas
df_sem_nulo = dados_sem_vazio.dropna(subset=colunas_dropar).copy()
print(df_sem_nulo.head())

# Reinicia o índice do novo DataFrame e imprime o número de valores nulos em cada coluna
df_sem_nulo.reset_index(drop=True, inplace=True)
print(df_sem_nulo.isna().sum())

# Imprime estatísticas descritivas básicas do novo DataFrame
print(df_sem_nulo.describe())

# Cria um boxplot da coluna 'cliente.tempo_servico' do DataFrame df_sem_nulo utilizando seaborn
sns.boxplot(x=df_sem_nulo['cliente.tempo_servico'])

# Exibe o gráfico
plt.show()

# Calcula estatísticas para identificação de outliers na coluna 'cliente.tempo_servico' de df_sem_nulo
Q1 = df_sem_nulo['cliente.tempo_servico'].quantile(.25)
Q3 = df_sem_nulo['cliente.tempo_servico'].quantile(.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

# Cria uma série booleana indicando os outliers na coluna 'cliente.tempo_servico'
outliers_index = (df_sem_nulo['cliente.tempo_servico'] < limite_inferior) | (df_sem_nulo['cliente.tempo_servico'] > limite_superior)
print(outliers_index)

# Imprime os valores dos outliers na coluna 'cliente.tempo_servico'
print(df_sem_nulo[outliers_index]['cliente.tempo_servico'])

# Cria uma cópia do DataFrame df_sem_nulo para manipulação dos outliers
df_sem_out = df_sem_nulo.copy()

# Preenche os valores dos outliers na coluna 'cliente.tempo_servico' com base em outro cálculo matemático
df_sem_out.loc[outliers_index, 'cliente.tempo_servico'] = np.ceil(
    df_sem_out.loc[outliers_index, 'conta.cobranca.Total'] /
    df_sem_out.loc[outliers_index, 'conta.cobranca.mensal']
)

# Cria um novo boxplot da coluna 'cliente.tempo_servico' do DataFrame df_sem_out utilizando seaborn
sns.boxplot(x=df_sem_out['cliente.tempo_servico'])

# Exibe o gráfico
plt.show()

# Imprime as linhas do DataFrame df_sem_out que contêm outliers nas colunas especificadas
print(df_sem_out[outliers_index][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']])

# Imprime os valores ajustados dos outliers na coluna 'cliente.tempo_servico'
print(df_sem_out[outliers_index]['cliente.tempo_servico'])

# Calcula novamente os limites de outlier para a coluna 'cliente.tempo_servico' de df_sem_out
Q1 = df_sem_out['cliente.tempo_servico'].quantile(.25)
Q3 = df_sem_out['cliente.tempo_servico'].quantile(.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

# Cria uma série booleana indicando os outliers atualizados na coluna 'cliente.tempo_servico'
outliers_index = (df_sem_out['cliente.tempo_servico'] < limite_inferior) | (df_sem_out['cliente.tempo_servico'] > limite_superior)
print(outliers_index)

# Imprime as linhas do DataFrame df_sem_out que contêm outliers após a remoção
print(df_sem_out[outliers_index])

# Remove as linhas do DataFrame df_sem_out que contêm outliers
df_sem_out = df_sem_out[~outliers_index]
print(df_sem_out)

# Cria um novo boxplot da coluna 'cliente.tempo_servico' do DataFrame df_sem_out após remoção de outliers
sns.boxplot(x=df_sem_out['cliente.tempo_servico'])

# Exibe o gráfico
plt.show()

# Reinicia o índice do DataFrame df_sem_out e remove a coluna 'id_cliente'
df_sem_id = df_sem_out.drop('id_cliente', axis=1).copy()
print(df_sem_id)

# Define um mapeamento para converter categorias textuais em números binários
mapeamento = {
    'nao': 0,
    'sim': 1,
    'masculino': 0,
    'feminino': 1
}

# Itera sobre as colunas do DataFrame df_sem_id, imprime os valores únicos e aplica o mapeamento
for col in df_sem_id.columns:
    print(f"Coluna: {col}")
    print(df_sem_id[col].unique())
    print("-" * 30)

# Define uma lista de colunas a serem convertidas utilizando o mapeamento
colunas = ['telefone.servico_telefone', 'Churn', 'cliente.parceiro', 'cliente.dependentes', 'conta.faturamente_eletronico', 'cliente.genero']

# Substitui os valores nas colunas especificadas pelo mapeamento
df_sem_id[colunas] = df_sem_id[colunas].replace(mapeamento)
print(df_sem_id)

# Itera novamente sobre as colunas do DataFrame df_sem_id para verificar os valores únicos após substituição
for col in df_sem_id.columns:
    print(f"Coluna: {col}")
    print(df_sem_id[col].unique())
    print("-" * 30)

# Exemplo de criação de uma série com valores 'abca'
s = pd.Series(list('abca'))
print(s)

# Aplica o método get_dummies para criar variáveis dummy de cada categoria na série s
print(pd.get_dummies(s, dtype=int))

# Imprime informações sobre o DataFrame df_sem_id
print(df_sem_id.info())

# Cria variáveis dummy para todas as colunas categóricas do DataFrame df_sem_id e imprime as primeiras linhas
df_dummies = pd.get_dummies(df_sem_id, dtype=int).copy()
print(df_dummies.head())

# Imprime os nomes das colunas do DataFrame df_dummies
print(df_dummies.columns)

# Imprime informações atualizadas sobre o DataFrame df_dummies
print(df_dummies.info())
