import os
from dotenv import load_dotenv

load_dotenv()

# --- Binance ---
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BINANCE_BASE = os.getenv("BINANCE_BASE", "https://api.binance.com")

# --- Telegram ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- Monitoreo ---
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))  # segundos
MIN_AMOUNT = float(os.getenv("MIN_AMOUNT", 1000))      # CUP
PAYMENT_METHODS = os.getenv("PAYMENT_METHODS", "Transferencia").split(",")

# --- Otros ---
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

if not BINANCE_API_KEY or not BINANCE_API_SECRET:
    raise ValueError("Faltan las credenciales de Binance en el archivo .env")

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Faltan las credenciales de Telegram en el archivo .env")
