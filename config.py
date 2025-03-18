from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import logging.config
import os


load_dotenv()


DEBUG = int(os.environ.get('DEBUG', 1))

CHANNEL_ID = os.environ.get("CHANNEL_ID", "")
SUBSCRIPTION_STATUSES = ["member", "administrator", "creator"]

DATABASE_URL = os.environ.get("DATABASE_URL")

bot = Bot(token=os.environ.get("TOKEN", ""))
dp = Dispatcher()

log_config = {
    "version": 1,
    "formatters": {
        "formatter": {
            "format": '%(asctime)s - %(levelname)s - %(message)s',
            "datefmt": '%d-%b-%y %H:%M:%S',
        },
    },
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "formatter": "formatter",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "formatter",
            "filename": os.environ.get("LOGGING_PATH", "./app.log")
        },
    },
    "loggers": {
        "log": {
            "handlers": ["file_handler"],
            "level": "DEBUG",
        },
        "console": {
            "handlers": ["console_handler"],
            "level": "DEBUG",
        }
    },
}


logging.config.dictConfig(log_config)
logger_mode = 'console' if DEBUG else 'log'
logger = logging.getLogger(logger_mode)

logger.debug(f"Debug mode: {DEBUG}")
