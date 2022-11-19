import datetime

from loguru import logger

from pb_analyzer import load_config
from pb_analyzer.__version__ import __version__
from pb_analyzer.client import get_stations, get_prices
from pb_analyzer.persistence import get_db_session
from pb_analyzer.persistence.models import Metadata
from pb_analyzer.persistence.actions import upsert_stations, insert_prices, upsert_metadata


@logger.catch
def main():
    """Main entry point of program"""
    config = load_config()
    logger.add(config["LOGGING"]["file_name"], rotation=config["LOGGING"]["rotation"])
    logger.info(f"PrezziBenzina Analyzer - v{__version__}")

    db_session = get_db_session(config["PERSISTENCE"]["db_file"])
    last_updated = db_session.query(Metadata.value).filter(Metadata.key == "last_updated").scalar()
    if last_updated:
        last_updated = datetime.datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")

    stations = get_stations(config["SEARCH"]["min_lat"],
                            config["SEARCH"]["min_long"],
                            config["SEARCH"]["max_lat"],
                            config["SEARCH"]["max_long"],
                            last_updated)
    logger.info(f"Found {len(stations)} stations")
    if stations:
        upsert_stations(db_session, stations)

    prices = get_prices(config["SEARCH"]["min_lat"],
                        config["SEARCH"]["min_long"],
                        config["SEARCH"]["max_lat"],
                        config["SEARCH"]["max_long"],
                        last_updated)
    logger.info(f"Found {len(prices)} prices")
    if prices:
        insert_prices(db_session, prices)

    upsert_metadata(db_session, {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    db_session.commit()
    logger.info("Updated the database")


if __name__ == "__main__":
    main()
