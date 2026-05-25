import tkinter as tk
import psutil

# Criar janela
janela = tk.Tk()
janela.title("DevBoard")
janela.geometry("500x300")


# Criar textos vazios
cpu_label = tk.Label(janela, text="")
cpu_label.pack(pady=20)

ram_label = tk.Label(janela, text="")
ram_label.pack(pady=20)


# Função que atualiza os dados
def atualizar():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    cpu_label.config(text=f"CPU: {cpu}%")
    ram_label.config(text=f"RAM: {ram}%")

    janela.after(1000, atualizar)


# Começar atualização
atualizar()

# Manter aberta
janela.mainloop()