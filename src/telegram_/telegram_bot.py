import time
import html
import requests
from src.core import logger
from core.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, DEBUG_MODE, MAX_RETRIES_TG, PARSE_MODE

def send_message(text: str, parse_mode=None, chat_id=None, retries=None):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.log("[TELEGRAM] Credenciales no configuradas.")
        return

    parse_mode = parse_mode or PARSE_MODE
    retries = retries or MAX_RETRIES_TG
    chat_id = chat_id or TELEGRAM_CHAT_ID

    if parse_mode == "HTML":
        text = html.escape(text, quote=False)

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }

    if DEBUG_MODE:
        logger.log(f"[TELEGRAM] Payload: {payload}")

    for attempt in range(1, retries + 1):
        try:
            r = requests.post(url, json=payload, timeout=10)
            r.raise_for_status()
            logger.log(f"[TELEGRAM] Mensaje enviado correctamente (intento {attempt}).")
            return
        except Exception as e:
            logger.log(f"[TELEGRAM] Error al enviar (intento {attempt}): {e}")
            if attempt < retries:
                time.sleep(2 ** attempt)