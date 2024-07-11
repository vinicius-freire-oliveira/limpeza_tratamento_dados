import pandas as pd  # Importa a biblioteca pandas
import numpy as np   # Importa a biblioteca numpy
import json          # Importa a biblioteca json
import matplotlib.pyplot as plt  # Importa o módulo pyplot da biblioteca matplotlib

# Imprime a versão do pandas que está sendo utilizada
print(pd.__version__)

# Lê o arquivo JSON 'dataset-telecon.json' e carrega os dados em um DataFrame
dados_churn = pd.read_json('dataset-telecon.json')

# Imprime as primeiras linhas do DataFrame para verificar a leitura correta
print(dados_churn.head())

# Acessa o valor da primeira linha da coluna 'conta' e imprime na tela
print(dados_churn['conta'][0])

# Normaliza a coluna 'conta' do DataFrame e imprime as primeiras linhas da normalização
print(pd.json_normalize(dados_churn['conta']).head())

# Normaliza a coluna 'telefone' do DataFrame e imprime as primeiras linhas da normalização
print(pd.json_normalize(dados_churn['telefone']).head())

# Abre o arquivo JSON 'dataset-telecon.json' como um arquivo bruto e carrega os dados em json_bruto
with open("dataset-telecon.json") as f:
    json_bruto = json.load(f)

# Imprime o conteúdo bruto do arquivo JSON
print(json_bruto)

# Normaliza os dados do arquivo JSON bruto e carrega em um DataFrame
dados_normalizados = pd.json_normalize(json_bruto)

# Imprime as primeiras linhas do DataFrame normalizado
print(dados_normalizados.head())
