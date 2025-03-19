#!/bin/bash

# Interface de rede do POD1
INTERFACE="eth0"

# Parâmetros da latência sinusoidal
MAX_DELAY=600   # Latência máxima em ms
MIN_DELAY=1    # Latência mínima em ms
INTERVAL=1      # Intervalo de atualização em segundos
PERIOD=30       # Período da onda em segundos (tempo para completar um ciclo)
CSV_FILE="latency_log.csv"

# Função para restaurar a interface e remover a latência ao sair
cleanup() {
    echo "Removendo a latência e restaurando a configuração da interface..."
    tc qdisc del dev "$INTERFACE" root 2>/dev/null
    echo "Latência removida. Encerrando o script."
    exit 0
}

# Captura sinais de interrupção (Ctrl+C, kill, etc.)
trap cleanup SIGINT SIGTERM

# Cria o arquivo CSV e adiciona o cabeçalho, se ainda não existir
if [ ! -f "$CSV_FILE" ]; then
    echo "timestamp,latency_ms" > "$CSV_FILE"
fi

# Loop para ajustar dinamicamente a latência
while true; do
    # Tempo atual em segundos e em formato legível
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

    # Calcula a latência baseada na função sinusoidal
    SIN_VALUE=$(awk -v t=$(date +%s) -v p=$PERIOD 'BEGIN { print sin(2 * 3.14159 * t / p) }')
    CURRENT_DELAY=$(awk -v max=$MAX_DELAY -v min=$MIN_DELAY -v sin_val=$SIN_VALUE \
        'BEGIN { print (max - min) / 2 * (sin_val + 1) + min }')

    # Aplica a nova latência
    tc qdisc replace dev "$INTERFACE" root netem delay "${CURRENT_DELAY}ms"

    # Salva a latência no arquivo CSV
    echo "$TIMESTAMP,$CURRENT_DELAY" >> "$CSV_FILE"

    echo "[$TIMESTAMP] Latência aplicada: ${CURRENT_DELAY}ms"

    # Aguarda o próximo intervalo
    sleep $INTERVAL
done
