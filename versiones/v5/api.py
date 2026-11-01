import requests

from config import CRIPTOS_FALLBACK, TOP_CRYPTO_LIMIT

API_BASE = "https://api.coingecko.com/api/v3"
API_TIMEOUT_SECONDS = 15
USER_AGENT = "reporte-precios/5.0"
NOMBRES_CRIPTOS = {
    "bitcoin": "Bitcoin", "ethereum": "Ethereum", "tether": "Tether",
    "binancecoin": "BNB", "solana": "Solana", "usd-coin": "USD Coin",
    "ripple": "XRP", "staked-ether": "Lido Staked Ether", "dogecoin": "Dogecoin",
    "cardano": "Cardano", "litecoin": "Litecoin", "polkadot": "Polkadot",
    "chainlink": "Chainlink",
}


def _get(path, params=None):
    response = requests.get(
        f"{API_BASE}{path}", params=params, timeout=API_TIMEOUT_SECONDS,
        headers={"User-Agent": USER_AGENT},
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, (dict, list)):
        raise ValueError("La API devolvió un formato inválido.")
    return data


def obtener_top_criptos(limit=TOP_CRYPTO_LIMIT):
    """Devuelve IDs ordenados por capitalización; usa fallback ante error de ranking."""
    try:
        data = _get("/coins/markets", {"vs_currency": "usd", "order": "market_cap_desc", "per_page": limit, "page": 1, "sparkline": "false"})
        ids = [item.get("id") for item in data if isinstance(item, dict) and item.get("id")]
        if len(ids) >= limit:
            return ids[:limit]
    except (requests.RequestException, ValueError, TypeError):
        pass
    return CRIPTOS_FALLBACK[:limit]


def obtener_precios(criptos):
    if not criptos:
        return {}
    data = _get("/simple/price", {"ids": ",".join(criptos), "vs_currencies": "usd"})
    precios = {}
    for cripto in criptos:
        registro = data.get(cripto) if isinstance(data, dict) else None
        precio = registro.get("usd") if isinstance(registro, dict) else None
        precios[cripto] = precio if isinstance(precio, (int, float)) else "No disponible"
    return precios


def calcular_variacion(precio_actual, precio_anterior):
    if not isinstance(precio_actual, (int, float)) or not isinstance(precio_anterior, (int, float)) or precio_anterior == 0:
        return None
    return round(((precio_actual - precio_anterior) / precio_anterior) * 100, 2)


def construir_reporte(criptos, precios, fecha, obtener_anterior=None):
    reporte = []
    for posicion, cripto in enumerate(criptos, start=1):
        precio = precios.get(cripto)
        anterior = obtener_anterior(cripto) if obtener_anterior else None
        reporte.append({
            "id": cripto,
            "ranking": posicion,
            "nombre": NOMBRES_CRIPTOS.get(cripto, cripto.replace("-", " ").title()),
            "precio": precio,
            "fecha": fecha,
            "variacion": calcular_variacion(precio, anterior),
        })
    return reporte
