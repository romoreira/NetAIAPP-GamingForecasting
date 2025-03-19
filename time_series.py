import pandas as pd
import matplotlib.pyplot as plt

# Carregar o CSV
data = pd.read_csv('filtered_gaming_data.csv')

# Converter a coluna de tempo para datetime
data['Time'] = pd.to_datetime(data['Time'], format='%Y-%m-%d %H:%M:%S')

# Ordenar os dados pelo tempo para garantir sequência correta
data = data.sort_values(by=['Time'])

# Criar um índice sequencial baseado no tempo para cada localidade
data['Time_Index'] = data.groupby(['Country', 'Region', 'City']).cumcount()

# Agrupar os dados por localidade
localidades = data.groupby(['Country', 'Region', 'City'])

# Criar o gráfico para cada localidade
for nome, grupo in localidades:
    plt.figure(figsize=(12, 6))
    
    # Plotar RTT médio ao longo do tempo usando o índice sequencial
    plt.plot(grupo['Time_Index'], grupo['RTT_mean'], marker='o', linestyle='-', label='RTT Mean')

    # Configurar rótulos e título
    plt.xlabel('Sequência Temporal (segundos dentro do dia)')
    plt.ylabel('RTT Mean (ms)')
    plt.title(f'Evolução do RTT Médio - {nome[2]}, {nome[1]}, {nome[0]}')
    plt.legend()
    plt.grid(True)
    
    # Melhorar a visualização
    plt.tight_layout()

    # Salvar o gráfico (opcional)
    plt.savefig(f'time_series_{nome[2]}_{nome[1]}_{nome[0]}.png')

    # Exibir o gráfico
    plt.show()
