import tkinter as tk
from tkinter import ttk
import psutil
import socket


# ==========================================
# CONFIGURAÇÃO DA JANELA
# ==========================================

janela = tk.Tk()
janela.title("DevBoard Ultimate")
janela.geometry("700x850")
janela.configure(bg="black")


# ==========================================
# TÍTULO PRINCIPAL
# ==========================================

titulo = tk.Label(
    janela,
    text="DEVBOARD - Monitor Completo",
    font=("Consolas", 20, "bold"),
    fg="white",
    bg="black"
)
titulo.pack(pady=15)


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def criar_bloco(cor):
    """Cria um label e uma barra"""

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


def atualizar_bloco(label, barra, texto, valor):
    """Atualiza texto e barra"""

    label.config(text=texto)
    barra["value"] = valor


def bytes_para_gb(valor):
    """Converte bytes para GB"""

    return valor / (1024 ** 3)


# ==========================================
# COMPONENTES DA TELA
# ==========================================

# CPU
cpu_label, cpu_bar = criar_bloco("lime")

# Frequência da CPU
freq_label = tk.Label(
    janela,
    text="",
    font=("Arial", 12),
    fg="white",
    bg="black"
)
freq_label.pack(pady=2)


# RAM
ram_label, ram_bar = criar_bloco("cyan")

# Detalhes da RAM
ram_info_label = tk.Label(
    janela,
    text="",
    font=("Arial", 12),
    fg="white",
    bg="black"
)
ram_info_label.pack(pady=2)


# SWAP
swap_label, swap_bar = criar_bloco("deepskyblue")


# DISCO
disk_label, disk_bar = criar_bloco("yellow")

# Detalhes do disco
disk_info_label = tk.Label(
    janela,
    text="",
    font=("Arial", 12),
    fg="white",
    bg="black"
)
disk_info_label.pack(pady=2)


# BATERIA
battery_label, battery_bar = criar_bloco("orange")


# REDE
network_label, network_bar = criar_bloco("magenta")

# IP do computador
ip_label = tk.Label(
    janela,
    text="",
    font=("Arial", 12),
    fg="white",
    bg="black"
)
ip_label.pack(pady=2)


# ==========================================
# VARIÁVEIS DE CONTROLE
# ==========================================

old_net = psutil.net_io_counters()

# Pegando IP só uma vez
try:
    ip_local = socket.gethostbyname(socket.gethostname())
except:
    ip_local = "Indisponível"


# ==========================================
# LOOP PRINCIPAL
# ==========================================

def atualizar():
    global old_net

    # ----------------------
    # CPU
    # ----------------------

    cpu = psutil.cpu_percent(interval=None)
    freq = psutil.cpu_freq()

    if cpu < 50:
        cor_cpu = "lime"
    elif cpu < 80:
        cor_cpu = "yellow"
    else:
        cor_cpu = "red"

    cpu_label.config(
        text=f"CPU: {cpu}%",
        fg=cor_cpu
    )
    cpu_bar["value"] = cpu

    if freq:
        freq_label.config(
            text=f"CPU Freq: {freq.current:.0f} MHz"
        )
    else:
        freq_label.config(
            text="CPU Freq: Indisponível"
        )

    # ----------------------
    # RAM
    # ----------------------

    ram = psutil.virtual_memory()

    atualizar_bloco(
        ram_label,
        ram_bar,
        f"RAM: {ram.percent}%",
        ram.percent
    )

    ram_info_label.config(
        text=(
            f"Total: {bytes_para_gb(ram.total):.1f} GB | "
            f"Livre: {bytes_para_gb(ram.available):.1f} GB"
        )
    )

    # ----------------------
    # SWAP
    # ----------------------

    swap = psutil.swap_memory()

    atualizar_bloco(
        swap_label,
        swap_bar,
        f"SWAP: {swap.percent}%",
        swap.percent
    )

    # ----------------------
    # DISCO
    # ----------------------

    disk = psutil.disk_usage("C:\\")

    atualizar_bloco(
        disk_label,
        disk_bar,
        f"Disco: {disk.percent}%",
        disk.percent
    )

    disk_info_label.config(
        text=(
            f"Total: {bytes_para_gb(disk.total):.1f} GB | "
            f"Livre: {bytes_para_gb(disk.free):.1f} GB"
        )
    )

    # ----------------------
    # BATERIA
    # ----------------------

    battery = psutil.sensors_battery()

    if battery is not None:
        atualizar_bloco(
            battery_label,
            battery_bar,
            f"Bateria: {battery.percent}%",
            battery.percent
        )
    else:
        atualizar_bloco(
            battery_label,
            battery_bar,
            "Bateria: Não disponível",
            0
        )

    # ----------------------
    # REDE
    # ----------------------

    new_net = psutil.net_io_counters()

    enviados = (
        new_net.bytes_sent - old_net.bytes_sent
    ) / 1024

    recebidos = (
        new_net.bytes_recv - old_net.bytes_recv
    ) / 1024

    velocidade = enviados + recebidos
    porcentagem = min(velocidade / 1000 * 100, 100)

    atualizar_bloco(
        network_label,
        network_bar,
        f"Rede: ↑{enviados:.1f} KB ↓{recebidos:.1f} KB",
        porcentagem
    )

    ip_label.config(
        text=f"IP: {ip_local}"
    )

    # Guarda valor atual da rede
    old_net = new_net

    # Atualiza novamente em 1 segundo
    janela.after(1000, atualizar)


# ==========================================
# INICIAR APP
# ==========================================

atualizar()
janela.mainloop()