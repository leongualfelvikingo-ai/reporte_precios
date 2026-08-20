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

def generar_grafico_historico(historial, ruta):
    from collections import defaultdict

    datos = defaultdict(list)

    for nombre, precio, fecha in historial:
        datos[nombre].append((fecha, precio))

    plt.figure(figsize=(12, 6))

    for nombre, registros in datos.items():
        registros.sort()

        fechas = [r[0] for r in registros]
        precios = [r[1] for r in registros]

        plt.plot(
            fechas,
            precios,
            marker="o",
            label=nombre
        )

    plt.title("Evolución histórica de precios")
    plt.xlabel("Fecha")
    plt.ylabel("Precio en USD")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(ruta)
    plt.close()