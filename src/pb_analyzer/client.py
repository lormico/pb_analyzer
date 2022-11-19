from typing import Dict, List

import requests

API_URL = "https://api3.prezzibenzina.it/"

JsonObject = Dict[str, str]


def get_stations(min_lat, min_long, max_lat, max_long, updated_since=False) -> Dict[str, JsonObject]:
    """
    TODO iterate if limit is reached

    :param min_lat:
    :param min_long:
    :param max_lat:
    :param max_long:
    :param updated_since:
    :return:
    """
    request = requests.PreparedRequest()
    url = API_URL
    params = dict(
        do="pb_get_stations",
        output="json",
        limit="500",
        appname="AndroidFuel",
        min_lat=min_lat,
        min_long=min_long,
        max_lat=max_lat,
        max_long=max_long,
    )
    if updated_since:
        params['upd_from'] = updated_since

    request.prepare_url(url, params)
    response_json = requests.post(request.url).json()
    status = response_json['pb_get_stations']['status']
    if status == "error":
        return {}
    else:
        station_list = response_json['pb_get_stations']['stations']['station']
        return dict([(station['id'], station) for station in station_list])


def get_prices(min_lat, min_long, max_lat, max_long, updated_since=False) -> List[JsonObject]:
    """
    TODO

    :param min_lat:
    :param min_long:
    :param max_lat:
    :param max_long:
    :param updated_since:
    :return:
    """
    request = requests.PreparedRequest()
    url = API_URL
    params = dict(
        do="pb_get_prices",
        output="json",
        limit="500",
        appname="AndroidFuel",
        min_lat=min_lat,
        min_long=min_long,
        max_lat=max_lat,
        max_long=max_long,
    )
    if updated_since:
        params['upd_from'] = updated_since

    request.prepare_url(url, params)
    response_json = requests.post(request.url).json()
    status = response_json['pb_get_prices']['status']
    if status == "error":
        return []
    else:
        return response_json['pb_get_prices']['prices']['price']
