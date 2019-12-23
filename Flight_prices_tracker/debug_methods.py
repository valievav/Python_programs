"""
Contains methods helpful for debugging
"""

import json
import logging
from custom_logger import get_logger


@get_logger
def get_api_results_from_file(file_name: str, logger: logging.Logger)-> iter:
    """
    Reads json data from file
    """

    with open(file_name, "r") as file:
        file_data = file.read()
        results = json.loads(file_data)
        logger.info(f"Read data from file '{file_name}'")
        return results

