import os
from datetime import datetime
from zoneinfo import ZoneInfo

from api import obtener_precios, construir_reporte
from config import (
    CRIPTOS, OUTPUT_DIR, ARCHIVO_SALIDA, ARCHIVO_CSV, ARCHIVO_HTML,
    ARCHIVO_PDF, ARCHIVO_GRAFICO_ACTUAL, ARCHIVO_GRAFICO_HISTORICO,
)
from database import (
    inicializar_db, guardar_precios, obtener_historial,
    obtener_precio_anterior,
)
from exportadores import exportar_excel, exportar_csv, exportar_html, exportar_pdf
from graficos import generar_grafico, generar_grafico_historico

EXPORTADORES = {
    "excel": (ARCHIVO_SALIDA, exportar_excel),
    "csv": (ARCHIVO_CSV, exportar_csv),
    "html": (ARCHIVO_HTML, exportar_html),
    "pdf": (ARCHIVO_PDF, exportar_pdf),
}


def generar_reporte(formatos=None):
    """Genera el informe v4 y exporta solo los formatos seleccionados."""
    seleccionados = list(dict.fromkeys(formatos or EXPORTADORES.keys()))
    invalidos = set(seleccionados) - set(EXPORTADORES)
    if invalidos:
        raise ValueError("Formato no válido: " + ", ".join(sorted(invalidos)))
    if not seleccionados:
        raise ValueError("Seleccioná al menos un formato de descarga.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    inicializar_db()

    precios = obtener_precios(CRIPTOS)
    if not precios:
        raise RuntimeError("No se pudieron obtener precios de CoinGecko.")

    fecha = datetime.now(
        ZoneInfo("America/Argentina/Buenos_Aires")
    ).strftime("%Y-%m-%d %H:%M")
    reporte = construir_reporte(CRIPTOS, precios, fecha, obtener_precio_anterior)
    guardar_precios(reporte)

    generar_grafico(reporte, ARCHIVO_GRAFICO_ACTUAL)
    historial = obtener_historial()
    generar_grafico_historico(historial, ARCHIVO_GRAFICO_HISTORICO)

    for formato in seleccionados:
        ruta, exportador = EXPORTADORES[formato]
        if formato == "excel":
            exportador(reporte, ruta, ARCHIVO_GRAFICO_ACTUAL, ARCHIVO_GRAFICO_HISTORICO)
        elif formato == "pdf":
            exportador(reporte, ruta, ARCHIVO_GRAFICO_ACTUAL, ARCHIVO_GRAFICO_HISTORICO)
        else:
            exportador(reporte, ruta)

    return {"reporte": reporte, "fecha": fecha, "historial": historial,
            "formatos": seleccionados}


if __name__ == "__main__":
    resultado = generar_reporte()
    print("\nREPORTE DE CRIPTOMONEDAS\n")
    for item in resultado["reporte"]:
        variacion = item["variacion"]
        variacion_texto = f" ({variacion:+.2f}%)" if variacion is not None else " (sin historial)"
        print(f"{item['nombre']}: USD {item['precio']}{variacion_texto} ({item['fecha']})")
    print("\nArchivos generados:")
    for formato in resultado["formatos"]:
        print(f"- {formato.upper()}: {EXPORTADORES[formato][0]}")
