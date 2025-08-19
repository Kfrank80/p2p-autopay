# core/order_monitor.py
import time
import logging
from binance.binance_client import get_p2p_orders
from telegram_.telegram_bot import send_message
from core.state import OrderState

def monitor_orders(interval=30):
    state = OrderState()
    logging.info("Iniciando monitor de órdenes...")

    while True:
        try:
            orders = get_p2p_orders()
            new_orders = state.update(orders)

            for order_id in new_orders:
                adv = next((o['adv'] for o in orders if o['adv']['advNo'] == order_id), None)
                if adv:
                    msg = f"📢 Nueva orden detectada:\n{adv['price']} USD por {adv['asset']}\nMétodo: {adv['tradeMethods'][0]['tradeMethodName']}"
                    send_message(msg)
                    logging.info(f"Orden nueva: {adv['advNo']}")

        except Exception as e:
            logging.error(f"Error en monitor: {e}")

        time.sleep(interval)
