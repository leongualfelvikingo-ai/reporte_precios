import logging
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file

from config import DEFAULT_TIMEZONE, REPORTS_DIR, SUPPORTED_LANGUAGES
from database import autorizar_descarga, marcar_pagado, obtener_archivos
from main import generar_reporte

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("reporte_precios")
# Fail closed: the simulated payment flow must be explicitly enabled for local testing.
DEMO_PAYMENTS_ENABLED = os.getenv("DEMO_PAYMENTS_ENABLED", "0") == "1"


def _error_id():
    import uuid
    return f"REP-{uuid.uuid4().hex[:10].upper()}"


def _authorized(report_id, owner_token):
    from database import _hash
    import sqlite3
    from config import ARCHIVO_BASE_DATOS
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        row = db.execute("SELECT owner_token_hash FROM reportes WHERE id=?", (report_id,)).fetchone()
    return bool(row and owner_token and row[0] == _hash(owner_token))


@app.get("/")
def index():
    return render_template("index.html", demo_payments=DEMO_PAYMENTS_ENABLED)


@app.post("/generar")
def generar():
    if not DEMO_PAYMENTS_ENABLED:
        return jsonify({"error": "El pago debe confirmarse mediante el proveedor configurado."}), 402
    try:
        language = request.form.get("language", "es")
        timezone_name = request.form.get("timezone", DEFAULT_TIMEZONE)
        if language not in SUPPORTED_LANGUAGES:
            language = "es"
        result = generar_reporte(timezone_name=timezone_name, language=language)
        return jsonify({
            "report_id": result["id"], "owner_token": result["owner_token"],
            "download_tokens": result["download_tokens"],
            "view_url": f"/reporte/{result['id']}?owner_token={result['owner_token']}",
            "crypto_count": len(result["reporte"]),
        }), 201
    except Exception:
        error_id = _error_id()
        logger.exception("Fallo de generación %s", error_id)
        return jsonify({"error": "No se pudo generar el informe.", "error_id": error_id}), 503


@app.get("/reporte/<report_id>")
def ver_reporte(report_id):
    owner_token = request.args.get("owner_token")
    if not _authorized(report_id, owner_token):
        return jsonify({"error": "Informe no autorizado."}), 403
    from database import obtener_historial
    rows = obtener_historial(report_id)
    return jsonify({"report_id": report_id, "historial": rows, "files": obtener_archivos(report_id)})


@app.post("/demo/pagar/<report_id>/<formato>")
def pagar_demo(report_id, formato):
    if not DEMO_PAYMENTS_ENABLED:
        return jsonify({"error": "Los pagos demo están desactivados."}), 404
    owner_token = request.args.get("owner_token")
    if not _authorized(report_id, owner_token):
        return jsonify({"error": "Informe no autorizado."}), 403
    formatos = {row[0]: row for row in obtener_archivos(report_id)}
    if formato not in formatos:
        return jsonify({"error": "Formato no disponible."}), 404
    marcar_pagado(report_id, formato)
    return jsonify({"paid": True, "download_url": f"/descargar/{report_id}/{formato}?token={request.args.get('download_token', '')}"})


@app.get("/descargar/<report_id>/<formato>")
def descargar(report_id, formato):
    token = request.args.get("token")
    if formato not in {"excel", "csv", "html", "pdf"} or not autorizar_descarga(report_id, formato, token):
        return jsonify({"error": "Descarga no autorizada."}), 403
    rows = {row[0]: row for row in obtener_archivos(report_id)}
    ruta = Path(rows[formato][1])
    if not ruta.is_file() or REPORTS_DIR not in ruta.parents:
        return jsonify({"error": "Archivo no disponible."}), 404
    return send_file(ruta, as_attachment=True)


@app.get("/health")
def health():
    return jsonify({"status": "ok", "version": "5.0"})


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1", port=int(os.getenv("PORT", "5000")))
