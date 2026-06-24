import requests


def obtener_precios(criptos):
    ids = ",".join(criptos)

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={ids}&vs_currencies=usd"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()

        return response.json()

    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return None


def construir_reporte(criptos, data, ahora):
    from database import obtener_precio_anterior
    reporte = []
    for cripto in criptos:
        precio = data.get(cripto, {}).get("usd", "No disponible")
        anterior = obtener_precio_anterior(cripto.capitalize())
        variacion = calcular_variacion(precio, anterior)
        reporte.append({
            "nombre": cripto.capitalize(),
            "precio": precio,
            "fecha": ahora,
            "variacion": variacion
        })
    return reporte

def calcular_variacion(precio_actual, precio_anterior):
    if precio_anterior is None:
        return None
    variacion = ((precio_actual - precio_anterior) / precio_anterior) * 100
    return round(variacion, 2)