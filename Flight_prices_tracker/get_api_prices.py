import datetime
import json
import pprint
import time
from configparser import ConfigParser

import requests


def get_place_id(base_url: str, headers: dict, currency: str, search_city: str, search_country: str) -> dict:
    """
     Returns list of place_ids (1 city can have different ids)
    """

    url = f"{base_url}autosuggest/v1.0/{currency}/{currency}/{locale_lang}/"
    querystring = {"query": {search_city}}
    response = requests.request("GET", url, headers=headers, params=querystring)
    result = json.loads(response.text)

    place_ids = {}
    for location_data in result['Places']:
        if location_data['CountryName'].lower() == search_country.lower():
            place_ids.setdefault(location_data['PlaceId'], location_data['PlaceName'])

    return place_ids


def live_prices_create_session(base_url: str, headers: dict, cabin_class: str, country: str, currency: str,
                               locale_lang: str, origin_place: str, destination_place: str, outbound_date: str)-> str:
    """
     Creates Live Pricing Service Session that should be created before requesting price data.\n
     See detailed documentation -> https://skyscanner.github.io/slate/#flights-live-prices
    """

    # rerun function until request is created successfully
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
            break
        except requests.exceptions.HTTPError as err:
            print(f"Occurred error {err}. Going to rerun function.")
            timer()

    return session_key


def live_prices_pull_results(base_url: str, headers: dict, session_key: str) -> list:
    """
    Returns Live API results of the previously created session.
    """

    # rerun function until response pulled successfully
    all_results = []
    while True:
        url = f"{base_url}pricing/uk2/v1.0/{session_key}?pageIndex=0&pageSize=20"
        querystring = {"pageIndex": "0", "pageSize": "10"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        result = json.loads(response.text)

        if response.status_code == 200:
            if result["Status"] == "UpdatesPending":  # get next results pages
                all_results.append(result)
                print("Response have status 'UpdatesPending'. Requesting more results.")
                continue
            print(f'Response status - {result["Status"]}. Moving on to the response processing.')
            break
        else:
            print(f"Occurred error {response.status_code} - {response.reason} - {response.content}. "
                  f"Going to rerun function.")
            timer()

    return all_results


def timer(wait_time: int = 90)-> bool:
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
        if not min_price:
            min_price = flight_itinerary["Price"]
        else:
            if min_price > flight_itinerary["Price"]:
                min_price = flight_itinerary["Price"]
                prices_count = n+1

    return prices_count, min_price


def get_live_api_prices(base_url: str, headers: dict, cabin_class: str, country: str, currency: str,
                        locale_lang: str, origin_place: str, destination_place: str, outbound_date: str,
                        prices_count_threshold: int)-> None:
    """
    Gets Live API results and logs then into file.\n
    Live API retrieval consists of 2 parts: creating session and getting results.
    Reruns program if number of results is low (incomplete data).
    """

    # rerun function until full response retrieved successfully
    while True:
        session_key = live_prices_create_session(base_url, headers, cabin_class, country, currency, locale_lang,
                                                 origin_place, destination_place, outbound_date)
        all_results = live_prices_pull_results(base_url, headers, session_key)

        for results in all_results:
            prices_count, min_price = get_min_price(results)

            if prices_count <= prices_count_threshold:
                continue

            # record results into log file
            with open(f"Results_{datetime.datetime.now()}.txt".replace(":", "-"), "w") as file:
                file.writelines(json.dumps(results))

            # print results and min price
            pprint.pprint(results, width=1)
            print(f">>> SUCCESS! Found flight price {min_price} < threshold {price_threshold}.") if min_price <= \
                    price_threshold else print(f">>> No suitable flight. "
                    f"Min price {min_price} > threshold {price_threshold}.")
            break


if __name__ == "__main__":
    parser = ConfigParser()
    parser.read('config.ini')
    api_key = parser.get("API", "rapidapi_key")

    base_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/"
    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': api_key
    }

    search_city_from = "Krakow"
    search_country_from = "Poland"
    search_city_to = "Tokyo"
    search_country_to = "Japan"

    country = "PL"
    currency = "UAH"
    locale_lang = "en-US"

    origin_place = "KRK-sky"
    destination_place = "TYOA-sky"
    outbound_date = "2019-12-21"
    cabin_class = "Economy"
    adults_number = 1

    price_threshold = 15000
    prices_count_threshold = 50

    place_ids_from = get_place_id(base_url, headers, currency, search_city_from, search_country_from)
    place_ids_to = get_place_id(base_url, headers, currency, search_city_to, search_country_to)
    print(place_ids_from, place_ids_to)  # TODO - incorporate into program as step # 1

    get_live_api_prices(base_url, headers, cabin_class, country, currency, locale_lang,
                        origin_place, destination_place, outbound_date, prices_count_threshold)

