import requests
import json
import pprint
from configparser import ConfigParser
import datetime


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

    url = f"{base_url}pricing/v1.0"
    payload = f"cabinClass={cabin_class}&country={country}&currency={currency}&locale={locale_lang}" \
              f"&originPlace={origin_place}&destinationPlace={destination_place}&outboundDate={outbound_date}" \
              f"&adults={adults_number}"
    headers.setdefault('content-type', "application/x-www-form-urlencoded")

    response = requests.request("POST", url, data=payload, headers=headers)
    response.raise_for_status()

    # check response - success if empty
    if len(response.text) == 2:
        session_key = response.headers["Location"].split("/")[-1]
        return session_key
    else:
        Exception(f"Attention! Issue with API LIVE request - {response.text}")


def live_prices_pull_results(base_url: str, headers: dict, session_key: str) -> dict:
    """
    Returns Live API results of the previously created session.
    """

    url = f"{base_url}pricing/uk2/v1.0/{session_key}?pageIndex=0&pageSize=20"

    querystring = {"pageIndex": "0", "pageSize": "10"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    if not response.status_code == 200:
        raise Exception(f"{response.status_code} - {response.reason} - {response.content['ValidationErrors'][0]}")

    result = json.loads(response.text)
    return result


def live_prices_get_min_price(results: dict) -> int:

    min_price = None
    for n in range(len(results["Itineraries"])):
        flight_itinerary = results["Itineraries"][n]["PricingOptions"][0]
        if not min_price:
            min_price = flight_itinerary["Price"]
        else:
            if min_price > flight_itinerary["Price"]:
                min_price = flight_itinerary["Price"]
    return min_price


if __name__ == "__main__":

    # general params
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


    place_ids_from = get_place_id(base_url, headers, currency, search_city_from, search_country_from)
    place_ids_to = get_place_id(base_url, headers, currency, search_city_to, search_country_to)
    print(place_ids_from, place_ids_to)

    # get Live API results and log them into file
    session_key = live_prices_create_session(base_url, headers, cabin_class, country, currency, locale_lang,
                                             origin_place, destination_place, outbound_date)
    results = live_prices_pull_results(base_url, headers, session_key)

    with open(f"Results_{datetime.datetime.now()}.txt".replace(":", "-"), "w") as file:
        file.writelines(results)

    pprint.pprint(results, width=1)

    min_price = live_prices_get_min_price(results)
    print(f">>> SUCCESS! Found flight price {min_price} < threshold {price_threshold}.") if min_price <= price_threshold\
        else print(f">>> No suitable flight. Min price {min_price} > threshold {price_threshold}.")

