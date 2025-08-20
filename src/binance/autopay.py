# autopay.py
import time
from binance.private_client import _sign_payload
import requests
from core.config import BINANCE_RELEASE_ENDPOINT, BINANCE_API_SECRET, BINANCE_API_KEY

def is_valid_order(order):
    return (
        not order["is_my_order"] and
        order["status"] == "PAID" and
        order["amount"] > 0
    )

def release_payment(order_id):
    timestamp = int(time.time() * 1000)
    payload = {
        "orderId": order_id,
        "timestamp": timestamp
    }
    signature = _sign_payload(payload)
    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }
    response = requests.post(
        BINANCE_RELEASE_ENDPOINT,
        params={**payload, "signature": signature},
        headers=headers
    )
    return response.json()
