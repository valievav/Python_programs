"""
Contains methods for API results processing.
"""

import logging
import sys


def get_all_prices(results: dict, logger: logging.Logger)-> list:
    """
    Returns all prices from result
    """

    stage_name = "GET_PRICES"
    all_prices = []

    itin_numbers = len(results)
    logger.info(f"{stage_name} - Number of itineraries - {len(results)}")
    all_flights_count = 0

    for itin_number in range(itin_numbers):  # results list has > 1 element if was 'Updates pending' status
        flights_data = results[itin_number]["Itineraries"]
        flights_count = len(flights_data)
        all_flights_count += flights_count

        for flight_number in range(flights_count):  # each itinerary has unique # of flights provided
            flight_prices_data = flights_data[flight_number]["PricingOptions"]
            flight_prices_count = len(flight_prices_data)
            flight_price = 0

            for price_number in range(flight_prices_count):  # each flight can have several legs (flights with stops)
                leg_price = flight_prices_data[price_number]["Price"]
                flight_price += leg_price

            all_prices.append(round(flight_price, 2))

    logger.info(f"{stage_name} - Number of flights - {all_flights_count}")
    logger.info(f"{stage_name} - Prepared all prices list")
    logger.debug(f"{stage_name} - All prices count - {len(all_prices)}, values - {all_prices}")
    return all_prices


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

