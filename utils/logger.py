import logging
from logging.handlers import RotatingFileHandler
import os




os.makedirs("../logs", exist_ok=True)


logger = logging.getLogger("whisper_bot")
logger.setLevel(logging.INFO)


formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)



file_handler = RotatingFileHandler(
    "../logs/bot.log",
    maxBytes=5 * 1024 * 1024,  # 5 МБ
    backupCount=3,             # хранить 3 старых файла
    encoding="utf-8"
)


file_handler.setFormatter(formatter)
logger.addHandler(file_handler)