from flask import Flask, render_template, send_file
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from config import CRIPTOS, ARCHIVO_SALIDA
from api import obtener_precios, construir_reporte
from database import inicializar_db, guardar_precios, obtener_historial
from exportadores import exportar_excel, exportar_csv, exportar_html, exportar_pdf
from graficos import generar_grafico, generar_grafico_historico

app = Flask(__name__)

def generar_reporte():
    inicializar_db()
    os.makedirs("output", exist_ok=True)
    data = obtener_precios(CRIPTOS)
    if not data:
        return None, None, None

    ahora = datetime.now(
        ZoneInfo("America/Argentina/Buenos_Aires")
    ).strftime("%Y-%m-%d %H:%M")

    reporte = construir_reporte(CRIPTOS, data, ahora)
    guardar_precios(reporte)

    exportar_excel(reporte, ARCHIVO_SALIDA)
    exportar_csv(reporte, "output/reporte.csv")
    exportar_html(reporte, "output/reporte.html")
    exportar_pdf(reporte, "output/reporte.pdf")
    generar_grafico(reporte, "output/grafico_precios.png")
    historial = obtener_historial()
    generar_grafico_historico(historial, "output/grafico_historico.png")

    return reporte, ahora, historial

@app.route("/")
def index():
    reporte, ahora, historial = generar_reporte()
    if not reporte:
        return "Error al obtener datos", 500
    return render_template("index.html", reporte=reporte, fecha=ahora, historial=historial)

@app.route("/descargar/<archivo>")
def descargar(archivo):
    rutas = {
        "excel": ARCHIVO_SALIDA,
        "csv": "output/reporte.csv",
        "pdf": "output/reporte.pdf"
    }
    if archivo not in rutas:
        return "Archivo no encontrado", 404
    return send_file(rutas[archivo], as_attachment=True)

@app.route("/grafico/<nombre>")
def grafico(nombre):
    rutas = {
        "actual": "output/grafico_precios.png",
        "historico": "output/grafico_historico.png"
    }
    if nombre not in rutas:
        return "Gráfico no encontrado", 404
    return send_file(rutas[nombre], mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True, port=5000)