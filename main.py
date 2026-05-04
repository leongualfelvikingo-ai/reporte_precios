import requests
from openpyxl import Workbook
import os

# Crear carpeta si no existe
if not os.path.exists("output"):
    os.makedirs("output")

# Obtener datos
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
response = requests.get(url)
data = response.json()

precio = data["bitcoin"]["usd"]

# Crear Excel
wb = Workbook()
ws = wb.active

ws["A1"] = "Criptomoneda"
ws["B1"] = "Precio USD"

ws["A2"] = "Bitcoin"
ws["B2"] = precio

# Guardar archivo
wb.save("output/reporte.xlsx")

print("Reporte generado correctamente")