import logging  # gives tools to make logging
import sys


logger = logging.getLogger("backend")
logger.setLevel(logging.DEBUG)

# Console logs (terminal)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    f"%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
console_handler.setFormatter(formatter)

# File logs (rotating, so it doesn't grow forever)
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
