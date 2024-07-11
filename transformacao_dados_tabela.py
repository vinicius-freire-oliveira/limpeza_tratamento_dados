import pandas as pd                 # Importa a biblioteca pandas para manipulação de dados
import numpy as np                  # Importa a biblioteca numpy para operações numéricas
import json                         # Importa a biblioteca json para trabalhar com arquivos JSON

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
