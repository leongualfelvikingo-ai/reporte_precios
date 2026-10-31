# Reporte Automático de Criptomonedas v5.0

Generador de informes informativos con las 10 criptomonedas de mayor capitalización disponibles en CoinGecko. Cada operación conserva el ranking, los precios, los gráficos y los cuatro formatos en una carpeta propia.

## Flujo técnico

La selección dinámica usa `coins/markets` de CoinGecko con `market_cap_desc`. Si el ranking no está disponible, se utiliza un fallback reproducible de diez activos. El informe guarda la selección usada en esa operación para que un informe antiguo no cambie cuando cambie el mercado.

La ruta principal muestra la interfaz. La generación ocurre mediante `POST /generar`. Cada informe recibe un identificador único, un token de propietario y tokens individuales para PDF, Excel, HTML y CSV. Las descargas se rechazan hasta que el formato figure como pagado.

## Ejecución local

```bash
python -m venv .venv
pip install -r requirements.txt
# Habilitar solo para probar el flujo simulado localmente:
# Windows PowerShell: $env:DEMO_PAYMENTS_ENABLED="1"
# macOS / Linux: export DEMO_PAYMENTS_ENABLED=1
python app.py
```

Abrí `http://127.0.0.1:5000/`.

El modo demo está desactivado por defecto. No mueve dinero real. No lo habilites en un despliegue público.

## Límites

No hay integración de producción con Mercado Pago, cuentas reales, webhooks firmados, reembolsos, hosting permanente ni almacenamiento externo privado. El flujo de pago actual es solo demostrativo y requiere una revisión de seguridad antes de cualquier despliegue.
