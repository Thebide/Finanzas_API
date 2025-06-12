import os

import logging
from logging.handlers import TimedRotatingFileHandler

from . import app_settings

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
date_format = "%Y-%m-%d"
datetime_format = "%Y-%m-%d %H:%M:%S"
def config_loggin():
    os.makedirs(app_settings.LOG_DIR, exist_ok=True)
    log_filename = f"{app_settings.LOG_DIR}\\FASTAPI.log"

    log_level = logging.DEBUG if app_settings.DEBUG else logging.INFO

    file_handler = TimedRotatingFileHandler(log_filename, "midnight", 1)
    file_handler.suffix = date_format

    console_handler = logging.StreamHandler()
    fromatter = logging.Formatter(log_format, datetime_format)
    console_handler.setFormatter(fromatter)
    file_handler.setFormatter(fromatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)

    console_handler.setLevel(logging.WARNING)
    root_logger.addHandler(console_handler)