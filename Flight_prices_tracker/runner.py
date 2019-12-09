from configparser import ConfigParser
from get_api_prices import get_place_id
from get_api_prices import get_live_api_prices


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
                        origin_place, destination_place, outbound_date, adults_number,
                        price_threshold, prices_count_threshold)


if __name__ == "__main__":
    main()
