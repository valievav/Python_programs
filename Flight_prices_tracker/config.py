import datetime
from Flight_prices_tracker.config_private_keys import *

# RAPID_API
base_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/"
headers = {'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
           'x-rapidapi-key': rapidapi_key}  # use private api key

# MONGODB
instance = 'mongodb://localhost:27017/'
db = 'skyskanner'
db_collection = 'itineraries'

# REQUEST_PARAMS
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

# ADDITIONAL_PARAMS
days_to_request = 3
price_threshold = 15000
max_retries = 3
json_files_folder = "json_files"
log_files_folder = "log_files"
json_file = f"{datetime.datetime.now().strftime('%Y-%m-%d')}_for_{city_from}-{city_to}_xxx.json"
log_file = f"Logs_{datetime.datetime.now()}.log".replace(":", "-")
pickle_file = 'pickled_date.txt'
save_to_file = True
log_files_to_keep = 10
