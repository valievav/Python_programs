"""
Provides custom formatting for the logs depending on the logs level
"""

import logging
from colorama import Fore


class CustomFormatter(logging.Formatter):
    """
    Colors log messages according to the log level
    """

    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    all_formats = {
        logging.DEBUG: Fore.LIGHTBLACK_EX + format,
        logging.INFO: Fore.BLACK + format,
        logging.WARNING: Fore.MAGENTA + format,
        logging.ERROR: Fore.LIGHTRED_EX + format,
        logging.CRITICAL: Fore.RED + format
    }

    def format(self, log_line):
        log_format = self.all_formats.get(log_line.levelno)
        formatter = logging.Formatter(log_format)
        return formatter.format(log_line)

