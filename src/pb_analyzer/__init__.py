import configparser
from typing import Dict, List

import requests

API_URL = "https://api3.prezzibenzina.it/"
DEFAULT_CONFIG_FILE = "../../config.ini"

JsonObject = Dict[str, str]


def load_config(config_file=DEFAULT_CONFIG_FILE):
    config = configparser.ConfigParser()
    config.read(config_file)
    return dict(config["SEARCH"])


def get_stations(min_lat, min_long, max_lat, max_long) -> Dict[str, JsonObject]:
    """
    TODO iterate if limit is reached

    :param min_lat:
    :param min_long:
    :param max_lat:
    :param max_long:
    :return:
    """
    request = requests.PreparedRequest()
    url = API_URL
    params = {
        "do": "pb_get_stations",
        "output": "json",
        "limit": "500",
        "appname": "AndroidFuel",
        "min_lat": min_lat,
        "min_long": min_long,
        "max_lat": max_lat,
        "max_long": max_long,
    }
    request.prepare_url(url, params)
    response = requests.post(request.url, verify=False)
    station_list = response.json()['pb_get_stations']['stations']['station']
    return dict([(station['id'], station) for station in station_list])


def get_prices(min_lat, min_long, max_lat, max_long) -> List[JsonObject]:
    """
    TODO

    :param min_lat:
    :param min_long:
    :param max_lat:
    :param max_long:
    :return:
    """
    request = requests.PreparedRequest()
    url = API_URL
    params = {
        "do": "pb_get_prices",
        "output": "json",
        "limit": "500",
        "appname": "AndroidFuel",
        "min_lat": min_lat,
        "min_long": min_long,
        "max_lat": max_lat,
        "max_long": max_long,
    }
    request.prepare_url(url, params)
    response = requests.post(request.url, verify=False)
    return response.json()['pb_get_prices']['prices']['price']
