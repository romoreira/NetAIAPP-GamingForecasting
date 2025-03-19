import subprocess
import csv
from datetime import datetime

# Configuração do comando tshark
interface = "veth491ff7b7"
command = [
    "sudo", "tshark", "-i", interface, "-Y", "gtp && icmp", "-T", "fields",
    "-e", "frame.time_relative", "-e", "icmp.type", "-e", "gtp.teid", "-l"
]

# Nome do arquivo CSV
csv_file = "latency_log.csv"

# Cria o arquivo CSV e adiciona o cabeçalho
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "teid", "latency_ms"])

def calcular_latencia_por_teid():
    try:
        print(f"Executando comando: {' '.join(command)}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        icmp_requests = {}  # Dicionário para armazenar os tempos de envio por TEID
        print("Capturando pacotes... Pressione Ctrl+C para parar.")

        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)

            for line in process.stdout:
                line = line.strip()
                if not line:
                    continue

                # Divide a linha em tempo relativo, tipo ICMP e TEID
                campos = line.split()
                if len(campos) != 3:
                    continue

                time_relative = float(campos[0])
                icmp_type = int(campos[1])
                teid = campos[2]

                # Se for um ICMP request (tipo 8), armazene o tempo associado ao TEID
                if icmp_type == 8:  # Echo request
                    if teid not in icmp_requests:
                        icmp_requests[teid] = []
                    icmp_requests[teid].append(time_relative)
                elif icmp_type == 0:  # Echo reply
                    if teid in icmp_requests and icmp_requests[teid]:
                        # Associa o último request com o reply para o TEID correspondente
                        request_time = icmp_requests[teid].pop(0)
                        latency = (time_relative - request_time) * 1000  # Converte para milissegundos
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        writer.writerow([timestamp, teid, latency])
                        print(f"TEID {teid} - Measured Latency: {latency:.3f} ms")  # Exibe a latência em ms

    except KeyboardInterrupt:
        print("\nFinalizando a captura...")

# Chama a função para calcular a latência por TEID
calcular_latencia_por_teid()

