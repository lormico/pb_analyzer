import pprint

from pb_analyzer import load_config, get_user_cookies, get_prices


def main():
    config = load_config()
    user_cookies = get_user_cookies(config["username"], config["password"])
    prices = get_prices(user_cookies,
                        config["min_lat"],
                        config["min_long"],
                        config["max_lat"],
                        config["max_long"],
                        config["fuels"])

    pp = pprint.PrettyPrinter()
    pp.pprint(dict([(station['price'], (station['name'], station['last_update'])) for station in prices]))


if __name__ == "__main__":
    main()
