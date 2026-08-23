import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def generar_grafico(reporte, ruta):
    nombres = [item["nombre"] for item in reporte]
    precios = [item["precio"] for item in reporte]

    plt.figure(figsize=(10, 6))
    plt.bar(nombres, precios, color=["#F7931A", "#627EEA", "#BFBBBB"])
    plt.yscale("log")
    plt.title("Precio actual de criptomonedas")
    plt.xlabel("Criptomoneda")
    plt.ylabel("Precio en USD")
    plt.tight_layout()
    plt.savefig(ruta)
    plt.close()

def generar_grafico_historico(historial, ruta):
    from collections import defaultdict

    datos = defaultdict(list)
    for nombre, precio, fecha in historial:
        datos[nombre].append((fecha, precio))

    criptos = list(datos.keys())
    fig, axes = plt.subplots(len(criptos), 1, figsize=(12, 4 * len(criptos)))

    if len(criptos) == 1:
        axes = [axes]

    for ax, nombre in zip(axes, criptos):
        registros = sorted(datos[nombre])
        fechas = [r[0] for r in registros]
        precios = [r[1] for r in registros]

        ax.plot(fechas, precios, marker="o", label=nombre)
        ax.set_title(f"Evolución de {nombre}")
        ax.set_ylabel("Precio USD")
        ax.tick_params(axis="x", rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(ruta)
    plt.close()
