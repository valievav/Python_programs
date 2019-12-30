"""
Contains methods for API results processing.
"""

import json
import logging
import sys

from custom_logger import get_logger


@get_logger
def record_results_into_file(file_name: str, results: dict, logger: logging.Logger)-> None:
    """
    Records dict into json file
    """

    stage_name = "RECORD_RESULTS_INTO_FILE"

    with open(file_name, "w") as file:
        json.dump(results, indent=4, fp=file)
    logger.info(f"{stage_name} - Recorded results into '{file_name}'.")


@get_logger
def get_all_prices(results: dict, logger: logging.Logger)-> list:
    """
    Returns all prices from result
    """

    stage_name = "GET_PRICES"
    all_prices = []

    itin_number = len(results)
    logger.debug(f"{stage_name} - Number of itineraries - {len(results)}")

    for itin in range(itin_number-1):  # results list has > 1 element if was 'Updates pending' status
        flights_number = len(results[itin]["Itineraries"][0])
        logger.debug(f"{stage_name} - Number of flights - {flights_number}")

        for flight_count in range(flights_number-1):
            price = results[itin]["Itineraries"][flight_count]["PricingOptions"][0]["Price"]
            all_prices.append(price)

    logger.info(f"{stage_name} - All prices list preparation finished.")
    logger.debug(f"{stage_name} - All prices count - {len(all_prices)}, values - {all_prices}")
    return all_prices


@get_logger
def get_min_price(results: list, price_threshold: int, logger: logging.Logger)-> None:
    """
    Returns min price from the list
    """

    stage_name = "GET_MIN_PRICE"

    if not results:
        logger.critical(f"{stage_name} - Results list is empty. Exiting the program.")
        sys.exit()

    min_price = sorted(results)[0]
    if min_price <= price_threshold:
        logger.info(f"{stage_name} - SUCCESS! Found flight price {min_price} < threshold {price_threshold}.")
    else:
        logger.info(f"{stage_name} - No suitable flight. Min price {min_price} > threshold {price_threshold}.")

