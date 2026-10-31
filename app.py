import logging
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file

from config import DEFAULT_TIMEZONE, REPORTS_DIR, SUPPORTED_LANGUAGES
from database import autorizar_descarga, marcar_pagado, obtener_archivos, obtener_estado_archivos, obtener_fuente_ranking, validar_propietario
from main import generar_reporte

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("reporte_precios")
# Fail closed: demo solo se habilita cuando se configura explícitamente.
DEMO_PAYMENTS_ENABLED = os.getenv("DEMO_PAYMENTS_ENABLED", "0") == "1"


def _error_id():
    import uuid
    return f"REP-{uuid.uuid4().hex[:10].upper()}"


def _owner_token():
    value = request.headers.get("Authorization", "")
    return value[7:].strip() if value.startswith("Bearer ") else ""


def _authorized(report_id):
    return validar_propietario(report_id, _owner_token())


@app.get("/")
def index():
    return render_template("index.html", demo_payments=DEMO_PAYMENTS_ENABLED)


@app.post("/generar")
def generar():
    if not DEMO_PAYMENTS_ENABLED:
        return jsonify({"error": "La generación requiere un pago confirmado por el proveedor configurado."}), 402
    try:
        language = request.form.get("language", "es")
        timezone_name = request.form.get("timezone", DEFAULT_TIMEZONE)
        if language not in SUPPORTED_LANGUAGES:
            language = "es"
        result = generar_reporte(timezone_name=timezone_name, language=language)
        return jsonify({
            "report_id": result["id"],
            "owner_token": result["owner_token"],
            "view_url": f"/reporte/{result['id']}",
            "crypto_count": len(result["reporte"]),
            "ranking_source": result["ranking_source"],
            "ranking_notice": ("No se pudo consultar el ranking dinámico. Se utilizó la lista de respaldo disponible." if result["ranking_source"] == "fallback" else None),
        }), 201
    except Exception:
        error_id = _error_id()
        logger.exception("Fallo de generación %s", error_id)
        return jsonify({"error": "No se pudo generar el informe.", "error_id": error_id}), 503


@app.get("/reporte/<report_id>")
def ver_reporte(report_id):
    if not _authorized(report_id):
        return jsonify({"error": "Informe no autorizado o token vencido."}), 403
    from database import obtener_historial
    return jsonify({
        "report_id": report_id,
        "historial": obtener_historial(report_id),
        "archivos": obtener_estado_archivos(report_id),
        "ranking_source": obtener_fuente_ranking(report_id),
    })


@app.post("/demo/pagar/<report_id>/<formato>")
def pagar_demo(report_id, formato):
    if not DEMO_PAYMENTS_ENABLED:
        return jsonify({"error": "Los pagos demo están desactivados."}), 404
    if not _authorized(report_id):
        return jsonify({"error": "Informe no autorizado o token vencido."}), 403
    if formato not in {"excel", "csv", "html", "pdf"}:
        return jsonify({"error": "Formato no disponible."}), 404
    download_token = marcar_pagado(report_id, formato)
    if not download_token:
        return jsonify({"error": "Formato no disponible."}), 404
    return jsonify({
        "paid": True,
        "download_url": f"/descargar/{report_id}/{formato}",
        "download_token": download_token,
        "expires_in_seconds": 900,
    })


@app.get("/descargar/<report_id>/<formato>")
def descargar(report_id, formato):
    if formato not in {"excel", "csv", "html", "pdf"}:
        return jsonify({"error": "Descarga no autorizada."}), 403
    token = request.headers.get("X-Download-Token", "").strip()
    if not autorizar_descarga(report_id, formato, token):
        return jsonify({"error": "Descarga no autorizada o token vencido."}), 403
    rows = {row[0]: row for row in obtener_archivos(report_id)}
    if formato not in rows:
        return jsonify({"error": "Archivo no disponible."}), 404
    ruta = Path(rows[formato][1]).resolve()
    base = REPORTS_DIR.resolve()
    if base not in ruta.parents or not ruta.is_file():
        logger.warning("Ruta de archivo no válida para informe %s", report_id)
        return jsonify({"error": "Archivo no disponible."}), 404
    return send_file(ruta, as_attachment=True)


@app.get("/health")
def health():
    return jsonify({"status": "ok", "version": "6.0"})


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1", port=int(os.getenv("PORT", "5000")))
