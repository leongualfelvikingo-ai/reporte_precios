import os
import tempfile
import unittest
from unittest.mock import patch

import main


class ReporteV4Tests(unittest.TestCase):
    @patch("main.exportar_csv")
    @patch("main.exportar_excel")
    @patch("main.exportar_html")
    @patch("main.exportar_pdf")
    @patch("main.generar_grafico_historico")
    @patch("main.generar_grafico")
    @patch("main.obtener_historial", return_value=[])
    @patch("main.guardar_precios")
    @patch("main.inicializar_db")
    @patch("main.obtener_precios", return_value={"bitcoin": 100, "ethereum": 200, "litecoin": 50})
    @patch("main.construir_reporte", return_value=[{
        "nombre": "Bitcoin", "precio": 100, "fecha": "2026-10-31 12:00",
        "variacion": None,
    }])
    def test_exporta_solo_el_formato_seleccionado(
        self, _reporte, _precios, _db, _guardar, _historial, _grafico,
        _grafico_historico, _pdf, _html, _excel, exportar_csv
    ):
        resultado = main.generar_reporte(["csv", "csv"])
        self.assertEqual(resultado["formatos"], ["csv"])
        exportar_csv.assert_called_once()
        _pdf.assert_not_called()
        _html.assert_not_called()
        _excel.assert_not_called()

    def test_rechaza_formato_desconocido(self):
        with self.assertRaises(ValueError):
            main.generar_reporte(["doc"])

    def test_exige_al_menos_un_formato(self):
        with self.assertRaises(ValueError):
            main.generar_reporte([])


class InterfazV4Tests(unittest.TestCase):
    def setUp(self):
        import app as modulo_app
        self.modulo_app = modulo_app
        self.client = modulo_app.app.test_client()
        modulo_app.formatos_disponibles = set()

    def test_inicio_no_genera_informe(self):
        with patch.object(self.modulo_app, "generar_reporte") as generar:
            respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)
        generar.assert_not_called()

    def test_descarga_solo_formato_generado(self):
        with tempfile.NamedTemporaryFile(delete=False) as archivo:
            ruta = archivo.name
        self.addCleanup(lambda: os.path.exists(ruta) and os.remove(ruta))
        with patch.dict(self.modulo_app.RUTAS_DESCARGA, {"csv": ruta}):
            self.modulo_app.formatos_disponibles = {"csv"}
            self.assertEqual(self.client.get("/descargar/csv").status_code, 200)
            self.assertEqual(self.client.get("/descargar/pdf").status_code, 404)

    def test_fallo_no_conserva_descargas_anteriores(self):
        self.modulo_app.formatos_disponibles = {"csv"}
        with patch.object(self.modulo_app, "generar_reporte", side_effect=RuntimeError("fallo")):
            respuesta = self.client.post("/generar", data={"formatos": "pdf"})
        self.assertEqual(respuesta.status_code, 503)
        self.assertEqual(self.modulo_app.formatos_disponibles, set())


if __name__ == "__main__":
    unittest.main()
