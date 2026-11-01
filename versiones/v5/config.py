from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "output"
REPORTS_DIR = OUTPUT_DIR / "reportes"

NOMBRE_PROYECTO = "Reporte Automático de Criptomonedas"
VERSION = "5.0"
TOP_CRYPTO_LIMIT = 10
DEFAULT_TIMEZONE = "America/Argentina/Buenos_Aires"
DEFAULT_CURRENCY = "usd"
SUPPORTED_LANGUAGES = {"es", "en"}
SUPPORTED_CURRENCIES = {"usd"}

CRIPTOS_FALLBACK = [
    "bitcoin", "ethereum", "tether", "binancecoin", "solana",
    "usd-coin", "xrp", "staked-ether", "dogecoin", "cardano",
]
CRIPTOS = CRIPTOS_FALLBACK

ARCHIVO_SALIDA = str(OUTPUT_DIR / "reporte.xlsx")
ARCHIVO_CSV = str(OUTPUT_DIR / "reporte.csv")
ARCHIVO_HTML = str(OUTPUT_DIR / "reporte.html")
ARCHIVO_PDF = str(OUTPUT_DIR / "reporte.pdf")
ARCHIVO_GRAFICO_ACTUAL = str(OUTPUT_DIR / "grafico_precios.png")
ARCHIVO_GRAFICO_HISTORICO = str(OUTPUT_DIR / "grafico_historico.png")
ARCHIVO_BASE_DATOS = str(OUTPUT_DIR / "historial.db")
