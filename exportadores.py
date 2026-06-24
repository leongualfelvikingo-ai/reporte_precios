import csv
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill


def exportar_excel(reporte, ruta):
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte Cripto"

    ws["A1"] = "Criptomoneda"
    ws["B1"] = "Precio USD"
    ws["C1"] = "Fecha consulta"

    for cell in ["A1", "B1", "C1"]:
        ws[cell].font = Font(bold=True, color="FFFFFF")
        ws[cell].fill = PatternFill(fill_type="solid", fgColor="4F81BD")

    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 15
    ws.column_dimensions["C"].width = 25

    for i, item in enumerate(reporte, start=2):
        ws[f"A{i}"] = item["nombre"]
        ws[f"B{i}"] = item["precio"]
        ws[f"C{i}"] = item["fecha"]

    wb.save(ruta)


def exportar_csv(reporte, ruta):
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Criptomoneda", "Precio USD", "Fecha"])
        for item in reporte:
            writer.writerow([item["nombre"], item["precio"], item["fecha"]])


def exportar_html(reporte, ruta):
    filas = ""
    for item in reporte:
        filas += f"<tr><td>{item['nombre']}</td><td>{item['precio']}</td><td>{item['fecha']}</td></tr>\n"

    html = f"""<html>
<head><meta charset="UTF-8"><title>Reporte Cripto</title></head>
<body>
<h1>Reporte de Criptomonedas</h1>
<table border="1">
<tr><th>Criptomoneda</th><th>Precio USD</th><th>Fecha</th></tr>
{filas}
</table>
</body>
</html>"""

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)