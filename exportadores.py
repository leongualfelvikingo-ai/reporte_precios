import csv
import html
from pathlib import Path

from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Font, PatternFill
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer


def _variacion(item):
    valor = item.get("variacion")
    return f"{valor:+.2f}%" if isinstance(valor, (int, float)) else "N/A"


def exportar_excel(reporte, ruta, grafico_actual=None, grafico_historico=None):
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte"
    ws.append(["Criptomoneda", "Precio USD", "Fecha consulta", "Variación %"])
    for item in reporte:
        ws.append([item["nombre"], item["precio"], item["fecha"], _variacion(item)])

    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(fill_type="solid", fgColor="4F81BD")

    for column, width in {"A": 22, "B": 16, "C": 22, "D": 16}.items():
        ws.column_dimensions[column].width = width

    for image_path, sheet_name in (
        (grafico_actual, "Gráfico actual"),
        (grafico_historico, "Historial"),
    ):
        if image_path and Path(image_path).is_file():
            sheet = wb.create_sheet(sheet_name)
            sheet.add_image(XLImage(image_path), "A1")

    wb.save(ruta)


def exportar_csv(reporte, ruta):
    with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["Criptomoneda", "Precio USD", "Fecha", "Variación %"])
        for item in reporte:
            writer.writerow([item["nombre"], item["precio"], item["fecha"], _variacion(item)])


def exportar_html(reporte, ruta):
    filas = []
    for item in reporte:
        filas.append(
            "<tr>"
            f"<td>{html.escape(str(item['nombre']))}</td>"
            f"<td>{html.escape(str(item['precio']))}</td>"
            f"<td>{html.escape(str(item['fecha']))}</td>"
            f"<td>{html.escape(_variacion(item))}</td>"
            "</tr>"
        )
    documento = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Reporte de criptomonedas</title>
<style>body{{font-family:Arial,sans-serif;margin:2rem;color:#202938}}table{{border-collapse:collapse;width:100%}}th{{background:#315f9c;color:#fff}}th,td{{padding:.65rem;border:1px solid #dce3ed;text-align:left}}tr:nth-child(even){{background:#f5f7fa}}</style>
</head><body><h1>Reporte de criptomonedas</h1><table><thead><tr><th>Criptomoneda</th><th>Precio USD</th><th>Fecha</th><th>Variación</th></tr></thead><tbody>{''.join(filas)}</tbody></table></body></html>"""
    Path(ruta).write_text(documento, encoding="utf-8")


def exportar_pdf(reporte, ruta, grafico_actual=None, grafico_historico=None):
    pdf = SimpleDocTemplate(ruta)
    estilos = getSampleStyleSheet()
    contenido = [Paragraph("Reporte de criptomonedas", estilos["Title"]), Spacer(1, 18)]

    for item in reporte:
        nombre = html.escape(str(item["nombre"]))
        precio = html.escape(str(item["precio"]))
        fecha = html.escape(str(item["fecha"]))
        contenido.extend([
            Paragraph(f"<b>{nombre}</b>", estilos["Heading2"]),
            Paragraph(f"Precio: USD {precio}", estilos["Normal"]),
            Paragraph(f"Fecha: {fecha}", estilos["Normal"]),
            Paragraph(f"Variación: {html.escape(_variacion(item))}", estilos["Normal"]),
            Spacer(1, 10),
        ])

    for image_path, titulo in (
        (grafico_actual, "Precios actuales"),
        (grafico_historico, "Historial de precios"),
    ):
        if image_path and Path(image_path).is_file():
            contenido.extend([
                Paragraph(titulo, estilos["Heading2"]),
                Image(image_path, width=450, height=250),
                Spacer(1, 14),
            ])

    pdf.build(contenido)
