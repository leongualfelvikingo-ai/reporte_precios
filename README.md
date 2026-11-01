# Reporte Automático de Criptomonedas — v4

La v4 combina el generador original de tres criptomonedas con una interfaz web local que permite elegir qué archivos generar.

## Funciones integradas
- Consulta de Bitcoin, Ethereum y Litecoin mediante CoinGecko.
- Historial local SQLite y variación frente al último registro guardado.
- Gráfico de precios actuales e histórico.
- Generación seleccionable de PDF, Excel, CSV y HTML.
- Los gráficos se incorporan a PDF y Excel.
- La página inicial no genera informes: la generación ocurre al pulsar el botón.
- Descargas habilitadas solo para los formatos generados en la última operación exitosa.

## Ejecutar
```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Abrí http://127.0.0.1:5000/.

También se puede generar todo desde la terminal con `python main.py`.

## Aclaración sobre la variación
La variación compara el precio actual con el último registro almacenado. El intervalo depende de cuándo se generó el informe anterior; no debe interpretarse automáticamente como variación de 24 horas.

## Alcance de v4
Se mantienen tres activos fijos y almacenamiento local. No se incorporan ranking dinámico, operaciones aisladas por cliente, cuentas, tokens de descarga ni pagos de v5.
