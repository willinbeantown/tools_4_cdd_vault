#!/usr/bin/env python
# coding: utf-8
"""
Set Logger and Create Log File.
"""
# IMPORTS
import os
import logging
from datetime import date, datetime


def set_logger() -> logging.Logger:
    today: date
    today_formed: str
    log_str: str
    log_path: str
    logger: logging.Logger
    file_handler: logging.FileHandler
    formatter: logging.Formatter
    
    today = date.today()
    today_formed = today.strftime("%Y-%m-%d")
    os.makedirs(f"logs_{today_formed}",
                exist_ok = True)
    log_str = f"logs_{today_formed}/log_%Y-%m-%d_%H-%M-%S.log"
    log_path = datetime.now().strftime(log_str)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
