import os
from dotenv import load_dotenv

# Carga de variables de entorno desde .env
load_dotenv()

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

# Nuevas variables para envío robusto
MAX_RETRIES_TG = int(os.getenv("MAX_RETRIES_TG", "3"))
PARSE_MODE = os.getenv("PARSE_MODE", "HTML")

# Monitor
MONITOR_INTERVAL = int(os.getenv("MONITOR_INTERVAL", "30"))
MONITOR_MODE = os.getenv("MONITOR_MODE", "public")
STATE_FILE = os.getenv("STATE_FILE", "state.json")

# Binance API (para modo privado)
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")

PAYMENT_METHODS = [
    m.strip() for m in os.getenv("PAYMENT_METHODS", "Zelle").split(",") if m.strip()
]