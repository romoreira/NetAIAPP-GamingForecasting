import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

# Ajustar o tamanho da fonte globalmente
plt.rcParams.update({'font.size': 14})

# Load the data
non_intrusive = pd.read_csv('non_intrusive_measured_latency.csv')
ue_latency = pd.read_csv('ue_latency_probe_log.csv')

# Convert the timestamp columns to datetime
non_intrusive['timestamp'] = pd.to_datetime(non_intrusive['timestamp'])
ue_latency['timestamp'] = pd.to_datetime(ue_latency['timestamp'])

# Merge the dataframes on the nearest timestamp
merged_df = pd.merge_asof(non_intrusive.sort_values('timestamp'), 
                          ue_latency.sort_values('timestamp'), 
                          on='timestamp', 
                          suffixes=('_non_intrusive', '_ue_latency'))

# Extract the latency columns
y_true = merged_df['latency_ue_latency']
y_pred = merged_df['latency_non_intrusive']

# Calculate the MAPE on original values
mape_original = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# Normalize the latency values
y_true_normalized = (y_true - y_true.mean()) / y_true.std()
y_pred_normalized = (y_pred - y_pred.mean()) / y_pred.std()

# Calculate the metrics on normalized values
mse = mean_squared_error(y_true_normalized, y_pred_normalized)
mae = mean_absolute_error(y_true_normalized, y_pred_normalized)
mape_normalized = np.mean(np.abs((y_true_normalized - y_pred_normalized) / y_true_normalized)) * 100
r2 = r2_score(y_true_normalized, y_pred_normalized)

# Print the results
print(f'Mean Squared Error (Normalized): {mse}')
print(f'Mean Absolute Error (Normalized): {mae}')
print(f'Mean Absolute Percentage Error (Normalized): {mape_normalized}')
print(f'R2 Score (Normalized): {r2}')
print(f'Mean Absolute Percentage Error (Original): {mape_original}')

# Create an index for the x-axis
index = np.arange(len(merged_df))

# Scatter Plot
plt.figure(figsize=(14, 5))
plt.scatter(y_true, y_pred, alpha=0.5)
plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--')
plt.xlabel('True Latency', fontsize=16)
plt.ylabel('Estimated Latency', fontsize=16)
#plt.title('Scatter Plot of True vs Predicted Values')
plt.savefig('graphs/scatter_plot.pdf')
plt.close()

# Error Plot
plt.figure(figsize=(14, 5))
plt.plot(index, y_true - y_pred, alpha=0.5)
plt.xlabel('Index')
plt.ylabel('Error')
plt.title('Error Plot')
plt.savefig('graphs/error_plot.pdf')
plt.close()

# Histogram of Errors
plt.figure(figsize=(10, 5))
plt.hist(y_true - y_pred, bins=50, alpha=0.5)
#plt.xlabel('Error')
plt.ylabel('Frequency', fontsize=16)
#plt.title('Histogram of Errors')
plt.savefig('graphs/histogram_of_errors.pdf')
plt.close()

# Time Series Plot
plt.figure(figsize=(14, 5))
plt.plot(index, y_true, label='True Values', alpha=0.5)
plt.plot(index, y_pred, label='Predicted Values', alpha=0.5)
plt.xlabel('Index')
plt.ylabel('Latency')
plt.title('Time Series Plot')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=14)
plt.savefig('graphs/time_series_plot.pdf')
plt.close()

# Sample 240 items for the combined line plot
sample_size = 30
sample_indices = np.linspace(0, len(merged_df) - 1, sample_size, dtype=int)
sample_index = np.arange(sample_size)
sample_y_true_normalized = y_true_normalized.iloc[sample_indices]
sample_y_pred_normalized = y_pred_normalized.iloc[sample_indices]

plt.figure(figsize=(14, 5))
plt.plot(sample_index, sample_y_true_normalized, label='True Latency', alpha=0.5, marker='o', markersize=8, linewidth=2)
plt.plot(sample_index, sample_y_pred_normalized, label='Estimated Latency', alpha=0.5, marker='x', markersize=8, linewidth=4)

# Ajustar limites do eixo Y (aumentando o espaço superior)
y_min, y_max = min(sample_y_true_normalized.min(), sample_y_pred_normalized.min()), max(sample_y_true_normalized.max(), sample_y_pred_normalized.max())
plt.ylim(y_min, y_max + 0.4 * (y_max - y_min))  # Adiciona 10% de espaço acima do maior valor

#plt.xlabel('Index')
plt.ylabel('Normalized Latency', fontsize=17)
#plt.title('Real vs Estimated')

# Colocar a legenda dentro do gráfico no canto superior direito
plt.legend(loc='upper right', fontsize=16, frameon=True)

plt.grid(True, linestyle='--', alpha=0.2)
plt.tight_layout()
plt.savefig('graphs/combined_line_plot_normalized.pdf')
plt.close()



#========SERVER LATENCY Experiment=============

# Carregar os dados
server_latency = pd.read_csv('server_latency_record.csv')

# Converter a coluna de timestamp para datetime
server_latency['timestamp'] = pd.to_datetime(server_latency['timestamp'])

# Normalizar os valores de latência
latency_normalized = (server_latency['latency_ms'] - server_latency['latency_ms'].mean()) / server_latency['latency_ms'].std()

# Criar um índice numérico para o eixo x
index = np.arange(len(server_latency))

# Plotar a série temporal normalizada
plt.figure(figsize=(14, 5))
plt.plot(index, latency_normalized, label='Server Latency (Normalized)', alpha=0.7)
plt.xlabel('Index')
plt.ylabel('Normalized Latency')
plt.title('Normalized Server Latency Over Time')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('graphs/server_latency_plot_normalized.pdf')
plt.close()