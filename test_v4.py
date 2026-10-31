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
    @patch("main.obtener_precios", return_value={"bitcoin": 100})
    @patch("main.construir_reporte", return_value=[{
        "nombre": "Bitcoin", "precio": 100, "fecha": "2026-10-31 12:00",
        "variacion": None,
    }])
    def test_exporta_solo_el_formato_seleccionado(
        self, _report, _prices, _db, _save, _history, _chart,
        _history_chart, _pdf, _html, _excel, csv_export
    ):
        result = main.generar_reporte(["csv"])
        self.assertEqual(result["formatos"], ["csv"])
        csv_export.assert_called_once()
        _pdf.assert_not_called()
        _html.assert_not_called()
        _excel.assert_not_called()

    def test_rechaza_formato_desconocido(self):
        with self.assertRaises(ValueError):
            main.generar_reporte(["doc"])

    def test_exige_al_menos_un_formato(self):
        with self.assertRaises(ValueError):
            main.generar_reporte([])


if __name__ == "__main__":
    unittest.main()
