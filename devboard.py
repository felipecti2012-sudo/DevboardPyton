import tkinter as tk
from tkinter import ttk
import psutil

# =========================
# CRIAR JANELA
# =========================

janela = tk.Tk()
janela.title("DevBoard")
janela.geometry("500x500")
janela.configure(bg="black")


# =========================
# TÍTULO
# =========================

titulo = tk.Label(
    janela,
    text="DEVBOARD - Monitor do Sistema",
    font=("Consolas", 20, "bold"),
    fg="white",
    bg="black"
)
titulo.pack(pady=15)


# =========================
# CPU
# =========================

cpu_label = tk.Label(
    janela,
    text="",
    font=("Arial", 18),
    fg="lime",
    bg="black"
)
cpu_label.pack(pady=10)

cpu_bar = ttk.Progressbar(
    janela,
    length=300,
    maximum=100
)
cpu_bar.pack()


# =========================
# RAM
# =========================

ram_label = tk.Label(
    janela,
    text="",
    font=("Arial", 18),
    fg="cyan",
    bg="black"
)
ram_label.pack(pady=10)

ram_bar = ttk.Progressbar(
    janela,
    length=300,
    maximum=100
)
ram_bar.pack()


# =========================
# DISCO
# =========================

disk_label = tk.Label(
    janela,
    text="",
    font=("Arial", 18),
    fg="yellow",
    bg="black"
)
disk_label.pack(pady=10)

disk_bar = ttk.Progressbar(
    janela,
    length=300,
    maximum=100
)
disk_bar.pack()


# =========================
# FUNÇÃO DE ATUALIZAÇÃO
# =========================

def atualizar():
    # pegar dados do sistema
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("C:\\").percent

    # mudar cor da CPU conforme uso
    if cpu < 50:
        cor_cpu = "lime"
    elif cpu < 80:
        cor_cpu = "yellow"
    else:
        cor_cpu = "red"

    # atualizar textos
    cpu_label.config(
        text=f"CPU: {cpu}%",
        fg=cor_cpu
    )

    ram_label.config(
        text=f"RAM: {ram}%"
    )

    disk_label.config(
        text=f"Disco: {disk}%"
    )

    # atualizar barras
    cpu_bar["value"] = cpu
    ram_bar["value"] = ram
    disk_bar["value"] = disk

    # repetir a cada 1 segundo
    janela.after(1000, atualizar)


# =========================
# INICIAR APP
# =========================

atualizar()
janela.mainloop()