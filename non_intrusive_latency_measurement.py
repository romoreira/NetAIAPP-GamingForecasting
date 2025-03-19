import subprocess

# Configuração do comando tshark
interface = "veth491ff7b7"
command = [
    "sudo", "tshark", "-i", interface, "-Y", "gtp && icmp", "-T", "fields",
    "-e", "frame.time_relative", "-e", "icmp.type", "-e", "gtp.teid", "-l"
]

def calcular_latencia_por_teid():
    try:
        print(f"Executando comando: {' '.join(command)}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        icmp_requests = {}  # Dicionário para armazenar os tempos de envio por TEID
        latencias = {}  # Dicionário para armazenar as latências calculadas por TEID

        print("Capturando pacotes... Pressione Ctrl+C para parar.")
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
                    if teid not in latencias:
                        latencias[teid] = []
                    latencias[teid].append(latency)
                    print(f"TEID {teid} - Measured Latency: {latency:.3f} ms")  # Exibe a latência em ms

        # Calcula a média da latência por TEID
        if latencias:
            for teid, latencias_teid in latencias.items():
                media_latencia = sum(latencias_teid) / len(latencias_teid)
                print(f"\nMédia da latência para TEID {teid}: {media_latencia:.3f} ms")  # Exibe a média em ms
        else:
            print("\nNenhuma latência calculada. Pode não haver pacotes ICMP reply suficientes.")

    except KeyboardInterrupt:
        print("\nFinalizando a captura...")

# Chama a função para calcular a latência por TEID
calcular_latencia_por_teid()

