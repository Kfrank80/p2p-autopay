# private_client.py

import os
import time
import hmac
import hashlib
import logging
import requests
import urllib.parse
from typing import Any, Dict, List, Optional
from core.config import BINANCE_API_KEY, BINANCE_API_SECRET

# 📌 Endpoint privado de historial C2C de Binance
BINANCE_PRIVATE_URL = "https://api.binance.com/sapi/v1/c2c/orderMatch/listUserOrderHistory"



def _sign_payload(params: Dict[str, Any]) -> str:
    """
    Firma los parámetros con HMAC-SHA256 y devuelve el querystring firmado.
    """
    query_string = urllib.parse.urlencode(params, doseq=True)
    signature = hmac.new(
        BINANCE_API_SECRET.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return f"{query_string}&signature={signature}"


def fetch_private_orders(
    page: int = 1,
    rows: int = 10,
    trade_type: Optional[str] = None,   # "BUY" o "SELL"
    status: Optional[str] = None        # "COMPLETED", "PENDING", etc.
) -> List[Dict[str, Any]]:
    """
    Consulta el historial privado de órdenes P2P del usuario autenticado.
    Devuelve una lista de órdenes normalizadas o [] en caso de error.
    """
    if not BINANCE_API_KEY or not BINANCE_API_SECRET:
        logging.error("❌ BINANCE_API_KEY o BINANCE_API_SECRET no configuradas.")
        return []

    # Asegurar rangos válidos
    page = max(1, page)
    rows = max(1, min(rows, 100))

    # Parámetros de la petición
    params: Dict[str, Any] = {
        "timestamp": int(time.time() * 1000),
        "recvWindow": 5000,
        "page": page,
        "rows": rows
    }
    if trade_type:
        params["tradeType"] = trade_type
    if status:
        params["orderStatus"] = status

    signed_query = _sign_payload(params)
    url = f"{BINANCE_PRIVATE_URL}?{signed_query}"
    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}

    logging.debug(f"[BINANCE][PRIVATE] GET {url}")

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        # Algunos endpoints devuelven código y mensaje en 200
        if isinstance(data, dict) and data.get("code") not in (None, 200):
            logging.error(f"[BINANCE][PRIVATE] API error code={data.get('code')}, msg={data.get('msg')}")
            return []

        raw = data.get("data", [])
        logging.info(f"[BINANCE][PRIVATE] Órdenes obtenidas: {len(raw)}")
        return _normalize_orders(raw)

    except requests.RequestException as e:
        logging.error(f"[BINANCE][PRIVATE] Error de red: {e}")
    except ValueError as e:
        logging.error(f"[BINANCE][PRIVATE] Error parseando JSON: {e}")
    except Exception as e:
        logging.error(f"[BINANCE][PRIVATE] Error inesperado: {e}")

    return []


def _normalize_orders(raw_orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Normaliza la estructura de órdenes para consumo interno uniforme.
    """
    normalized: List[Dict[str, Any]] = []
    for o in raw_orders:
        normalized.append({
            "orderNumber": o.get("orderNumber"),
            "asset": o.get("asset"),
            "fiat": o.get("fiat"),
            "tradeType": o.get("tradeType"),
            "orderStatus": o.get("orderStatus"),
            "price": float(o.get("price", 0)),
            "amount": float(o.get("amount", 0)),
            "createTime": o.get("createTime"),
            "updateTime": o.get("transactTime") or o.get("updateTime"),
            "counterparty": o.get("counterPartNickName") or o.get("advertiserNickName")
        })
    return normalized