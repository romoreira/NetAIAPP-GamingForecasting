#!/bin/bash

# Nome do arquivo CSV
OUTPUT_FILE="latency_log.csv"

# Cabeçalho do arquivo CSV
echo "timestamp,latency" > "$OUTPUT_FILE"

# Realiza o ping e processa a saída
ping -I uesimtun0 20.42.98.166 | while read -r line; do
    if [[ $line =~ time=([0-9.]+) ]]; then
        LATENCY=${BASH_REMATCH[1]}
        TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
        echo "$TIMESTAMP,$LATENCY" >> "$OUTPUT_FILE"
    fi
done

