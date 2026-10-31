# Reporte Automático de Criptomonedas v6.0

Generador informativo de informes con las diez criptomonedas de mayor capitalización disponibles en CoinGecko. Cada operación conserva su selección de activos, precios, gráficos e informes PDF, Excel, HTML y CSV en una carpeta independiente.

## Ranking y datos
La selección dinámica consulta CoinGecko por capitalización de mercado. Cada informe registra si el ranking provino de CoinGecko o de la lista fallback. Si se usa el respaldo, debe indicarse que no se pudo recuperar el ranking dinámico. El ranking puede incluir stablecoins y activos derivados; no es una recomendación de compra o inversión.

## Ejecución local
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
python app.py
```
Abrí http://127.0.0.1:5000/. El modo demo está desactivado por defecto. Para habilitarlo solo en pruebas locales:
```bash
DEMO_PAYMENTS_ENABLED=1 python app.py
```
No habilitar el modo demo en un despliegue público.

## Seguridad
- GET / solo muestra la interfaz; no genera informes.
- POST /generar crea un informe solo si el modo demo está habilitado.
- El token propietario se envía en Authorization: Bearer TOKEN.
- El token de descarga se envía en X-Download-Token.
- Los tokens no se aceptan en query strings.
- Los tokens de propietario vencen a las 24 horas y los de descarga a los 15 minutos desde su emisión al simular el pago.
- Las respuestas públicas no exponen rutas físicas.
- La ruta del archivo se valida dentro del directorio privado de informes.

El modo demo no cobra dinero. En producción, el pago debe confirmarse en el backend mediante el proveedor y un webhook validado.

## Localización
La estructura acepta los campos es/en y una zona horaria configurable, pero la traducción integral sigue pendiente. USD es la única moneda implementada; las conversiones locales están pendientes.

## Pruebas
```bash
python -m unittest -v test_reporte.py
python -m compileall -q .
```
Si Flask no está instalado, instalar dependencias con pip install -r requirements.txt. La prueba web se omite explícitamente cuando falta Flask.

## Pendiente antes de producción
No hay integración real con Mercado Pago, cuentas reales, webhooks firmados, reembolsos, contracargos, hosting permanente, almacenamiento privado externo, CSRF, rate limiting ni pruebas de concurrencia. Los plazos de tokens son valores iniciales que deben revisarse. Esta versión no debe recibir pagos reales ni exponerse públicamente.
