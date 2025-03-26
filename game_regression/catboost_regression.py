import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Verificar se o arquivo CSV já existe
csv_path = '../subset.csv'
excel_path = '../planilha_final_jogos_global.xlsx'

if not os.path.exists(csv_path):
    # Carregar o arquivo Excel e transformar em CSV
    df_subset = pd.read_excel(excel_path)
    df_subset.to_csv(csv_path, index=False)
    print("Arquivo CSV gerado com sucesso.")
else:
    print("Arquivo CSV já existe. Nenhuma ação necessária.")

# Carregar os dados do CSV
#df = pd.read_csv(csv_path)
df = pd.read_csv('../merged_gaming_data.csv')

# Visualizar as primeiras linhas
print("Dados carregados:")
print(df.head())

# Selecionar apenas colunas numéricas relevantes
numeric_columns = ['RTT', 'Length', 'Longitude', 'Latitude']
df_numeric = df[numeric_columns]

# Separar os dados em treino e teste
X = df_numeric.drop('RTT', axis=1)  # Recursos (features)
y = df_numeric['RTT']              # Target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo com CatBoostRegressor
catboost_model = CatBoostRegressor(verbose=0, random_seed=42)  # verbose=0 para evitar saída longa
catboost_model.fit(X_train, y_train)

# Fazer previsões
y_pred = catboost_model.predict(X_test)

# Calcular as métricas
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
mae_normalizado = mae / (y_test.max() - y_test.min())

# Exibir os resultados
print(f"R² Score: {r2:.2f}")
print(f"MAPE: {mape:.2f}%")
print(f"MSE: {mse:.2f}")
print(f"MAE Normalizado: {mae_normalizado:.2f}")


# Salvar métricas em um arquivo .txt
output_path = 'resultados_metricas.txt'

with open(output_path, 'w') as f:
    f.write(f"R² Score: {r2:.2f}\n")
    f.write(f"MAPE: {mape:.2f}%\n")
    f.write(f"MSE: {mse:.2f}\n")
    f.write(f"MAE Normalizado: {mae_normalizado:.2f}\n")

print(f"Métricas salvas em: {output_path}")