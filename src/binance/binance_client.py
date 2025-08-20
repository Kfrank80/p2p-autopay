import requests
from src.core import logger
from core.config import DEBUG_MODE, PAYMENT_METHODS

def get_p2p_orders(trade_type="BUY", asset="USDT", fiat="USD", pay_types=PAYMENT_METHODS):
    """
    Consulta órdenes activas en Binance P2P.
    """
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "asset": asset,
        "fiat": fiat,
        "tradeType": trade_type,
        "payTypes": pay_types or [],
        "page": 1,
        "rows": 5
    }

    if DEBUG_MODE:
        logger.log(f"[BINANCE] Payload: {payload}")

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        logger.log(f"[BINANCE] Error consultando órdenes P2P: {e}")
        return []
