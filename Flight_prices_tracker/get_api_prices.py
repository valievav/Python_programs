import requests
import json
import pprint
from configparser import ConfigParser


def live_prices_create_session(api_key, cabin_class, country, currency, locale, origin_place, destination_place, outbound_date):

    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/v1.0"

    payload = f"cabinClass={cabin_class}&country={country}&currency={currency}&locale={locale}" \
              f"&originPlace={origin_place}&destinationPlace={destination_place}&outboundDate={outbound_date}" \
              f"&adults={adults_number}"
    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': api_key,
        'content-type': "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    response.raise_for_status()

    # check response - success if empty
    if len(response.text) == 2:
        session_key = response.headers["Location"].split("/")[-1]
        return session_key
    else:
        Exception(f"Attention! Issue with API LIVE request - {response.text}")


def live_prices_pull_results(session_key):

    url = f"https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/" \
                       f"apiservices/pricing/uk2/v1.0/{session_key}"

    querystring = {"pageIndex": "0", "pageSize": "10"}

    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': api_key
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    results = json.loads(response.text)
    return results


def live_prices_get_min_price(results):
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
    parser = ConfigParser()
    parser.read('config.ini')

    api_key = parser.get("API", "rapidapi_key")
    print(api_key)
    cabin_class = "Economy"
    country = "PL"
    currency = "UAH"
    locale = "en-US"
    origin_place = "KRK-sky"
    destination_place = "NRT-sky"
    # destination_place = "TYOA-sky"
    outbound_date = "2019-12-21"
    adults_number = 1

    price_threshold = 11000

    session_key = live_prices_create_session(api_key, cabin_class, country, currency, locale, origin_place, destination_place, outbound_date)
    results = live_prices_pull_results(session_key)

    pprint.pprint(results, width=1)
    print("--------")

    min_price = live_prices_get_min_price(results)
    print(f">>> SUCCESS! Found flight price {min_price} < threshold {price_threshold}.") if min_price <= price_threshold\
        else print(f">>> No suitable flight. Min price {min_price} > threshold {price_threshold}.")

