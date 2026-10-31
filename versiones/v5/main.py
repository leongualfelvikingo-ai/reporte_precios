import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from api import obtener_top_criptos, obtener_precios, construir_reporte
from config import DEFAULT_TIMEZONE, REPORTS_DIR
from database import crear_reporte, guardar_precios, obtener_historial, obtener_precio_anterior, registrar_archivo
from exportadores import exportar_csv, exportar_excel, exportar_html, exportar_pdf
from graficos import generar_grafico, generar_grafico_historico


def generar_reporte(timezone_name=DEFAULT_TIMEZONE, language="es", currency="usd", crypto_ids=None):
    report_id = uuid.uuid4().hex
    ids = list(crypto_ids or obtener_top_criptos())
    precios = obtener_precios(ids)
    ahora = datetime.now(ZoneInfo(timezone_name)).strftime("%Y-%m-%d %H:%M")
    owner_token = crear_reporte(report_id, ids, timezone_name, language, currency)
    reporte = construir_reporte(ids, precios, ahora, obtener_precio_anterior)
    guardar_precios(reporte, report_id)
    historial = obtener_historial(report_id)
    report_dir = REPORTS_DIR / report_id
    report_dir.mkdir(parents=True, exist_ok=True)
    actual = report_dir / "grafico_precios.png"
    historico = report_dir / "grafico_historico.png"
    generar_grafico(reporte, str(actual))
    generar_grafico_historico(historial, str(historico))
    paths = {
        "excel": report_dir / "reporte.xlsx", "csv": report_dir / "reporte.csv",
        "html": report_dir / "reporte.html", "pdf": report_dir / "reporte.pdf",
    }
    exportar_excel(reporte, str(paths["excel"]), str(actual), str(historico))
    exportar_csv(reporte, str(paths["csv"]))
    exportar_html(reporte, str(paths["html"]))
    exportar_pdf(reporte, str(paths["pdf"]), str(actual), str(historico))
    download_tokens = {fmt: registrar_archivo(report_id, fmt, path) for fmt, path in paths.items()}
    return {"id": report_id, "owner_token": owner_token, "download_tokens": download_tokens, "reporte": reporte, "fecha": ahora, "historial": historial, "paths": paths}


if __name__ == "__main__":
    result = generar_reporte()
    print(f"Informe generado: {result['id']}")
    for item in result["reporte"]:
        print(f"{item['ranking']}. {item['nombre']}: USD {item['precio']}")
