# core/order_monitor.py
import time
import logging
from binance.binance_client import get_p2p_orders  # o la función privada si MONITOR_MODE='private'
from telegram_.telegram_bot import send_message
from core.state import OrderState
from core.config import MONITOR_INTERVAL, STATE_FILE, MONITOR_MODE, DEBUG_MODE, PAYMENT_METHODS

logger = logging.getLogger(__name__)


def monitor_orders():
    logger.info(f"Iniciando monitor de órdenes en modo: {MONITOR_MODE}")

    # Inicializar el estado UNA sola vez, con persistencia en disco
    if MONITOR_MODE == 'private':
        from binance.private_client import fetch_private_orders  # si tienes cliente privado
        key_func = lambda o: o['orderNumber']
        fetch_func = fetch_private_orders
    else:
        key_func = lambda o: o['adv']['advNo']
        fetch_func = get_p2p_orders

    state = OrderState(key_func=key_func, persist_path=STATE_FILE)

    while True:
        try:
            # ---- 1. Obtener órdenes ----
            if DEBUG_MODE:
                logger.debug("[BINANCE] Consultando órdenes...")

            orders = fetch_func()

            # ---- 2. Comparar con estado previo ----
            nuevas_ids = state.update(orders)

            for oid in nuevas_ids:
                # Diferenciar formato de datos según modo
                if MONITOR_MODE == 'private':
                    order_data = next((o for o in orders if o['orderNumber'] == oid), None)
                    if order_data:
                        msg = (
                            f"📢 Nueva orden privada:\n"
                            f"Monto: {order_data.get('amount')} {order_data.get('asset')}\n"
                            f"Precio: {order_data.get('price')} {order_data.get('fiat')}\n"
                            f"Método: {order_data.get('paymentMethod', 'Desconocido')}"
                        )
                else:
                    adv = next((o['adv'] for o in orders if o['adv']['advNo'] == oid), None)
                    if adv:
                        msg = (
                            f"📢 Nueva orden pública:\n"
                            f"{adv.get('price')} USD por {adv.get('asset')}\n"
                            f"Método: {adv['tradeMethods'][0]['tradeMethodName']}"
                        )

                # ---- 3. Log y envío ----
                if msg:
                    logger.info(f"Orden nueva detectada: {oid}")
                    send_message(msg)

        except Exception as e:
            logger.error(f"Error en monitor: {e}", exc_info=True)

        # ---- 4. Esperar al siguiente ciclo ----
        time.sleep(MONITOR_INTERVAL)
