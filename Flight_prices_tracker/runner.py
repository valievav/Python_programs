"""
Gets Live API results, records them into MongoDB, records into file and finds min price.
"""

import os
from Flight_prices_tracker.custom_logger import create_logger
from Flight_prices_tracker.files_cleaner import files_cleaner
from Flight_prices_tracker.get_live_api_results import get_api_data_for_n_days
from Flight_prices_tracker.mongodb_methods import connect_to_mongodb, find_flights_with_low_prices
from Flight_prices_tracker.config import *


def main():

    # create logger
    cwd = os.getcwd()
    logger = create_logger(os.path.join(cwd, log_files_folder, log_file))

    # connect to db
    collection = connect_to_mongodb(mongodb_instance=instance,
                                    mongodb=db,
                                    mongodb_collection=db_collection,
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
                            save_to_file=save_to_file)

    # find flights with price < threshold
    find_flights_with_low_prices(threshold=price_threshold,
                                 search_date=outbound_date,
                                 collection=collection,
                                 logger=logger)

    # clean up log files
    log_path_to_clean = os.path.join(cwd, log_files_folder)
    files_cleaner(path_to_clean=log_path_to_clean,
                  extension='log',
                  to_keep_number=log_files_to_keep,
                  logger=logger)


if __name__ == "__main__":
    main()

