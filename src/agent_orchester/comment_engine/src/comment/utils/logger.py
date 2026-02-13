import logging
from pathlib import Path
import sys

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        handler.setStream(open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
