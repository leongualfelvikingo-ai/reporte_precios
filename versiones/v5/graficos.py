import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from api import NOMBRES_CRIPTOS
from datetime import datetime

plt.rcParams["font.family"] = "DejaVu Sans"
COLORES = ["#F7931A", "#627EEA", "#BFBBBB", "#14F195", "#F3BA2F", "#23292F", "#0033AD", "#C2A633", "#E6007A", "#375BD2"]


def generar_grafico(reporte, ruta):
    validos = [item for item in reporte if isinstance(item.get("precio"), (int, float))]
    nombres = [item["nombre"] for item in validos]
    precios = [item["precio"] for item in validos]
    fig, ax = plt.subplots(figsize=(13, 7))
    if validos:
        ax.bar(nombres, precios, color=COLORES[:len(validos)])
        ax.set_yscale("log")
        ax.set_ylabel("Precio en USD (escala logarítmica)")
        ax.tick_params(axis="x", rotation=35)
    else:
        ax.text(0.5, 0.5, "No hay precios disponibles", ha="center", va="center")
        ax.set_axis_off()
    ax.set_title("Precio actual de criptomonedas")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def generar_grafico_historico(historial, ruta):
    from collections import defaultdict
    datos = defaultdict(list)
    for nombre, precio, fecha in historial:
        if isinstance(precio, (int, float)):
            datos[NOMBRES_CRIPTOS.get(nombre, nombre.replace("-", " ").title())].append((fecha, precio))
    if not datos:
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.text(0.5, 0.5, "Todavía no hay historial disponible", ha="center", va="center")
        ax.set_axis_off()
        fig.tight_layout()
        fig.savefig(ruta, dpi=150)
        plt.close(fig)
        return
    nombres = list(datos)
    fig, axes = plt.subplots(len(nombres), 1, figsize=(12, max(4, 2.8 * len(nombres))), squeeze=False)
    for index, nombre in enumerate(nombres):
        ax = axes[index][0]
        registros = sorted(datos[nombre])
        fechas = []
        for registro in registros:
            try:
                fechas.append(datetime.strptime(registro[0], "%Y-%m-%d %H:%M"))
            except (TypeError, ValueError):
                fechas.append(registro[0])
        precios = [registro[1] for registro in registros]
        ax.plot(fechas, precios, marker="o", label=nombre, color=COLORES[index % len(COLORES)])
        ax.set_title(f"Evolución de {nombre}")
        ax.set_ylabel("Precio USD")
        ax.tick_params(axis="x", rotation=35)
        ax.grid(True, alpha=0.3)
        ax.legend()
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
