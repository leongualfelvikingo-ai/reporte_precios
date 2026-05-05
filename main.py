import requests
from openpyxl import Workbook
import os
from datetime import datetime
from config import CRIPTOS, ARCHIVO_SALIDA

# Crear carpeta si no existe
if not os.path.exists("output"):
    os.makedirs("output")

# Construir URL dinámica
ids = ",".join(CRIPTOS)
url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"

# Obtener datos (con manejo de error básico)
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print("Error al obtener datos:", e)
    exit()

# Fecha actual
ahora = datetime.now().strftime("%Y-%m-%d %H:%M")

# Crear Excel
wb = Workbook()
ws = wb.active

# Encabezados
ws["A1"] = "Criptomoneda"
ws["B1"] = "Precio USD"
ws["C1"] = "Fecha consulta"

# Datos
for i, cripto in enumerate(CRIPTOS, start=2):
    ws[f"A{i}"] = cripto.capitalize()
    ws[f"B{i}"] = data[cripto]["usd"]
    ws[f"C{i}"] = ahora

# Guardar archivo
wb.save(ARCHIVO_SALIDA)

print(f"Reporte generado correctamente en {ARCHIVO_SALIDA}")