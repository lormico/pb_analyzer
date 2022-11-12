import configparser
import datetime
import urllib.parse

import requests
from requests import PreparedRequest

BASE_URL = "https://www.prezzibenzina.it/www2/develop/tech/handlers/"
DEFAULT_CONFIG_FILE = "../../config.ini"
COMMON_HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
}


def load_config(config_file=DEFAULT_CONFIG_FILE):
    config = configparser.ConfigParser()
    config.read(config_file)
    return dict(config["USER"]) | dict(config["SEARCH"])


def get_user_cookies(username, password):
    request = PreparedRequest()
    url = urllib.parse.urljoin(BASE_URL, "user_handler.php")
    params = {
        "sel": "login",
        "user": username,
        "pass": password,
        "rand": int(datetime.datetime.now().timestamp() * 1000)
    }
    headers = COMMON_HEADERS

    request.prepare_url(url, params)
    response = requests.get(request.url, headers=headers, verify=False)
    if response.text and response.cookies:
        return response.cookies.get_dict()


def get_prices(user_cookies, min_lat, min_long, max_lat, max_long, fuel):
    request = PreparedRequest()
    url = urllib.parse.urljoin(BASE_URL, "search_handler.php")
    params = {
        "sel": "getStationsTab",
        "min_lat": min_lat,
        "min_long": min_long,
        "max_lat": max_lat,
        "max_long": max_long,
        "brand": None,
        "fuels": fuel,
        "rand": int(datetime.datetime.now().timestamp() * 1000)
    }
    headers = COMMON_HEADERS

    request.prepare_url(url, params)
    response = requests.get(request.url, headers=headers, cookies=user_cookies, verify=False)
    return response.json()
