import requests
import bs4
import re


def get_product_data(url: str, user_agent: dict):
    """
    Returns product brand, title, price, discount_price and currency_code from provided url
    :param url: str
    :param user_agent: dict
    :return: brand, title, price, discount_price, currency_code
    """

    def find_price_and_discount(price_line: str):
        """
        Finds price and discount_price in a str line: price is 1-st number, discount_price is 2-nd number.\n
        Price should be with comma or dot like so: 123.00 or 123,00.
        """

        price, discount_price = None, None
        prices = [x for x in re.findall(r"\d+[.|,]\d+", price_line)]

        if len(prices) == 2:
            price = prices[0]
            discount_price = prices[1]
        elif len(prices) == 1:
            price = prices[0]
        elif len(prices) > 2:
            print(f"DETECTED > 2 Price values - {prices}! Skipping values.")

        return price, discount_price

    # get page html
    page = requests.get(url, headers=user_agent)
    page.raise_for_status()

    soup = bs4.BeautifulSoup(page.content, features="html.parser")

    # find elements on page
    brand = soup.findAll('div', class_='h-m-bottom-m')[0].getText(separator=u' ')
    title = soup.findAll('div', class_='h-m-bottom-m')[1].getText(separator=u' ')
    price_line = soup.find('div', class_='h-product-price topSection').getText(separator=u' ').replace('\xa0', ' ')

    price, discount_price = find_price_and_discount(price_line)
    currency_code = ""  # TODO

    return brand, title, price, discount_price, currency_code


if __name__ == "__main__":

    url = "https://www.zalando.pl/musse-and-cloud-wenda-botki-na-platformie-mue11n00k-q11.html"
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"}

    params = ["BRAND", "TITLE", "PRICE", "DISCOUNT_PRICE", "CURRENCY_CODE", "URL"]
    brand, title, price, discount_price, currency_code = get_product_data(url, header)
    for pair in (zip(params, [brand, title, price, discount_price, currency_code, url])):
        print(pair)


