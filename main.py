import os
from datetime import datetime
from zoneinfo import ZoneInfo
from config import CRIPTOS, ARCHIVO_SALIDA
from api import obtener_precios, construir_reporte
from exportadores import exportar_excel, exportar_csv, exportar_html

# Crear carpeta si no existe
os.makedirs("output", exist_ok=True)

# Obtener datos
data = obtener_precios(CRIPTOS)
if not data:
    exit()

# Fecha actual
ahora = datetime.now(
    ZoneInfo("America/Argentina/Buenos_Aires")
).strftime("%Y-%m-%d %H:%M")

# Construir reporte
reporte = construir_reporte(CRIPTOS, data, ahora)

# Mostrar en consola
print("\nREPORTE DE CRIPTOMONEDAS\n")
for item in reporte:
    print(f"{item['nombre']}: USD {item['precio']} ({item['fecha']})")

# Exportar
exportar_excel(reporte, ARCHIVO_SALIDA)
exportar_csv(reporte, "output/reporte.csv")
exportar_html(reporte, "output/reporte.html")

print("\nArchivos generados correctamente:\n")
print(f"- Excel : {ARCHIVO_SALIDA}")
print("- CSV   : output/reporte.csv")
print("- HTML  : output/reporte.html")