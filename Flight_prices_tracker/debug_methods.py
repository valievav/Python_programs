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

    stage_name = "READ_RESULTS_FROM_FILE"

    with open(file_name, "r") as file:
        file_data = file.read()
        results = json.loads(file_data)
        logger.info(f"{stage_name} - Read data from '{file_name}'")
        return results

