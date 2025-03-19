#!/bin/bash

# Interface de rede do POD1
INTERFACE="eth0"

# Parâmetros da latência sinusoidal
MAX_DELAY=200   # Latência máxima em ms
MIN_DELAY=50    # Latência mínima em ms
INTERVAL=1      # Intervalo de atualização em segundos
PERIOD=30       # Período da onda em segundos (tempo para completar um ciclo)

# Loop para ajustar dinamicamente a latência
while true; do
    # Tempo atual em segundos
    CURRENT_TIME=$(date +%s)

    # Calcula a latência baseada na função sinusoidal
    SIN_VALUE=$(awk -v t=$CURRENT_TIME -v p=$PERIOD 'BEGIN { print sin(2 * 3.14159 * t / p) }')
    CURRENT_DELAY=$(awk -v max=$MAX_DELAY -v min=$MIN_DELAY -v sin_val=$SIN_VALUE \
        'BEGIN { print (max - min) / 2 * (sin_val + 1) + min }')

    # Aplica a nova latência
    tc qdisc replace dev "$INTERFACE" root netem delay "${CURRENT_DELAY}ms"

    echo "Latência aplicada: ${CURRENT_DELAY}ms"

    # Aguarda o próximo intervalo
    sleep $INTERVAL
done

