import os
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Verificar se o arquivo CSV já existe
csv_path = '../subset.csv'
excel_path = '../planilha_final_jogos_global.xlsx'

if not os.path.exists(csv_path):
    # Carregar o arquivo Excel e transformar em CSV
    df_subset = pd.read_excel(excel_path)
    # Salvar como CSV
    df_subset.to_csv(csv_path, index=False)
    print("Arquivo CSV gerado com sucesso.")
else:
    print("Arquivo CSV já existe. Nenhuma ação necessária.")

# Carregar os dados do CSV
df = pd.read_csv(csv_path)

# Visualizar as primeiras linhas
print("Dados carregados:")
print(df.head())
print(df.columns())

# Using RF I want to forecast (regression) the RTT of the dataset game
# The target variable is the RTT
# The features are the other columns

# Separar os dados em features e target
X = df.drop(columns=['RTT'])
y = df['RTT']
