"""
Gets Live API results, logs then into file and finds min price.
"""

import datetime
import sys
from configparser import ConfigParser

from debug_methods import get_api_results_from_file
from files_cleaner import files_cleaner
from get_live_api_results import get_live_api_results
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
    outbound_date = "2020-01-01"
    cabin_class = "Economy"
    adults_count = 1

    price_threshold = 15000
    max_retries = 3
    results_file_name = f"Results_{datetime.datetime.now()}.json".replace(":", "-")

    get_results_from_api = True
    debug_results_file = 'Results_debug.json'

    # check date validity before run
    if datetime.datetime.now().date() > datetime.datetime.strptime(outbound_date, "%Y-%m-%d").date():
        sys.exit(f"Outbound date {outbound_date} is in the past. Please fix.")

    # get api results (from API for regular run or from file for process methods debug)
    if get_results_from_api:
        all_results = get_live_api_results(base_url=base_url,
                                           headers=headers,
                                           currency=currency,
                                           locale_lang=locale_lang,
                                           city_from=city_from,
                                           country_from=country_from,
                                           city_to=city_to,
                                           country_to=country_to,
                                           max_retries=max_retries,
                                           cabin_class=cabin_class,
                                           country=country,
                                           outbound_date=outbound_date,
                                           adults_count=adults_count
                                           )

        record_results_into_file(file_name=results_file_name,
                                 results=all_results)
    else:
        # get results from file to debug processing methods below
        all_results = get_api_results_from_file(debug_results_file)

    all_prices = get_all_prices(results=all_results)

    get_min_price(results=all_prices,
                  price_threshold=price_threshold)

    files_cleaner(extension='log',
                  to_keep_number=10)

    files_cleaner(extension='json',
                  to_keep_number=5,
                  exception_file=debug_results_file)


if __name__ == "__main__":
    main()

