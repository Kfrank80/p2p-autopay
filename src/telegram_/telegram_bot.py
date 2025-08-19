import requests
from src.core import logger
from core.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, DEBUG_MODE

def send_message(text: str):
    """
    Envía un mensaje de texto a tu canal o chat de Telegram.
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.log("[TELEGRAM] Credenciales no configuradas.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    if DEBUG_MODE:
        logger.log(f"[TELEGRAM] Payload: {payload}")

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.log("[TELEGRAM] Mensaje enviado correctamente.")
    except Exception as e:
        logger.log(f"[TELEGRAM] Error al enviar mensaje: {e}")
