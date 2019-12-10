from configparser import ConfigParser
from get_api_prices import get_place_id
from get_api_prices import get_live_api_prices
import logging
import datetime


def main():

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
    outbound_date = "2019-12-21"
    cabin_class = "Economy"
    adults_number = 1

    price_threshold = 15000
    prices_count_threshold = 50

    # get FROM and TO city ids
    origin_place = get_place_id(base_url=base_url,
                                headers=headers,
                                currency=currency,
                                locale_lang=locale_lang,
                                search_city=search_city_from,
                                search_country=search_country_from)
    destination_place = get_place_id(base_url=base_url,
                                     headers=headers,
                                     currency=currency,
                                     locale_lang=locale_lang,
                                     search_city=search_city_to,
                                     search_country=search_country_to)

    # record logs into log file
    log_file = f"Logs_{datetime.datetime.now()}.log".replace(":", "-")
    logging.basicConfig(filename=log_file,
                        level=logging.DEBUG,
                        format=' %(asctime)s - %(levelname)s - %(message)s',
                        filemode="w")
    logging.getLogger().setLevel(logging.DEBUG)

    # run LIVE API search
    if origin_place and destination_place:
        get_live_api_prices(base_url=base_url,
                            headers=headers,
                            cabin_class=cabin_class,
                            country=country,
                            currency=currency,
                            locale_lang=locale_lang,
                            origin_place=origin_place,
                            destination_place=destination_place,
                            outbound_date=outbound_date,
                            adults_number=adults_number,
                            price_threshold=price_threshold,
                            prices_count_threshold=prices_count_threshold)


if __name__ == "__main__":
    main()

