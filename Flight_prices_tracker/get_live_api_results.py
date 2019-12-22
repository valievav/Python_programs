"""
Contains methods for Live API import.
Live API retrieval consists of 2 parts: creating session and getting results.
"""

import json
import logging
import sys
import time

import requests
from custom_logger import get_logger


@get_logger
def timer(logger: logging.Logger, wait_time: int = 60) -> None:
    """
    Timer to count down certain number of seconds
    """

    now = time.time()
    timer_time = now + wait_time
    while now <= timer_time:
        time.sleep(1)
        now += 1
    logger.debug(f"Passed {wait_time} sec")


@get_logger
def retry(stage_name, current_try, max_tries, err, logger)-> None:
    """
    Compares current run number with max run number and creates delay before the rerun.
    If max retries number is reached it exits the program.
    """

    if current_try <= max_tries:
        logger.error(f"{stage_name} - Try #{current_try} - Occurred error '{err}'. Rerunning after delay.")
        timer()
    else:
        logger.error(f"{stage_name} - Try #{current_try}. Exiting the program.")
        sys.exit()  # no point in running further if no results in N tries


@get_logger
def get_place_id(base_url: str, headers: dict, currency: str, locale_lang: str,
                 search_city: str, search_country: str, max_retries: int,
                 logger: logging.Logger) -> str:
    """
    Gets list of all place ids (1 city can have different ids) and returns 1st element in the list.
    """

    stage_name = "GET_PLACE_ID"
    try_number = 0

    url = f"{base_url}autosuggest/v1.0/{currency}/{currency}/{locale_lang}/"
    querystring = {"query": {search_city}}

    # rerun if response unsuccessful
    while True:
        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            result = json.loads(response.text)
        except Exception as exc:
            try_number += 1
            retry(stage_name, try_number, max_retries, exc)
        else:
            # get all place ids
            place_ids = []
            for location_data in result['Places']:
                if location_data['CountryName'].lower() == search_country.lower():
                    place_ids.append(location_data['PlaceId'])

            if not place_ids:
                sys.exit(f"Place_ids list is empty. Please investigate and fix.")

            # return 1st place id
            place_id = place_ids[0]
            logger.debug(f"{stage_name} - Available codes for {search_city}-{search_country}: {place_ids}. "
                         f"Going to use 1st element from the list.")
            logger.info(f"{stage_name} - {search_city}-{search_country} place id - '{place_id}'")
            return place_id


@get_logger
def live_prices_create_session(base_url: str, headers: dict, cabin_class: str, country: str, currency: str,
                               locale_lang: str, origin_place: str, destination_place: str, outbound_date: str,
                               adults_count: int, max_retries: int, logger: logging.Logger)-> str:
    """
     Creates Live Pricing Service Session (it should be created before requesting price data).\n
     See detailed documentation -> https://skyscanner.github.io/slate/#flights-live-prices
    """

    stage_name = "CREATE_SESSION"
    try_number = 0

    url = f"{base_url}pricing/v1.0"
    payload = f"cabinClass={cabin_class}&country={country}&currency={currency}" \
              f"&locale={locale_lang}&originPlace={origin_place}&destinationPlace={destination_place}" \
              f"&outboundDate={outbound_date}&adults={adults_count}"
    headers.setdefault('content-type', "application/x-www-form-urlencoded")

    # rerun if response unsuccessful
    while True:
        try:
            response = requests.request("POST", url, data=payload, headers=headers)
            logger.debug(f"{stage_name} - Full requested url: {url}/{payload}")
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            try_number += 1
            retry(stage_name, try_number, max_retries, err)
        else:
            session_key = response.headers["Location"].split("/")[-1]
            logger.info(f"{stage_name} - Session created successfully")
            return session_key


@get_logger
def live_prices_pull_results(base_url: str, headers: dict, session_key: str,
                             max_retries: int, logger: logging.Logger) -> list:
    """
    Returns Live API results from the created session.
    """

    stage_name = "PULL_RESULTS"
    try_number = 0

    url = f"{base_url}pricing/uk2/v1.0/{session_key}?pageIndex=0&pageSize=20"
    querystring = {"pageIndex": "0", "pageSize": "100"}
    all_results = []

    # rerun if response unsuccessful
    while True:
        response = requests.request("GET", url, headers=headers, params=querystring)
        result = json.loads(response.text)

        if response.status_code == 200:
            all_results.append(result)
            if result["Status"] == "UpdatesPending":  # get next scope results
                logger.debug(f"{stage_name} - Got response 'UpdatesPending'. Requesting more results after delay.")
                timer(wait_time=20)  # wait for all results to be updated
                continue
            logger.info(f'{stage_name} - Got response status - {result["Status"]}. '
                        f'Recorded {len(all_results)} result requests. Moving on to the next stage.')
            break
        else:
            try_number += 1
            retry(stage_name, try_number, max_retries, f"{response.status_code} - {response.content}")

    return all_results

