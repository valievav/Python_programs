"""
Contains methods for Live API import.
Live API retrieval consists of 2 parts: creating session and getting results.
"""

import datetime
import json
import logging
import os
import pickle
import sys
import time
import pymongo
import requests
from bson import json_util  # to record JSON to file after mongodb
from Flight_prices_tracker.mongodb_methods import record_json_to_mongodb


def timer(logger: logging.Logger, wait_time: int = 60) -> None:
    """
    Timer to count down certain number of seconds
    """

    stage_name = "TIMER"

    now = time.time()
    timer_time = now + wait_time
    while now <= timer_time:
        time.sleep(1)
        now += 1
    logger.debug(f"{stage_name} - Passed {wait_time} sec")


def retry(stage_name: str, current_try: int, max_tries: int, err: Exception or str, logger: logging.Logger)-> None:
    """
    Compares current run number with max run number and creates delay before the rerun.
    If max retries number is reached it exits the program.
    """

    if current_try <= max_tries:
        logger.error(f"{stage_name} - Try #{current_try} - Occurred error '{err}'. Rerunning after delay.")
        timer(logger=logger)
    else:
        logger.critical(f"{stage_name} - Try #{current_try}. Exiting the program.")
        sys.exit()  # no point in running further if no results in N tries


def get_airport_ids(base_url: str, headers: dict, currency: str, locale_lang: str,
                    search_cities: list, search_countries: list, max_retries: int,
                    logger: logging.Logger) -> list:
    """
    Gets list of airport ids, where each element is 1st airport for search city-country combination responses
    (1 city-country pair can have several airports).
    """

    stage_name = "GET_PLACE_ID"
    try_number = 0

    # compare if length of search lists is equal
    if len(search_cities) != len(search_countries):
        logger.warning(f"City and country lists length are different - {len(search_cities)} vs {len(search_countries)}."
                       f"Cannot match all elements - please fix.")

    airport_ids = []

    # get airport_ids for each search city-country pair
    for (search_city, search_country) in zip(search_cities, search_countries):

        url = f"{base_url}autosuggest/v1.0/{currency}/{currency}/{locale_lang}/"
        querystring = {"query": {search_city}}

        # rerun if response unsuccessful
        while True:
            try:
                response = requests.request("GET", url, headers=headers, params=querystring)
                result = json.loads(response.text)
            except Exception as exc:
                try_number += 1
                retry(stage_name, try_number, max_retries, exc, logger=logger)
            else:
                # get all airport ids
                location_airport_ids = []
                for location_data in result['Places']:
                    if location_data['CountryName'].lower() == search_country.lower():
                        location_airport_ids.append(location_data['PlaceId'])

                if not location_airport_ids:
                    logger.critical(f"{stage_name} - Place_ids list is empty! Exiting the program.")
                    sys.exit()

                # return 1st elem
                airport_id = location_airport_ids[0]
                logger.debug(f"{stage_name} - Available codes for {search_city}-{search_country}: {location_airport_ids}. "
                             f"Going to use 1st element from the list.")
                logger.info(f"{stage_name} - {search_city}-{search_country} airport id - '{airport_id}'")
                airport_ids.append(airport_id)
                break

    return airport_ids


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
            retry(stage_name, try_number, max_retries, err, logger=logger)
        else:
            session_key = response.headers["Location"].split("/")[-1]
            logger.info(f"{stage_name} - Session created successfully")
            return session_key


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
                logger.info(f"{stage_name} - Got response 'UpdatesPending'. Requesting more results after delay.")
                timer(wait_time=10, logger=logger)  # wait for all results to be updated
                continue
            logger.info(f'{stage_name} - Got response status - {result["Status"]}. '
                        f'Recorded {len(all_results)} result requests. Moving on to the next stage.')
            break
        else:
            try_number += 1
            retry(stage_name, try_number, max_retries, f"{response.status_code} - {response.content}", logger=logger)

    return all_results


def get_live_api_results(base_url: str, headers: dict, cabin_class: str, country: str, currency: str,
                         locale_lang: str, city_from: str, city_to: str, country_from: str, country_to: str,
                         outbound_date: str, adults_count: int, max_retries: int, logger: logging.Logger)-> iter:
    """
    Performs 3 steps to get Live API results: get city_id_from & city_id_to, create Live API session and
    retrieve API results. Returns API response as an iterable.
    """

    # get city ids
    city_id_from, city_id_to = get_airport_ids(base_url=base_url,
                                               headers=headers,
                                               currency=currency,
                                               locale_lang=locale_lang,
                                               search_cities=[city_from, city_to],
                                               search_countries=[country_from, country_to],
                                               max_retries=max_retries,
                                               logger=logger)

    # create session
    session_key = live_prices_create_session(base_url=base_url,
                                             headers=headers,
                                             cabin_class=cabin_class,
                                             country=country,
                                             currency=currency,
                                             locale_lang=locale_lang,
                                             origin_place=city_id_from,
                                             destination_place=city_id_to,
                                             outbound_date=outbound_date,
                                             adults_count=adults_count,
                                             max_retries=max_retries,
                                             logger=logger)

    # retrieve results
    all_results = live_prices_pull_results(base_url=base_url,
                                           headers=headers,
                                           session_key=session_key,
                                           max_retries=max_retries,
                                           logger=logger)

    return all_results


def record_results_into_file(file_abs_path: str, results: iter, logger: logging.Logger)-> None:
    """
    Records dict into json file
    """

    stage_name = "RECORD_RESULTS_INTO_FILE"

    with open(file_abs_path, "w") as file:
        # json_util encoder after pymongo (else "not JSON serializable" error)
        json.dump(results, indent=4, fp=file, default=json_util.default)
    logger.info(f"{stage_name} - Recorded results into '{file_abs_path.split('/')[-1]}'.")


def pickle_data(file_name: str, data_to_pickle: iter, logger: logging.Logger) -> None:
    """
    Pickles data into file as dictionary if key doesn't exists, else - updates pickled data
    """

    stage_name = "PICKLE DATA"

    # get pickled data
    with open(file_name, "rb") as file:
        try:
            pickled_data = pickle.load(file)
        except EOFError:
            pickled_data = None

    # update pickled data if exists the same key
    if pickled_data:
        logger.debug(f"{stage_name} - Updating pickled data - {pickled_data} with new value {data_to_pickle}")
        data_to_pickle = {**pickled_data, **data_to_pickle}  # 2nd dict overwrites values for common keys

    # record new data or updated data into file
    with open(file_name, "wb") as file:
        pickle.dump(data_to_pickle, file, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info(f"{stage_name} - '{file_name}' content: {data_to_pickle}")


def unpickle_data(file_name: str, logger: logging.Logger) -> iter:
    """
    Retrieves pickled data from file
    """

    stage_name = "UNPICKLE DATA"

    # retrieve pickled data if exists
    with open(file_name, "rb") as file:
        try:
            data = pickle.load(file)
            logger.debug(f"{stage_name} - Unpickled {data} from '{file_name}'")
            return data
        except EOFError:
            return None


def get_pickled_outbound_date(pickle_file: str, city_from: str, city_to: str, logger: logging.Logger)-> str or None:
    """
    Retrieves pickled date from pickled file
    """

    pickled_data = unpickle_data(file_name=pickle_file,
                                 logger=logger)

    if pickled_data:
        pickled_outbound_date = pickled_data[f"{city_from}-{city_to}"]
        return pickled_outbound_date


def get_api_data_for_n_days(days: int, pickle_file: str, base_url: str, headers: dict, cabin_class: str,
                            country: str, currency: str, locale_lang: str, city_from: str, city_to: str,
                            country_from: str, country_to: str, outbound_date: str, adults_count: int, max_retries: int,
                            json_files_folder: str, json_file: str, collection: pymongo.collection.Collection,
                            logger: logging.Logger, save_to_file: bool = False)-> None:
    """
    Runs get_live_api_results for N days, pickles last used date (to continue where left off
    in case of interruption), records data to MongoDB and into file if passed True flag.
    """

    for n in range(days):

        # get outbound date from picked file (to continue where left off) or use passed date
        pickled_data = unpickle_data(file_name=pickle_file,
                                     logger=logger)

        outbound_date = pickled_data[f"{city_from}-{city_to}"] if pickled_data else outbound_date
        logger.info(f"Running API request for -> {outbound_date}")
        outbound_date_datetime = datetime.datetime.strptime(outbound_date, "%Y-%m-%d").date()

        # check date validity before run
        if datetime.datetime.now().date() > outbound_date_datetime:
            sys.exit(f"Outbound date {outbound_date_datetime} is in the past. Please fix.")

        # get LIVE API results
        all_results = get_live_api_results(base_url=base_url,
                                           headers=headers,
                                           cabin_class=cabin_class,
                                           country=country,
                                           currency=currency,
                                           locale_lang=locale_lang,
                                           city_from=city_from,
                                           city_to=city_to,
                                           country_from=country_from,
                                           country_to=country_to,
                                           outbound_date=outbound_date,
                                           adults_count=adults_count,
                                           max_retries=max_retries,
                                           logger=logger)

        # record results into db
        record_json_to_mongodb(json_data=all_results,
                               collection=collection,
                               logger=logger)

        # record results into file
        if save_to_file:
            file_abs_path = os.path.join(os.getcwd(), json_files_folder, json_file.replace('xxx', outbound_date))
            record_results_into_file(file_abs_path=file_abs_path,
                                     results=all_results,
                                     logger=logger)
        # find next date
        next_outbound_date_datetime = outbound_date_datetime + datetime.timedelta(days=1)
        outbound_date = next_outbound_date_datetime.strftime("%Y-%m-%d")

        # pickle next date (process can resume from this point on the next run)
        pickle_data(file_name=pickle_file,
                    data_to_pickle={f"{city_from}-{city_to}": outbound_date},
                    logger=logger)

