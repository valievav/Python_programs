"""
Gets Live API results, logs then into file and finds min price.
"""

import datetime
import sys
from configparser import ConfigParser

from get_live_api_results import get_place_id
from get_live_api_results import live_prices_create_session
from get_live_api_results import live_prices_pull_results
from process_api_results import get_all_prices
from process_api_results import get_min_price
from process_api_results import record_results_into_file


def main():

    parser = ConfigParser()
    parser.read('config.ini')
    api_key = parser.get("API", "rapidapi_key")
    base_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/"
    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': api_key
    }

    city_from = "Krakow"
    country_from = "Poland"
    city_to = "Tokyo"
    country_to = "Japan"

    country = "PL"
    currency = "UAH"
    locale_lang = "en-US"
    outbound_date = "2019-12-25"
    cabin_class = "Economy"
    adults_count = 1

    price_threshold = 15000
    max_retries = 3
    results_file_name = f"Results_{datetime.datetime.now()}.json".replace(":", "-")

    # exit if date value is in the past
    if datetime.datetime.now().date() > datetime.datetime.strptime(outbound_date, "%Y-%m-%d").date():
        sys.exit(f" Outbound date {outbound_date} is in the past. Please fix.")

    # get FROM and TO city ids
    origin_place = get_place_id(base_url=base_url,
                                headers=headers,
                                currency=currency,
                                locale_lang=locale_lang,
                                search_city=city_from,
                                search_country=country_from,
                                max_retries=max_retries)

    destination_place = get_place_id(base_url=base_url,
                                     headers=headers,
                                     currency=currency,
                                     locale_lang=locale_lang,
                                     search_city=city_to,
                                     search_country=country_to,
                                     max_retries=max_retries)

    # run LIVE API search
    if not (origin_place and destination_place):
        sys.exit(f"Invalid value for origin_place - {origin_place}, destination_place - {destination_place}.")
    else:
        session_key = live_prices_create_session(base_url=base_url,
                                                 headers=headers,
                                                 cabin_class=cabin_class,
                                                 country=country,
                                                 currency=currency,
                                                 locale_lang=locale_lang,
                                                 origin_place=origin_place,
                                                 destination_place=destination_place,
                                                 outbound_date=outbound_date,
                                                 adults_count=adults_count,
                                                 max_retries=max_retries)

        all_results = live_prices_pull_results(base_url=base_url,
                                               headers=headers,
                                               session_key=session_key,
                                               max_retries=max_retries)

    record_results_into_file(file_name=results_file_name,
                             results=all_results)

    all_prices = get_all_prices(results=all_results)

    get_min_price(results=all_prices,
                  price_threshold=price_threshold)


if __name__ == "__main__":
    main()

