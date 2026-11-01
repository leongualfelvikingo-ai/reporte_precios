# Reporte Automático de Criptomonedas — v4

La v4 es una aplicación web local para consultar los precios en USD de las tres criptomonedas fijas configuradas, registrar el historial y generar informes descargables.

## Funciones

- Interfaz web local: la página inicial no consulta la API ni genera archivos automáticamente.
- Botón explícito para generar un informe.
- Selección de uno o varios formatos: PDF, Excel, CSV y HTML.
- Solo se generan los formatos seleccionados.
- Registro del historial en SQLite.
- Gráfico de precios actuales y gráfico histórico.
- Inclusión de los gráficos en las exportaciones PDF y Excel.
- Mensajes controlados ante errores de conexión o generación.
- Endpoint de comprobación: `/health`.

## Variación de precio

La variación se calcula frente al último precio guardado para cada activo en la base SQLite. No es una variación de 24 horas garantizada: el intervalo depende de cuándo se hayan guardado los informes anteriores.

## Ejecutar localmente

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Abrí http://127.0.0.1:5000/.

También se puede generar el informe desde la terminal con:

```bash
python main.py
```

## Límites de la v4

- Mantiene la lista fija de tres activos de `config.py`.
- Usa almacenamiento local en `output/`; no es un servicio multiusuario desplegado.
- No incluye ranking dinámico por capitalización, informes aislados por cliente, tokens individuales, cuentas, pagos ni integración con Mercado Pago.
- La selección de formatos controla la generación y descarga; no representa una compra ni un cobro.
- Los datos dependen de CoinGecko. El proyecto no ofrece asesoramiento financiero.

## Versión 5

El código de la evolución avanzada se conserva por separado en [`versiones/v5/`](versiones/v5/README.md). No reemplaza ni se mezcla con la ejecución de v4.
