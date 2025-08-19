import time
from src.core import logger
from core.config import CHECK_INTERVAL, MIN_AMOUNT, PAYMENT_METHODS, DEBUG_MODE
from binance.binance_client import get_p2p_orders
from telegram_.telegram_bot import send_message

def main():
    logger.log("🚀 Bot Binance P2P iniciado.")

    while True:
        if DEBUG_MODE:
            logger.log(f"🔍 Verificando órdenes... Mínimo: {MIN_AMOUNT}, Métodos: {PAYMENT_METHODS}")

        orders = get_p2p_orders(
            trade_type="Buy",
            asset="USDT",
            fiat="USD",
            pay_types=PAYMENT_METHODS
        )

        if not orders:
            logger.log("⚠️ No se encontraron órdenes que coincidan con los filtros.")
        else:
            for order in orders:
                price = order["adv"]["price"]
                available = float(order["adv"]["surplusAmount"])
                advertiser = order["advertiser"]["nickName"]

                if available >= MIN_AMOUNT:
                    mensaje = f"💰 Orden encontrada: {advertiser} vende {available} USDT a {price} USD"
                    logger.log(f"[MATCH] {mensaje}")
                    send_message(mensaje)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.log("🛑 Bot detenido por el usuario.")
