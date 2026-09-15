from flask import Flask, render_template, send_file
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from config import (
    CRIPTOS,
    ARCHIVO_SALIDA,
    ARCHIVO_CSV,
    ARCHIVO_HTML,
    ARCHIVO_PDF,
    ARCHIVO_GRAFICO_ACTUAL,
    ARCHIVO_GRAFICO_HISTORICO,
)

from api import obtener_precios, construir_reporte
from database import (
    inicializar_db,
    guardar_precios,
    obtener_historial,
    obtener_precio_anterior,
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


app = Flask(__name__)


def generar_reporte():
    inicializar_db()

    OUTPUT_DIR = os.path.dirname(ARCHIVO_SALIDA)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    data = obtener_precios(CRIPTOS)

    if not data:
        return None, None, None

    ahora = datetime.now(
        ZoneInfo("America/Argentina/Buenos_Aires")
    ).strftime("%Y-%m-%d %H:%M")

    reporte = construir_reporte(
        CRIPTOS,
        data,
        ahora,
        obtener_precio_anterior,
    )

    guardar_precios(reporte)

    exportar_excel(reporte, ARCHIVO_SALIDA)
    exportar_csv(reporte, ARCHIVO_CSV)
    exportar_html(reporte, ARCHIVO_HTML)
    exportar_pdf(reporte, ARCHIVO_PDF)

    generar_grafico(
        reporte,
        ARCHIVO_GRAFICO_ACTUAL,
    )

    historial = obtener_historial()

    generar_grafico_historico(
        historial,
        ARCHIVO_GRAFICO_HISTORICO,
    )

    return reporte, ahora, historial


@app.route("/")
def index():
    try:
        reporte, ahora, historial = generar_reporte()
    except Exception as error:
        return f"Error al generar el reporte: {error}", 503

    if not reporte:
        return "No se pudieron obtener datos de la API.", 503

    return render_template(
        "index.html",
        reporte=reporte,
        fecha=ahora,
        historial=historial,
    )


@app.route("/descargar/<archivo>")
def descargar(archivo):
    rutas = {
        "excel": ARCHIVO_SALIDA,
        "csv": ARCHIVO_CSV,
        "html": ARCHIVO_HTML,
        "pdf": ARCHIVO_PDF,
    }

    if archivo not in rutas:
        return "Archivo no encontrado", 404

    ruta = rutas[archivo]

    if not os.path.exists(ruta):
        return "El archivo todavía no fue generado.", 404

    return send_file(
        ruta,
        as_attachment=True,
    )


@app.route("/grafico/<nombre>")
def grafico(nombre):
    rutas = {
        "actual": ARCHIVO_GRAFICO_ACTUAL,
        "historico": ARCHIVO_GRAFICO_HISTORICO,
    }

    if nombre not in rutas:
        return "Gráfico no encontrado", 404

    ruta = rutas[nombre]

    if not os.path.exists(ruta):
        return "El gráfico todavía no fue generado.", 404

    return send_file(
        ruta,
        mimetype="image/png",
    )


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    port = int(os.getenv("PORT", "5000"))

    app.run(
        debug=debug,
        port=port,
    )
