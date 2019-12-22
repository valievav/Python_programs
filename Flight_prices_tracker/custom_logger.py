"""
Records logs both into file and prints into the console
"""

import logging
import datetime
from custom_formatter import CustomFormatter


def get_logger(func, level=logging.DEBUG):
    """
    Decorator that changes function by adding a custom logger.
    It records logs into file and prints into the console.
    Console records are colored using CustomFormatter.
    """

    file_name = f"Logs_{datetime.datetime.now()}.log".replace(":", "-")

    def create_logger(file_name):
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

    def wrapper(*args, **kwargs):
        logger = create_logger(file_name)
        result = func(*args, **kwargs, logger=logger)
        return result

    return wrapper

