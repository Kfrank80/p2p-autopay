import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

from core.config import DEBUG_MODE

def log(msg):
    if DEBUG_MODE:
        print(f"[DEBUG] {msg}")

