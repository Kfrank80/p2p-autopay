from logger import logger
from config import TELEGRAM_TOKEN

if __name__ == "__main__":
    logger.info("Bot initialized...")
    logger.info(f"Telegram Token loaded...: {bool(TELEGRAM_TOKEN)}")
