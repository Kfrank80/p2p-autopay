import logging
import sys
from core.config import MONITOR_MODE
from core.order_monitor import monitor_orders

def main():
    # Si el usuario pasa un argumento, ese modo prevalece sobre .env
    mode = sys.argv[1] if len(sys.argv) > 1 else MONITOR_MODE

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    logging.info("🚀 Bot Binance P2P Autopay iniciado.")
    logging.info(f"Modo de monitorización: {mode}")

    try:
        monitor_orders_override(mode)
    except KeyboardInterrupt:
        logging.info("🛑 Ejecución interrumpida por el usuario.")
    except Exception as e:
        logging.error(f"❌ Error fatal en main.py: {e}")

def monitor_orders_override(mode):
    """
    Llama al monitor de órdenes con el modo forzado.
    """
    from core.order_monitor import monitor_orders as base_monitor
    from core.config import STATE_FILE, MONITOR_INTERVAL
    import core.order_monitor as om

    # Guardamos modo original y forzamos temporalmente
    original_mode = om.MONITOR_MODE if hasattr(om, "MONITOR_MODE") else None
    om.MONITOR_MODE = mode
    base_monitor()
    # Restaurar si es necesario (normalmente no se alcanza por loop infinito)
    if original_mode is not None:
        om.MONITOR_MODE = original_mode

if __name__ == "__main__":
    main()
