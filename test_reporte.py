import importlib.util
import os
import shutil
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


class ReporteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.output = Path(cls.tmp) / "output"
        os.environ["DEMO_PAYMENTS_ENABLED"] = "1"
        import config
        config.OUTPUT_DIR = cls.output
        config.REPORTS_DIR = cls.output / "reportes"
        config.ARCHIVO_BASE_DATOS = str(cls.output / "historial.db")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_reporte_tiene_diez_activos_y_nombres_legibles(self):
        from api import construir_reporte
        ids = ["bitcoin", "ethereum", "tether", "binancecoin", "solana", "usd-coin", "ripple", "staked-ether", "dogecoin", "cardano"]
        reporte = construir_reporte(ids, {item: index + 1 for index, item in enumerate(ids)}, "2026-10-31 10:00")
        self.assertEqual(len(reporte), 10)
        self.assertEqual(reporte[3]["nombre"], "BNB")

    def test_datos_incompletos_no_rompen_variacion(self):
        from api import construir_reporte
        reporte = construir_reporte(["bitcoin"], {"bitcoin": "No disponible"}, "now")
        self.assertIsNone(reporte[0]["variacion"])

    def test_tokens_expiran_y_propietario_se_revoca(self):
        import sqlite3
        import config
        from database import inicializar_db, crear_reporte, validar_propietario, registrar_archivo, marcar_pagado, autorizar_descarga, revocar_propietario
        inicializar_db()
        owner = crear_reporte("secure", ["bitcoin"], "UTC", "es", "usd", "fallback")
        self.assertTrue(validar_propietario("secure", owner))
        registrar_archivo("secure", "pdf", "/tmp/report.pdf")
        token = marcar_pagado("secure", "pdf")
        self.assertTrue(autorizar_descarga("secure", "pdf", token))
        self.assertFalse(autorizar_descarga("secure", "pdf", "incorrecto"))
        with sqlite3.connect(config.ARCHIVO_BASE_DATOS) as db:
            vencido = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()
            db.execute("UPDATE archivos SET expires_at=? WHERE report_id=? AND formato=?", (vencido, "secure", "pdf"))
        self.assertFalse(autorizar_descarga("secure", "pdf", token))
        self.assertTrue(revocar_propietario("secure"))
        self.assertFalse(validar_propietario("secure", owner))

    @unittest.skipUnless(importlib.util.find_spec("flask"), "Flask no está instalado; instalar requirements.txt para ejecutar la prueba web")
    def test_flask_no_genera_en_get_y_demo_cerrado_por_defecto(self):
        from app import app
        client = app.test_client()
        self.assertEqual(client.get("/").status_code, 200)
        self.assertEqual(client.post("/generar").status_code, 402)


if __name__ == "__main__":
    unittest.main()
