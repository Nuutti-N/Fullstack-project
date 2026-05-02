import logging  # gives tools to make logging
from logging.handlers import RotatingFileHandler
import sys
import os

logger = logging.getLogger("backend")
logger.setLevel(logging.DEBUG)

# Console logs (terminal)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    f"%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
console_handler.setFormatter(formatter)

# Add rotatingFileHandler, that if hit limit start new.
if os.getenv("ENVIRONMENT") != "production":
    file_handler = RotatingFileHandler(
        "app.log", maxBytes=10000, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
