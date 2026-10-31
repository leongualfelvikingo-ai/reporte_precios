import csv
import html
from pathlib import Path
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Font, PatternFill
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer
from config import ARCHIVO_GRAFICO_ACTUAL, ARCHIVO_GRAFICO_HISTORICO


def _variacion(item):
    return item.get("variacion") if item.get("variacion") is not None else "N/A"


def exportar_excel(reporte, ruta, grafico_actual=ARCHIVO_GRAFICO_ACTUAL, grafico_historico=ARCHIVO_GRAFICO_HISTORICO):
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte"
    ws.append(["Criptomoneda", "Precio USD", "Fecha consulta", "Variación %"])
    for item in reporte:
        ws.append([item["nombre"], item["precio"], item["fecha"], _variacion(item)])
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(fill_type="solid", fgColor="4F81BD")
    for column, width in {"A": 20, "B": 16, "C": 22, "D": 15}.items():
        ws.column_dimensions[column].width = width
    for image_path, sheet_name in ((grafico_actual, "Gráfico Actual"), (grafico_historico, "Gráfico Histórico")):
        if Path(image_path).is_file():
            chart_sheet = wb.create_sheet(sheet_name)
            chart_sheet.add_image(XLImage(image_path), "A1")
    wb.save(ruta)


def exportar_csv(reporte, ruta):
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["Criptomoneda", "Precio USD", "Fecha", "Variación %"])
        for item in reporte:
            writer.writerow([item["nombre"], item["precio"], item["fecha"], _variacion(item)])


def exportar_html(reporte, ruta):
    filas = []
    for item in reporte:
        filas.append("<tr>" + "".join(
            f"<td>{html.escape(str(value))}</td>"
            for value in (item["nombre"], item["precio"], item["fecha"], _variacion(item))
        ) + "</tr>")
    contenido = """<!doctype html><html lang="es"><head><meta charset="UTF-8"><title>Reporte</title></head><body><h1>Reporte de Criptomonedas</h1><table><thead><tr><th>Criptomoneda</th><th>Precio USD</th><th>Fecha</th><th>Variación %</th></tr></thead><tbody>""" + "".join(filas) + "</tbody></table></body></html>"
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(contenido)


def exportar_pdf(reporte, ruta, grafico_actual=ARCHIVO_GRAFICO_ACTUAL, grafico_historico=ARCHIVO_GRAFICO_HISTORICO):
    pdf = SimpleDocTemplate(ruta)
    styles = getSampleStyleSheet()
    contenido = [Paragraph("Reporte de Criptomonedas", styles["Title"]), Spacer(1, 20)]
    for item in reporte:
        variacion = item.get("variacion")
        var_str = f"{'+' if variacion > 0 else ''}{variacion}%" if variacion is not None else "N/A"
        contenido.extend([
            Paragraph(f"<b>{html.escape(str(item['nombre']))}</b>", styles["Heading2"]),
            Paragraph(f"Precio: USD {html.escape(str(item['precio']))}", styles["Normal"]),
            Paragraph(f"Fecha: {html.escape(str(item['fecha']))}", styles["Normal"]),
            Paragraph(f"Variación: {html.escape(var_str)}", styles["Normal"]), Spacer(1, 10),
        ])
    for image_path, title in ((grafico_actual, "Precios actuales"), (grafico_historico, "Historial de precios")):
        if Path(image_path).is_file():
            contenido.extend([Paragraph(title, styles["Heading2"]), Image(image_path, width=450, height=250), Spacer(1, 15)])
    pdf.build(contenido)
