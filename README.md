# Reporte Automático de Criptomonedas — v4

La v4 es una aplicación web sencilla para consultar las tres criptomonedas configuradas, revisar su precio en USD y su variación frente al último dato guardado, y descargar un informe en los formatos seleccionados.

## Funciones incluidas

- Interfaz web local con botón explícito para generar el informe.
- Selección de PDF, Excel, CSV y HTML antes de generar.
- Registro del historial en SQLite.
- Gráfico de precios actuales y gráfico histórico.
- Inclusión de gráficos en las exportaciones PDF y Excel.
- Mensajes controlados cuando la API no responde o faltan precios.

## Ejecutar

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Abrí http://127.0.0.1:5000/.

También se puede ejecutar sin interfaz web:

```bash
python main.py
```

## Alcance de esta versión

La v4 mantiene la lista fija de tres activos configurados en `config.py`. No incluye ranking dinámico por capitalización, informes aislados por cliente, tokens individuales de descarga, autorización de pagos ni integración con Mercado Pago. Esas capacidades pertenecen a la evolución v5 y posteriores.

La selección de formatos en v4 controla qué archivos se generan y quedan disponibles para descargar. No representa una compra ni un cobro.

## Limitaciones

- La aplicación usa almacenamiento local en la carpeta `output/`; no es un servicio multiusuario desplegado.
- No hay cuentas, autenticación ni pagos.
- La base de datos conserva el historial en el entorno donde se ejecuta.
- Los datos dependen de la disponibilidad de CoinGecko.
- El proyecto es informativo y no ofrece asesoramiento financiero.
