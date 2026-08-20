import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def generar_grafico(reporte, ruta):
    nombres = [item["nombre"] for item in reporte]
    precios = [item["precio"] for item in reporte]

    plt.figure(figsize=(10, 6))
    plt.bar(nombres, precios, color=["#F7931A", "#627EEA", "#BFBBBB"])
    plt.title("Precio actual de criptomonedas")
    plt.xlabel("Criptomoneda")
    plt.ylabel("Precio en USD")
    plt.tight_layout()
    plt.savefig(ruta)
    plt.close()