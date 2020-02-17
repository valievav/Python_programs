"""
Gets Live API results, records them into MongoDB, records into file and finds min price.
"""

import datetime
import os
from configparser import ConfigParser
from Flight_prices_tracker.custom_logger import create_logger
from Flight_prices_tracker.files_cleaner import files_cleaner
from Flight_prices_tracker.get_live_api_results import get_api_data_for_n_days
from Flight_prices_tracker.mongodb import connect_to_mongodb
from Flight_prices_tracker.process_api_results import get_all_prices, get_min_price


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
    outbound_date = "2020-05-01"

    # additional params
    days_to_request = 3
    price_threshold = 15000
    max_retries = 3
    json_files_folder = "json_files"
    log_files_folder = "log_files"
    json_file = f"xxx_{city_from}-{city_to}_from_{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.json"
    log_file = f"Logs_{datetime.datetime.now()}.log".replace(":", "-")
    pickle_file = 'Pickled_data.txt'

    # create logger
    cwd = os.getcwd()
    log_file_abs_path = os.path.join(cwd, log_files_folder, log_file)
    logger = create_logger(log_file_abs_path)

    # connect to db
    collection = connect_to_mongodb(mongodb_instance=instance,
                                    mongodb=db,
                                    mongodb_collection=collection,
                                    logger=logger)

    # get LIVE API results, record values to db
    get_api_data_for_n_days(days=days_to_request,
                            pickle_file=pickle_file,
                            base_url=base_url,
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
                            json_files_folder=json_files_folder,
                            json_file=json_file,
                            collection=collection,
                            logger=logger,
                            save_to_file=True)

    # TODO - get prices from mongodb
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

