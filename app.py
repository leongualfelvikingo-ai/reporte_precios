from flask import Flask, render_template
from datetime import datetime
from zoneinfo import ZoneInfo
from config import CRIPTOS
from api import obtener_precios, construir_reporte
from database import inicializar_db, guardar_precios

app = Flask(__name__)

@app.route("/")
def index():
    inicializar_db()
    data = obtener_precios(CRIPTOS)
    if not data:
        return "Error al obtener datos", 500

    ahora = datetime.now(
        ZoneInfo("America/Argentina/Buenos_Aires")
    ).strftime("%Y-%m-%d %H:%M")

    reporte = construir_reporte(CRIPTOS, data, ahora)
    guardar_precios(reporte)

    return render_template("index.html", reporte=reporte, fecha=ahora)

if __name__ == "__main__":
    app.run(debug=True, port=5000)