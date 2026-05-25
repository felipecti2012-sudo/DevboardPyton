import tkinter as tk
import psutil

# Criar janela
janela = tk.Tk()
janela.title("DevBoard")
janela.geometry("500x300")
janela.configure(bg="white")


# Criar textos (labels)
cpu_label = tk.Label(
    janela,
    text="",
    font=("Arial", 18),
    fg="red",
    bg="white"
)
cpu_label.pack(pady=20)


ram_label = tk.Label(
    janela,
    text="",
    font=("Arial", 18),
    fg="red",
    bg="white"
)
ram_label.pack(pady=20)

disk_label = tk.Label(
    janela,
    text="",
    font=("Arial", 18),
    fg="red",
    bg="white"
)
disk_label.pack(pady=20)

# Função que atualiza os dados
def atualizar():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("C:\\").percent

    cpu_label.config(text=f"CPU: {cpu}%")
    ram_label.config(text=f"RAM: {ram}%")
    disk_label.config(text=f"Disco: {disk}%")
    # Atualiza novamente em 1 segundo
    janela.after(1000, atualizar)


# Começar atualização
atualizar()


# Manter a janela aberta
janela.mainloop()