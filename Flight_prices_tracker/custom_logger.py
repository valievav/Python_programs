"""
Records logs both into file and prints into the console
"""

import logging
import datetime
from custom_formatter import CustomFormatter


def create_logger(level=logging.DEBUG):
    """
    Creates custom logger that records logs into file AND prints them into the console.
    Console records are colored using CustomFormatter.
    """

    file_name = f"Logs_{datetime.datetime.now()}.log".replace(":", "-")

    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    if not logger.handlers:  # do not create handlers if already exist (else - multiple log lines)

        # setup file logging
        file_handler = logging.FileHandler(file_name)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # setup console logging
        console_handler = logging.StreamHandler()
        console_formatter = CustomFormatter()  # use CustomFormatter to color logs
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger


def get_logger(func):
    """
    Decorator that changes function by adding a custom logger.
    """

    def wrapper(*args, **kwargs):
        logger = create_logger()
        result = func(*args, **kwargs, logger=logger)
        return result

    return wrapper

