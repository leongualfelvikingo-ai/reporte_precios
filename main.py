import os

from database import (
    inicializar_db,
    guardar_precios,
    obtener_historial
)

from datetime import datetime
from zoneinfo import ZoneInfo

from config import (
    CRIPTOS,
    ARCHIVO_SALIDA
)

from api import (
    obtener_precios,
    construir_reporte
)

from exportadores import (
    exportar_excel,
    exportar_csv,
    exportar_html,
    exportar_pdf
)

from graficos import (
    generar_grafico,
    generar_grafico_historico
)


# Crear carpeta si no existe
os.makedirs(
    "output",
    exist_ok=True
)


# Inicializar base de datos
inicializar_db()


# Obtener datos
data = obtener_precios(CRIPTOS)

if not data:
    exit()


# Fecha actual
ahora = datetime.now(
    ZoneInfo(
        "America/Argentina/Buenos_Aires"
    )
).strftime(
    "%Y-%m-%d %H:%M"
)


# Construir reporte
reporte = construir_reporte(
    CRIPTOS,
    data,
    ahora
)


# Guardar precios en base de datos
guardar_precios(reporte)


# Mostrar en consola
print("\nREPORTE DE CRIPTOMONEDAS\n")

for item in reporte:

    variacion = item["variacion"]

    if variacion is not None:

        signo = "+" if variacion > 0 else ""

        var_str = f" ({signo}{variacion}%)"

    else:

        var_str = " (sin historial)"

    print(
        f"{item['nombre']}: "
        f"USD {item['precio']}"
        f"{var_str} "
        f"({item['fecha']})"
    )


# Exportar
exportar_excel(
    reporte,
    ARCHIVO_SALIDA
)

exportar_csv(
    reporte,
    "output/reporte.csv"
)

exportar_html(
    reporte,
    "output/reporte.html"
)

exportar_pdf(
    reporte,
    "output/reporte.pdf"
)


# Generar gráfico de precios actuales
generar_grafico(
    reporte,
    "output/grafico_precios.png"
)


# Obtener historial actualizado
historial = obtener_historial()


# Generar gráfico histórico
generar_grafico_historico(
    historial,
    "output/grafico_historico.png"
)


# Resumen final
print("\nArchivos generados correctamente:\n")

print(f"- Excel : {ARCHIVO_SALIDA}")
print("- CSV   : output/reporte.csv")
print("- HTML  : output/reporte.html")
print("- PDF   : output/reporte.pdf")
print("- Gráfico : output/grafico_precios.png")
print("- Gráfico histórico : output/grafico_historico.png")