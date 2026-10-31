# Pagos y descargas — v6

El circuito disponible es únicamente de demostración. Está desactivado por defecto y se habilita explícitamente con DEMO_PAYMENTS_ENABLED=1 solo para pruebas locales. No mueve dinero real.

## Contrato recomendado para producción
1. Crear una orden con informe, versión, importe y estado pendiente.
2. Crear el checkout en Mercado Pago con un identificador externo único.
3. Recibir el webhook y consultar el pago directamente en la API del proveedor.
4. Aceptar únicamente el estado aprobado y vincularlo al informe y al formato.
5. Hacer la operación idempotente para evitar permisos duplicados.
6. Registrar eventos, reembolsos, contracargos y errores.
7. Entregar permisos de descarga con vencimiento, sin exponer rutas físicas.

El token de propietario se transmite en Authorization: Bearer TOKEN; el token de descarga, en X-Download-Token. No deben enviarse en query strings. Los tokens de propietario expiran a las 24 horas y los de descarga a los 15 minutos tras emitirse al simular el pago.

No almacenar datos de tarjetas, tokens privados ni credenciales en Git. Las variables de producción deben configurarse como secretos del hosting. La integración real requiere credenciales, webhook público, validación del proveedor y pruebas autorizadas.
