"""
Gets Live API results, records them into MongoDB, records into file and finds min price.
"""

import datetime
import os
import sys
from configparser import ConfigParser

from Flight_prices_tracker.custom_logger import create_logger
from Flight_prices_tracker.files_cleaner import files_cleaner
from Flight_prices_tracker.get_live_api_results import get_live_api_results
from Flight_prices_tracker.mongodb import connect_to_mongodb, record_json_to_mongodb
from Flight_prices_tracker.process_api_results import get_all_prices, get_min_price, record_results_into_file
from Flight_prices_tracker.process_api_results import get_api_results_from_file, pickle_data, get_pickled_outbound_date


def main():

    # rapidapi
    parser = ConfigParser()
    parser.read('config.ini')
    api_key = parser.get("API", "rapidapi_key")
    base_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/"
    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': api_key
    }

    # mongodb
    instance = 'mongodb://localhost:27017/'
    db = 'skyskanner'
    collection = 'itineraries'

    # request params
    city_from = "Krakow"
    country_from = "Poland"
    city_to = "Tokyo"
    country_to = "Japan"
    country = "PL"
    currency = "UAH"
    locale_lang = "en-US"
    cabin_class = "Economy"
    adults_count = 1
    outbound_date = "2020-03-01"

    # additional params
    days_to_request = 3
    price_threshold = 15000
    max_retries = 3
    json_files_folder = "json_files"
    log_files_folder = "log_files"
    get_results_from_api = True
    debug_results_file = 'Results_debug.json'
    pickle_file = 'Pickled_data.txt'

    cwd = os.getcwd()
    log_file_abs_path = os.path.join(cwd, log_files_folder, f"Logs_{datetime.datetime.now()}.log".replace(":", "-"))

    # create logger and connect to db
    logger = create_logger(log_file_abs_path)
    collection = connect_to_mongodb(mongodb_instance=instance,
                                    mongodb=db,
                                    mongodb_collection=collection,
                                    logger=logger)

    # get data from API or from file
    if get_results_from_api:

        # get API data for N days
        for n in range(days_to_request):

            # get outbound date from picked file (to continue where left off) or use passed date
            pickled_outbound_date = get_pickled_outbound_date(pickle_file=pickle_file,
                                                              city_from=city_from,
                                                              city_to=city_to,
                                                              logger=logger)
            if pickled_outbound_date:
                outbound_date = pickled_outbound_date
                logger.info(f"Found pickled date. Running API request for -> {pickled_outbound_date} ")
            else:
                logger.info(f"No pickled date. Running API request for the passed date -> {outbound_date} ")

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

            # record results to file
            json_file = f"{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}_{city_from}-{city_to}_for_{outbound_date}.json"
            file_abs_path = os.path.join(os.getcwd(), json_files_folder, json_file)

            record_results_into_file(file_abs_path=file_abs_path,
                                     results=all_results,
                                     logger=logger)
            # find next date
            next_outbound_date_datetime = outbound_date_datetime + datetime.timedelta(days=1)
            outbound_date = next_outbound_date_datetime.strftime("%Y-%m-%d")

            # pickle next date (process can resume from this point if occurred issue with API response during the run)
            pickle_data(file_name=pickle_file,
                        data_to_pickle={f"{city_from}-{city_to}": outbound_date},
                        logger=logger)
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

