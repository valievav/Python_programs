"""
Records logs both into file and prints into the console
"""

import logging
from Flight_prices_tracker.custom_formatter import CustomFormatter


def create_logger(log_file_abs_path: str, level=logging.DEBUG)-> logging.Logger:
    """
    Creates custom logger that records logs into file AND prints them into the console.
    Console records are colored using CustomFormatter.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    if not logger.handlers:  # do not create handlers if already exist (else - multiple log lines)

        # setup file logging
        file_handler = logging.FileHandler(log_file_abs_path)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # setup console logging
        console_handler = logging.StreamHandler()
        console_formatter = CustomFormatter()  # use CustomFormatter to color logs
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger

