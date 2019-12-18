import datetime
import json
import logging
import time

import requests

# record logs into file and print into the console
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(f"Logs_{datetime.datetime.now()}.log".replace(":", "-"))

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def get_place_id(base_url: str, headers: dict, currency: str, locale_lang: str,
                 search_city: str, search_country: str) -> str:
    """
    Displays list of all place ids (1 city can have different ids)
    and returns 1st element in the list as the most popular one.
    """

    url = f"{base_url}autosuggest/v1.0/{currency}/{currency}/{locale_lang}/"
    querystring = {"query": {search_city}}
    response = requests.request("GET", url, headers=headers, params=querystring)
    result = json.loads(response.text)

    # get all place ids
    places = {}
    for location_data in result['Places']:
        if location_data['CountryName'].lower() == search_country.lower():
            places.setdefault(location_data['PlaceId'], location_data['PlaceName'])

    # get first place id
    if places:
        place_ids = [place_id for place_id, place_name in places.items()]
        logger.info(f"Available codes for {search_city}-{search_country}: {place_ids}. "
                     f"Going to use 1st element from the list -> '{place_ids[0]}'")

        return place_ids[0]


def live_prices_create_session(base_url: str, headers: dict, cabin_class: str, country: str, currency: str,
                               locale_lang: str, origin_place: str, destination_place: str, outbound_date: str,
                               adults_number: int)-> str:
    """
     Creates Live Pricing Service Session that should be created before requesting price data.\n
     See detailed documentation -> https://skyscanner.github.io/slate/#flights-live-prices
    """

    # rerun until request is created successfully
    while True:
        url = f"{base_url}pricing/v1.0"
        payload = f"cabinClass={cabin_class}&country={country}&currency={currency}&locale={locale_lang}" \
                  f"&originPlace={origin_place}&destinationPlace={destination_place}&outboundDate={outbound_date}" \
                  f"&adults={adults_number}"
        headers.setdefault('content-type', "application/x-www-form-urlencoded")

        response = requests.request("POST", url, data=payload, headers=headers)

        try:
            response.raise_for_status()
            session_key = response.headers["Location"].split("/")[-1]
            logger.info(f"CREATING SESSION STAGE - Session created successfully.")
            break
        except requests.exceptions.HTTPError as err:
            logger.exception(f"    >>> CREATING SESSION STAGE - Occurred error '{err}'. RERUNNING function with delay.")
            timer()

    return session_key


def live_prices_pull_results(base_url: str, headers: dict, session_key: str) -> list:
    """
    Returns Live API results of the previously created session.
    """

    # rerun until response pulled successfully
    all_results = []
    while True:
        url = f"{base_url}pricing/uk2/v1.0/{session_key}?pageIndex=0&pageSize=20"
        querystring = {"pageIndex": "0", "pageSize": "100"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        result = json.loads(response.text)

        if response.status_code == 200:
            all_results.append(result)
            if result["Status"] == "UpdatesPending":  # get next scope results
                logger.info("PULLING RESULTS STAGE - Got response 'UpdatesPending'. "
                             "Requesting more results with delay.")
                timer(0.5)
                continue
            logger.info(f'PULLING RESULTS STAGE - Got response status - {result["Status"]}. '
                         f'Recorded {len(all_results)} result requests. Moving on to the next stage.')
            break
        else:
            logger.exception(f"    >>> PULLING RESULTS ERROR: {response.status_code} - {response.content}. "
                          f"RERUNNING function with delay.")
            timer()

    return all_results


def timer(wait_time: float = 90)-> bool:
    """
    Returns True when passed certain amount of seconds.
    """

    now = time.time()
    timer_time = now + wait_time
    while now <= timer_time:
        time.sleep(1)
        now += 1

    return True


def get_min_price(results: dict):
    """
    Returns number of prices in dictionary and minimum price.
    """

    min_price = 0
    prices_count = 0

    for n in range(len(results["Itineraries"])):
        flight_itinerary = results["Itineraries"][n]["PricingOptions"][0]
        prices_count += 1

        if not min_price:
            min_price = flight_itinerary["Price"]
        else:
            if min_price > flight_itinerary["Price"]:
                min_price = flight_itinerary["Price"]

    return prices_count, min_price


def get_live_api_prices(base_url: str, headers: dict, cabin_class: str, country: str, currency: str,
                        locale_lang: str, origin_place: str, destination_place: str, outbound_date: str,
                        adults_number: int, price_threshold: int, prices_count_threshold: int)-> None:
    """
    Gets Live API results and logs then into file.\n
    Live API retrieval consists of 2 parts: creating session and getting results.
    Reruns program if number of results is low (incomplete data) or no results.
    """

    # rerun until full response retrieved successfully
    while True:
        # get session key and retrieve results
        session_key = live_prices_create_session(base_url, headers, cabin_class, country, currency, locale_lang,
                                                 origin_place, destination_place, outbound_date, adults_number)
        all_results = live_prices_pull_results(base_url, headers, session_key)

        # rerun if no results
        if not all_results:
            logger.info("RERUNNING function - no results.")
            continue

        # find general prices count and min prices
        all_prices_count = 0
        all_min_prices = []
        for results in all_results:
            prices_count, min_price = get_min_price(results)
            all_prices_count += prices_count
            all_min_prices.append(min_price)

            logger.debug(f"RESULT SCOPE # {len(all_min_prices)+1}:")
            logger.debug(json.dumps(results))

        # rerun if incomplete results
        if all_prices_count <= prices_count_threshold:
            logger.info("RERUNNING function - results are incomplete.")
            continue

        # find min price
        min_price = sorted(all_min_prices)[0]
        logger.info(f">>> SUCCESS! Found flight price {min_price} < threshold {price_threshold}.") \
            if min_price <= price_threshold else \
            logger.info(f">>> No suitable flight. Min price {min_price} > threshold {price_threshold}.")
        logger.info("Process finished.")

        break

