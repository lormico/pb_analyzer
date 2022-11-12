from pb_analyzer import load_config, get_stations, get_prices


def main():
    config = load_config()
    stations = get_stations(config["min_lat"],
                            config["min_long"],
                            config["max_lat"],
                            config["max_long"])
    print(f"found {len(stations)} stations")

    prices = get_prices(config["min_lat"],
                        config["min_long"],
                        config["max_lat"],
                        config["max_long"])

    for price in sorted(prices, key=lambda p: p['date'], reverse=True):
        if price["fuel"] != config["fuel"]:
            continue
        station = stations[price["station"]]
        print(f"{station['name']} ({station['address']}): {price['price']} {price['service']} ({price['date']})")


if __name__ == "__main__":
    main()
