from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "output"

NOMBRE_PROYECTO = "Reporte Automático de Criptomonedas"
VERSION = "4.0"

CRIPTOS = ["bitcoin", "ethereum", "litecoin"]

ARCHIVO_SALIDA = str(OUTPUT_DIR / "reporte.xlsx")
ARCHIVO_CSV = str(OUTPUT_DIR / "reporte.csv")
ARCHIVO_HTML = str(OUTPUT_DIR / "reporte.html")
ARCHIVO_PDF = str(OUTPUT_DIR / "reporte.pdf")
ARCHIVO_GRAFICO_ACTUAL = str(OUTPUT_DIR / "grafico_precios.png")
ARCHIVO_GRAFICO_HISTORICO = str(OUTPUT_DIR / "grafico_historico.png")
ARCHIVO_BASE_DATOS = str(OUTPUT_DIR / "historial.db")
