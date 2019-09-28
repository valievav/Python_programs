import requests
import json
import datetime
import smtplib
from configparser import ConfigParser


def umbrella_reminder(api_call, number_of_timestamps, return_forecast, return_json):
    """
    Makes API forecast call to see if it's going to rain in the nearest hours.\n
    Returns rain forecast message, short forecast weather description* and raw json data*.\n
    `* if requested \n
    :param api_call: valid API call link
    :param number_of_timestamps: int
    :param return_forecast: bool
    :param return_json: bool
    :return: rain_hours - list, forecast_weather - dict, json_data - dict
    """

    # make an api call
    api_response = requests.get(api_call)
    api_response.raise_for_status()

    # get api response
    json_data = api_response.json()

    # iterate through json and find weather for timestamps
    rain_hours = []
    forecast_weather = {}

    for timestamp in range(number_of_timestamps):
        date_js = json_data['list'][timestamp]['dt_txt']
        date = datetime.datetime.strptime(date_js, "%Y-%m-%d %H:%M:%S")
        hour = date.strftime("%H:%M")
        weather_js = json_data['list'][timestamp]['weather'][0]['main']

        # record rain hours
        if weather_js.lower() == 'rain':
            rain_hours.append(hour)

        # record short weather
        forecast_weather.setdefault(date, weather_js)

    return rain_hours, forecast_weather if return_forecast else None, json_data if return_json else None


def send_email(server_smtp, server_smtp_port, email_sender, password_sender, email_recipient, email_subject, email_body):
    """
    Sends email using provided sender and recipient data as well as email subject and body.\n
    :param server_smtp: str
    :param server_smtp_port: int
    :param email_sender: valid email
    :param password_sender: str
    :param email_recipient: valid email
    :param email_subject: str
    :param email_body: str
    :return: 0 if failed, 1 if successfully sent
    """
    # connect to server
    smtp_obj = smtplib.SMTP(server_smtp, server_smtp_port)
    smtp_obj.ehlo()
    smtp_obj.starttls()
    smtp_obj.login(email_sender, password_sender)

    # send email
    send_email = smtp_obj.sendmail(email_sender, email_recipient, f'Subject:{email_subject}\n\n{email_body}')

    return 1 if send_email == {} else 0


if __name__ == "__main__":
    parser = ConfigParser()
    parser.read('config.ini')

    # run rain check
    city_name = "krakow"
    country_code = "pl"
    api_key = parser.get("API", "openweathermap_api_key")
    number_of_results = 4  # number of timestamps for 1 day (weather is provided for every 3 hours) - used 1/2 day
    api_weather_call = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name},{country_code}&units=metric&cnt={number_of_results}&APPID={api_key}"
    show_forecast = True
    show_json_data = False

    rain_hours, forecast_weather, json_data = umbrella_reminder(api_weather_call, number_of_results, show_forecast, show_json_data)

    # prepare email_body (combine rain alert, short weather and json if requested)
    print_separator = '-' * 20
    results = ''
    if rain_hours:
        results += f"ATTENTION!>>> Please take your UMBRELLA. It's going to rain at around {', '.join(rain_hours)}.\n"
    if show_forecast:
        results += f"{print_separator}\nShort weather forecast for the next {number_of_results * 3} hours for city {city_name.upper()}:\n"
        for v, k in forecast_weather.items():
            results += f"{v} - {k}\n"
    if show_json_data:
        results += f"{print_separator}\nRaw JSON data:\n{json.dumps(json_data, indent=6)}"

    # send email with alert
    smtp = 'smtp.gmail.com'
    smtp_port = '587'
    email_from = parser.get('EMAIL', 'email')
    password = parser.get('EMAIL', 'email_password')
    email_to = parser.get('EMAIL', 'email')
    subject = 'RAIN Alert'

    email_sent = send_email(smtp, smtp_port, email_from, password, email_to, subject, results)
    if email_sent:
        print(f'SUCCESS - Sent email to {email_to} with subject "{subject}"')
    else:
        print(f'FAIL - Cannot send email to {email_to} with subject "{subject}"')

