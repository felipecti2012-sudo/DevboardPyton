import psutil
import time

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live


console = Console()


# -------------------
# INFORMAÇÕES SISTEMA
# -------------------

def get_cpu():
    return psutil.cpu_percent(interval=0.5)


def get_ram():
    return psutil.virtual_memory()


def get_disk():
    return psutil.disk_usage("C:\\")


def get_boot_time():
    boot = psutil.boot_time()
    return time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(boot))


# -------------------
# TABELA PRINCIPAL
# -------------------

def build_system_table():
    cpu = get_cpu()
    ram = get_ram()
    disk = get_disk()

    table = Table(title="DevBoard - Monitor do Sistema")

    table.add_column("Métrica", style="cyan")
    table.add_column("Valor", style="green")

    table.add_row("CPU", f"{cpu}%")
    table.add_row("Núcleos físicos", str(psutil.cpu_count(logical=False)))
    table.add_row("Núcleos lógicos", str(psutil.cpu_count()))
    table.add_row("RAM usada", f"{ram.used / (1024**3):.2f} GB")
    table.add_row("RAM total", f"{ram.total / (1024**3):.2f} GB")
    table.add_row("RAM %", f"{ram.percent}%")
    table.add_row("Disco livre", f"{disk.free / (1024**3):.2f} GB")
    table.add_row("Disco %", f"{disk.percent}%")
    table.add_row("Boot do sistema", get_boot_time())

    return table


# -------------------
# TOP PROCESSOS
# -------------------

def build_process_table():
    table = Table(title="Top Processos (RAM)")

    table.add_column("Processo")
    table.add_column("RAM MB")

    processos = []

    for proc in psutil.process_iter(
        ["name", "memory_info"]
    ):
        try:
            nome = proc.info["name"]
            memoria = proc.info["memory_info"].rss / (1024 * 1024)

            processos.append((nome, memoria))

        except:
            pass

    processos.sort(
        key=lambda x: x[1],
        reverse=True
    )

    top5 = processos[:5]

    for nome, memoria in top5:
        table.add_row(
            nome,
            f"{memoria:.1f}"
        )

    return table


# -------------------
# ALERTAS
# -------------------

def build_alert_panel():
    cpu = psutil.cpu_percent()

    if cpu >= 90:
        mensagem = "[bold red]ALERTA: CPU quase no limite![/bold red]"
    elif cpu >= 70:
        mensagem = "[yellow]CPU alta[/yellow]"
    else:
        mensagem = "[green]Sistema estável[/green]"

    return Panel(
        mensagem,
        title="Status"
    )


# -------------------
# LAYOUT GERAL
# -------------------

def build_layout():
    layout = Layout()

    layout.split_column(
        Layout(name="top", size=12),
        Layout(name="middle", size=12),
        Layout(name="bottom", size=5),
    )

    layout["top"].update(
        build_system_table()
    )

    layout["middle"].update(
        build_process_table()
    )

    layout["bottom"].update(
        build_alert_panel()
    )

    return layout


# -------------------
# LOOP PRINCIPAL
# -------------------

if __name__ == "__main__":
    console.print(
        "[bold green]Iniciando DevBoard...[/bold green]"
    )

    with Live(
        build_layout(),
        refresh_per_second=1,
        console=console
    ) as live:

        while True:
            time.sleep(1)
            live.update(
                build_layout()
            )