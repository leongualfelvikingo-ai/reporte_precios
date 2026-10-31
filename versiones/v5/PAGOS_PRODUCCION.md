# Pagos y descargas — v5

La v5 incluye un circuito de demostración: genera una operación aislada, crea tokens de descarga, bloquea cada formato hasta marcarlo como pagado y permite descargar solo el formato autorizado.

El modo demo se controla con `DEMO_PAYMENTS_ENABLED=1` y no mueve dinero real. Antes de producción hay que reemplazar la ruta de pago demo por un proveedor real y confirmar el pago en el servidor mediante webhook. El navegador nunca debe ser la fuente de verdad.

## Contrato recomendado

1. Crear una orden con `report_id`, producto, importe y estado `pending`.
2. Crear la preferencia o checkout en Mercado Pago con un identificador externo único.
3. Recibir el webhook y consultar el pago en la API del proveedor.
4. Aceptar únicamente el estado aprobado y vincularlo al `report_id` y al formato.
5. Hacer la operación idempotente: el mismo evento no debe duplicar permisos.
6. Marcar el formato pagado y conservar auditoría del evento.
7. Entregar un token privado con expiración y sin exponer la ruta física.

No se deben almacenar datos de tarjetas, tokens privados ni credenciales en Git. Las variables de producción deben configurarse como secretos del entorno del hosting. La validación real, reembolsos, contracargos y firma del webhook requieren credenciales de una cuenta de producción y pruebas autorizadas.
