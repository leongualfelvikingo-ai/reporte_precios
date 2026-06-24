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

    reporte = []

    for cripto in criptos:

        precio = data.get(
            cripto,
            {}
        ).get(
            "usd",
            "No disponible"
        )

        reporte.append({
            "nombre": cripto.capitalize(),
            "precio": precio,
            "fecha": ahora
        })

    return reporte