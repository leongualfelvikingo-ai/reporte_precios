import os

from database import (
    inicializar_db,
    guardar_precios,
    obtener_historial,
    obtener_precio_anterior,
)

from datetime import datetime
from zoneinfo import ZoneInfo

from config import (
    CRIPTOS,
    OUTPUT_DIR,
    ARCHIVO_SALIDA,
    ARCHIVO_CSV,
    ARCHIVO_HTML,
    ARCHIVO_PDF,
    ARCHIVO_GRAFICO_ACTUAL,
    ARCHIVO_GRAFICO_HISTORICO,
)

from api import (
    obtener_precios,
    construir_reporte,
)

from exportadores import (
    exportar_excel,
    exportar_csv,
    exportar_html,
    exportar_pdf,
)

from graficos import (
    generar_grafico,
    generar_grafico_historico,
)


# Crear la carpeta de salida en la ubicación definida en config.py
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Inicializar base de datos
inicializar_db()


# Obtener datos
data = obtener_precios(CRIPTOS)

if not data:
    raise SystemExit("No se pudieron obtener datos de la API.")


# Fecha actual
ahora = datetime.now(
    ZoneInfo("America/Argentina/Buenos_Aires")
).strftime("%Y-%m-%d %H:%M")


# Construir reporte
reporte = construir_reporte(
    CRIPTOS,
    data,
    ahora,
    obtener_precio_anterior,
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


# Exportar los archivos usando las rutas centralizadas en config.py
exportar_excel(reporte, ARCHIVO_SALIDA)
exportar_csv(reporte, ARCHIVO_CSV)
exportar_html(reporte, ARCHIVO_HTML)
exportar_pdf(reporte, ARCHIVO_PDF)


# Generar gráfico de precios actuales
generar_grafico(reporte, ARCHIVO_GRAFICO_ACTUAL)


# Obtener historial actualizado
historial = obtener_historial()


# Generar gráfico histórico
generar_grafico_historico(historial, ARCHIVO_GRAFICO_HISTORICO)


# Resumen final
print("\nArchivos generados correctamente:\n")
print(f"- Excel: {ARCHIVO_SALIDA}")
print(f"- CSV: {ARCHIVO_CSV}")
print(f"- HTML: {ARCHIVO_HTML}")
print(f"- PDF: {ARCHIVO_PDF}")
print(f"- Gráfico actual: {ARCHIVO_GRAFICO_ACTUAL}")
print(f"- Gráfico histórico: {ARCHIVO_GRAFICO_HISTORICO}")
