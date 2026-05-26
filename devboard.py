import tkinter as tk
from tkinter import ttk
import psutil


# =========================
# Janela principal
# =========================

janela = tk.Tk()
janela.title("DevBoard Ultimate")
janela.geometry("600x750")
janela.configure(bg="black")


# =========================
# Título do app
# =========================

titulo = tk.Label(
    janela,
    text="DEVBOARD - Monitor Completo",
    font=("Consolas", 20, "bold"),
    fg="white",
    bg="black"
)
titulo.pack(pady=15)


# =========================
# Função para criar cada bloco
# (texto + barra de progresso)
# =========================

def criar_bloco(cor):
    label = tk.Label(
        janela,
        text="",
        font=("Arial", 14),
        fg=cor,
        bg="black"
    )
    label.pack(pady=6)

    barra = ttk.Progressbar(
        janela,
        length=350,
        maximum=100
    )
    barra.pack()

    return label, barra


# =========================
# Criando os componentes
# que vão aparecer na tela
# =========================

cpu_label, cpu_bar = criar_bloco("lime")
ram_label, ram_bar = criar_bloco("cyan")
swap_label, swap_bar = criar_bloco("deepskyblue")
disk_label, disk_bar = criar_bloco("yellow")
battery_label, battery_bar = criar_bloco("orange")
network_label, network_bar = criar_bloco("magenta")


# =========================
# Guardando dados antigos
# da rede para calcular
# velocidade em tempo real
# =========================

old_net = psutil.net_io_counters()


# =========================
# Função principal que
# atualiza tudo sozinho
# =========================

def atualizar():
    global old_net

    # Pegando uso atual da CPU
    cpu = psutil.cpu_percent()

    # Mudando a cor dependendo do uso
    if cpu < 50:
        cor_cpu = "lime"
    elif cpu < 80:
        cor_cpu = "yellow"
    else:
        cor_cpu = "red"

    # Atualiza texto e barra da CPU
    cpu_label.config(
        text=f"CPU: {cpu}%",
        fg=cor_cpu
    )
    cpu_bar["value"] = cpu

    # Pegando dados da memória RAM
    ram = psutil.virtual_memory()
    ram_label.config(
        text=f"RAM: {ram.percent}%"
    )
    ram_bar["value"] = ram.percent

    # Pegando memória virtual (swap)
    swap = psutil.swap_memory()
    swap_label.config(
        text=f"SWAP: {swap.percent}%"
    )
    swap_bar["value"] = swap.percent

    # Pegando uso do disco principal
    disk = psutil.disk_usage("C:\\")
    disk_label.config(
        text=f"Disco: {disk.percent}%"
    )
    disk_bar["value"] = disk.percent

    # Verifica se existe bateria
    battery = psutil.sensors_battery()

    if battery:
        battery_label.config(
            text=f"Bateria: {battery.percent}%"
        )
        battery_bar["value"] = battery.percent
    else:
        battery_label.config(
            text="Bateria: Não disponível"
        )
        battery_bar["value"] = 0

    # Monitorando tráfego da internet
    new_net = psutil.net_io_counters()

    enviados = (new_net.bytes_sent - old_net.bytes_sent) / 1024
    recebidos = (new_net.bytes_recv - old_net.bytes_recv) / 1024

    velocidade = enviados + recebidos
    porcentagem = min(velocidade / 1000 * 100, 100)

    network_label.config(
        text=f"Rede: ↑{enviados:.1f} KB ↓{recebidos:.1f} KB"
    )
    network_bar["value"] = porcentagem

    # Atualiza valor antigo da rede
    old_net = new_net

    # Atualiza tudo de novo
    # depois de 1 segundo
    janela.after(1000, atualizar)


# =========================
# Iniciando o monitor
# =========================

atualizar()
janela.mainloop()