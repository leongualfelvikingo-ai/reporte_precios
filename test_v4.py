import unittest
from unittest.mock import patch

import main


class GeneracionV4Tests(unittest.TestCase):
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
    @patch("main.construir_reporte", return_value=[
        {"nombre": "Bitcoin", "precio": 100, "fecha": "2026-10-31 12:00", "variacion": None}
    ])
    def test_solo_exporta_formatos_seleccionados(
        self, _reporte, _precios, _db, _guardar, _historial, _grafico,
        _grafico_historico, _pdf, _html, _excel, exportar_csv
    ):
        resultado = main.generar_reporte(["csv"])
        self.assertEqual(resultado["formatos"], ["csv"])
        exportar_csv.assert_called_once()
        _pdf.assert_not_called()
        _html.assert_not_called()
        _excel.assert_not_called()

    def test_lista_vacia_no_genera_todos_los_formatos(self):
        with self.assertRaises(ValueError):
            main.generar_reporte([])

    def test_rechaza_formato_desconocido(self):
        with self.assertRaises(ValueError):
            main.generar_reporte(["doc"])


if __name__ == "__main__":
    unittest.main()
