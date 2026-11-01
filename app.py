import logging
import os

from flask import Flask, render_template, send_file, request

from config import (
    ARCHIVO_SALIDA, ARCHIVO_CSV, ARCHIVO_HTML, ARCHIVO_PDF,
    ARCHIVO_GRAFICO_ACTUAL, ARCHIVO_GRAFICO_HISTORICO,
)
from main import generar_reporte

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("reporte_precios_v4")

RUTAS_DESCARGA = {
    "excel": ARCHIVO_SALIDA,
    "csv": ARCHIVO_CSV,
    "html": ARCHIVO_HTML,
    "pdf": ARCHIVO_PDF,
}
formatos_disponibles = set()


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/generar")
def generar():
    global formatos_disponibles
    # Un informe fallido no debe dejar habilitadas descargas de una ejecución anterior.
    formatos_disponibles = set()
    formatos = request.form.getlist("formatos")
    try:
        resultado = generar_reporte(formatos)
        formatos_disponibles = set(resultado["formatos"])
        return render_template(
            "index.html",
            reporte=resultado["reporte"],
            fecha=resultado["fecha"],
            formatos=resultado["formatos"],
            generado=True,
        )
    except ValueError as error:
        return render_template("index.html", error=str(error)), 400
    except Exception:
        logger.exception("Error al generar el reporte v4")
        return render_template(
            "index.html",
            error="No se pudo generar el informe. Revisá la conexión e intentá nuevamente.",
        ), 503


@app.get("/descargar/<formato>")
def descargar(formato):
    if formato not in RUTAS_DESCARGA or formato not in formatos_disponibles:
        return "Formato no disponible en el último informe.", 404
    ruta = RUTAS_DESCARGA[formato]
    if not os.path.isfile(ruta):
        return "El archivo no está disponible.", 404
    return send_file(ruta, as_attachment=True)


@app.get("/grafico/<nombre>")
def grafico(nombre):
    rutas = {
        "actual": ARCHIVO_GRAFICO_ACTUAL,
        "historico": ARCHIVO_GRAFICO_HISTORICO,
    }
    if nombre not in rutas or not os.path.isfile(rutas[nombre]):
        return "Gráfico no disponible.", 404
    return send_file(rutas[nombre], mimetype="image/png")


@app.get("/health")
def health():
    return {"status": "ok", "version": "4.1"}


if __name__ == "__main__":
    app.run(
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
        port=int(os.getenv("PORT", "5000")),
    )
