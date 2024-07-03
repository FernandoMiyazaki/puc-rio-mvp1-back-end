import logging
import os
from logging.config import dictConfig

LOG_PATH = "log/"

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

dictConfig({
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s",
        },
        "detailed": {
            "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s - call_trace=%(pathname)s L%(lineno)-4d",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": os.path.join(LOG_PATH, "gunicorn.error.log"),
            "maxBytes": 10000,
            "backupCount": 10,
            "delay": True,
        },
        "detailed_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": os.path.join(LOG_PATH, "gunicorn.detailed.log"),
            "maxBytes": 10000,
            "backupCount": 10,
            "delay": True,
        },
    },
    "loggers": {
        "gunicorn.error": {
            "handlers": ["console", "error_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "detailed_file"],
        "level": "INFO",
    },
})

logger = logging.getLogger(__name__)
