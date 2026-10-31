import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


COLORES = ["#F7931A", "#627EEA", "#BFBBBB"]


def generar_grafico(reporte, ruta):
    validos = [
        item for item in reporte
        if isinstance(item.get("precio"), (int, float))
    ]
    fig, ax = plt.subplots(figsize=(10, 6))

    if validos:
        nombres = [item["nombre"] for item in validos]
        precios = [item["precio"] for item in validos]
        ax.bar(nombres, precios, color=[COLORES[i % len(COLORES)] for i in range(len(validos))])
        ax.set_yscale("log")
        ax.set_ylabel("Precio en USD (escala logarítmica)")
        ax.tick_params(axis="x", rotation=35)
    else:
        ax.text(0.5, 0.5, "No hay precios disponibles", ha="center", va="center")
        ax.set_axis_off()

    ax.set_title("Precio actual de criptomonedas")
    fig.tight_layout()
    fig.savefig(ruta, dpi=140)
    plt.close(fig)


def generar_grafico_historico(historial, ruta):
    from collections import defaultdict

    datos = defaultdict(list)
    for nombre, precio, fecha in historial:
        if isinstance(precio, (int, float)):
            datos[nombre].append((fecha, precio))

    if not datos:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.text(0.5, 0.5, "Todavía no hay historial disponible", ha="center", va="center")
        ax.set_axis_off()
        fig.tight_layout()
        fig.savefig(ruta, dpi=140)
        plt.close(fig)
        return

    nombres = list(datos)
    fig, axes = plt.subplots(len(nombres), 1, figsize=(12, max(4, 3 * len(nombres))), squeeze=False)
    for index, nombre in enumerate(nombres):
        ax = axes[index][0]
        registros = sorted(datos[nombre])
        fechas = [registro[0] for registro in registros]
        precios = [registro[1] for registro in registros]
        ax.plot(fechas, precios, marker="o")
        ax.set_title(f"Evolución de {nombre}")
        ax.set_ylabel("Precio USD")
        ax.tick_params(axis="x", rotation=35)
        ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(ruta, dpi=140)
    plt.close(fig)
