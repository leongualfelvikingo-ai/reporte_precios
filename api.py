import requests

API_URL = "https://api.coingecko.com/api/v3/simple/price"
API_TIMEOUT_SECONDS = 15


def obtener_precios(criptos):
    params = {
        "ids": ",".join(criptos),
        "vs_currencies": "usd",
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=API_TIMEOUT_SECONDS,
        headers={"User-Agent": "reporte-precios/4.0"},
    )

    response.raise_for_status()

    data = response.json()

    if not isinstance(data, dict):
        raise ValueError("La API devolvió un formato de datos inválido.")

    precios = {}

    for cripto in criptos:
        precio = data.get(cripto, {}).get("usd")

        if not isinstance(precio, (int, float)):
            precio = "No disponible"

        precios[cripto] = precio

    return precios


def calcular_variacion(precio_actual, precio_anterior):
    if not isinstance(precio_actual, (int, float)):
        return None

    if not isinstance(precio_anterior, (int, float)) or precio_anterior == 0:
        return None

    return ((precio_actual - precio_anterior) / precio_anterior) * 100


def construir_reporte(criptos, precios, fecha, obtener_anterior=None):
    reporte = []

    for cripto in criptos:
        precio = precios.get(cripto)

        precio_anterior = None

        if obtener_anterior is not None:
            precio_anterior = obtener_anterior(cripto)

        variacion = calcular_variacion(
            precio,
            precio_anterior
        )

        reporte.append({
            "nombre": cripto.capitalize(),
            "precio": precio,
            "fecha": fecha,
            "variacion": variacion,
        })

    return reporte
