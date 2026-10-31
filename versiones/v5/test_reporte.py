import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


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

    def test_api_y_reporte_tienen_diez_activos(self):
        from api import construir_reporte
        ids = ["bitcoin", "ethereum", "tether", "binancecoin", "solana", "usd-coin", "ripple", "staked-ether", "dogecoin", "cardano"]
        report = construir_reporte(ids, {item: index + 1 for index, item in enumerate(ids)}, "2026-10-31 10:00")
        self.assertEqual(len(report), 10)
        self.assertEqual(report[3]["nombre"], "BNB")

    def test_api_incompleta_no_rompe(self):
        from api import construir_reporte
        report = construir_reporte(["bitcoin"], {"bitcoin": "No disponible"}, "now")
        self.assertIsNone(report[0]["variacion"])

    def test_persistencia_y_permisos(self):
        from database import inicializar_db, crear_reporte, registrar_archivo, marcar_pagado, autorizar_descarga
        inicializar_db()
        owner = crear_reporte("abc", ["bitcoin"], "UTC", "es", "usd")
        token = registrar_archivo("abc", "pdf", "/tmp/report.pdf")
        self.assertFalse(autorizar_descarga("abc", "pdf", token))
        self.assertTrue(marcar_pagado("abc", "pdf"))
        self.assertTrue(autorizar_descarga("abc", "pdf", token))
        self.assertFalse(autorizar_descarga("abc", "pdf", "incorrecto"))
        self.assertTrue(owner)

    @patch("api.obtener_top_criptos", return_value=["bitcoin"])
    @patch("api.obtener_precios", return_value={"bitcoin": 100})
    def test_flask_separa_generacion_y_bloquea_descarga(self, _prices, _top):
        from app import app
        client = app.test_client()
        self.assertEqual(client.get("/").status_code, 200)
        response = client.post("/generar")
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["crypto_count"], 1)
        self.assertEqual(client.get(f"/descargar/{data['report_id']}/pdf?token=bad").status_code, 403)


if __name__ == "__main__":
    unittest.main()
