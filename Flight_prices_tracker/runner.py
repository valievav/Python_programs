"""
Gets Live API results, logs then into file and finds min price.
"""

import datetime
import os
import sys
from configparser import ConfigParser

from custom_logger import create_logger
from files_cleaner import files_cleaner
from get_live_api_results import get_live_api_results, get_airport_ids
from process_api_results import get_all_prices, get_min_price, record_results_into_file, get_api_results_from_file


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
    cabin_class = "Economy"
    adults_count = 1

    outbound_date = "2020-02-01"
    days_to_request = 3

    price_threshold = 15000
    max_retries = 3

    json_files_folder = "json_files"
    log_files_folder = "log_files"

    get_results_from_api = True
    debug_results_file = 'Results_debug.json'

    cwd = os.getcwd()
    log_file_abs_path = os.path.join(cwd, log_files_folder, f"Logs_{datetime.datetime.now()}.log".replace(":", "-"))

    logger = create_logger(log_file_abs_path)

    if get_results_from_api:  # get data from API or from file

        # get city ids
        city_id_from, city_id_to = get_airport_ids(base_url=base_url,
                                                   headers=headers,
                                                   currency=currency,
                                                   locale_lang=locale_lang,
                                                   search_cities=[city_from, city_to],
                                                   search_countries=[country_from, country_to],
                                                   max_retries=max_retries,
                                                   logger=logger)

        # get API data for N days
        for n in range(days_to_request):
            outbound_date_datetime = datetime.datetime.strptime(outbound_date, "%Y-%m-%d").date()
            logger.info(f"Running API request for date -> {outbound_date}")

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
                                               city_id_from=city_id_from,
                                               city_id_to=city_id_to,
                                               outbound_date=outbound_date,
                                               adults_count=adults_count,
                                               max_retries=max_retries,
                                               logger=logger)

            # record results to file
            json_file = f"Results_{outbound_date}_{city_id_from}-{city_id_to}_from_" \
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.json"
            file_abs_path = os.path.join(os.getcwd(), json_files_folder, json_file)

            record_results_into_file(file_abs_path=file_abs_path,
                                     results=all_results,
                                     logger=logger)
            # find next date
            next_outbound_date_datetime = outbound_date_datetime + datetime.timedelta(days=1)
            outbound_date = next_outbound_date_datetime.strftime("%Y-%m-%d")
    else:
        # get results from file to debug processing functions below
        all_results = get_api_results_from_file(file_name=debug_results_file,
                                                logger=logger)

    # process results
    all_prices = get_all_prices(results=all_results,
                                logger=logger)

    get_min_price(results=all_prices,
                  price_threshold=price_threshold,
                  logger=logger)

    # clean up log files
    log_path_to_clean = os.path.join(cwd, log_files_folder)
    files_cleaner(path_to_clean=log_path_to_clean,
                  extension='log',
                  to_keep_number=10,
                  logger=logger)


if __name__ == "__main__":
    main()

