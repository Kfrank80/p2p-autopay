import requests
import logging

BINANCE_P2P_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

def fetch_orders(asset="USDT", fiat="CUP", trade_type="BUY", pay_types=None, min_amount=None):
    payload = {
        "page": 1,
        "rows": 10,
        "payTypes": pay_types or [],
        "asset": asset,
        "fiat": fiat,
        "tradeType": trade_type
    }

    try:
        response = requests.post(BINANCE_P2P_URL, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return filter_orders(data.get("data", []), min_amount)
    except Exception as e:
        logging.error(f"Error al consultar Binance P2P: {e}")
        return []

def filter_orders(orders, min_amount):
    filtered = []
    for order in orders:
        adv = order.get("adv", {})
        price = float(adv.get("price", 0))
        min_single_trans_amount = float(adv.get("minSingleTransAmount", 0))
        if min_amount is None or min_single_trans_amount >= min_amount:
            filtered.append({
                "price": price,
                "min_amount": min_single_trans_amount,
                "seller": adv.get("userName", "N/A"),
                "methods": adv.get("tradeMethods", [])
            })
    return filtered
