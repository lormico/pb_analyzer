import datetime
import traceback

from loguru import logger

from pb_analyzer.configuration import load_config
from pb_analyzer import __version__
from pb_analyzer.client import get_stations, get_prices
from pb_analyzer.mail import prepare_message, send_mail
from pb_analyzer.persistence import get_db_session
from pb_analyzer.persistence.actions import upsert_stations, insert_prices, upsert_metadata
from pb_analyzer.persistence.models import Metadata


@logger.catch
def main():
    """Main entry point of program"""
    config = load_config()
    logger.add(config["LOGGING"]["file_name"], rotation=config["LOGGING"]["rotation"])
    logger.info(f"PrezziBenzina Analyzer - v{__version__}")

    try:
        db_session = get_db_session(config["PERSISTENCE"]["db_file"])
        last_updated = db_session.query(Metadata.value).filter(Metadata.key == "last_updated").scalar()
        if last_updated:
            last_updated = datetime.datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
            logger.debug(f"Last update: {last_updated}")

        # Look for station updates 6 hours since last update
        # May produce duplicates on db, but it's ok, they will be handled
        # Doing this since the API wouldn't return data if filtered too strictly
        stations = get_stations(config["SEARCH"]["min_lat"],
                                config["SEARCH"]["min_long"],
                                config["SEARCH"]["max_lat"],
                                config["SEARCH"]["max_long"],
                                last_updated - datetime.timedelta(hours=6))
        logger.info(f"Found {len(stations)} stations")
        if stations:
            upsert_stations(db_session, stations)

        # Same as above
        prices = get_prices(config["SEARCH"]["min_lat"],
                            config["SEARCH"]["min_long"],
                            config["SEARCH"]["max_lat"],
                            config["SEARCH"]["max_long"],
                            last_updated - datetime.timedelta(hours=6))
        logger.info(f"Found {len(prices)} prices")
        if prices:
            insert_prices(db_session, prices)

        upsert_metadata(db_session, {"last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        # db_session.commit()
        logger.info("Updated the database")
    except Exception:
        logger.exception("Exception while running the main method")
        formatted_exc = traceback.format_exc()
        mail_content = """
        <html>
        <head>
            <style>
            p4 {
                color: black;
                text-align: left;
                font-size: 12px;
                font-family: monospace;
                white-space: pre;
               }
            </style>
        </head>
        <body>
            <p4>An error occurred at %s:</br>%s</p4>
        </body>
        </html>""" % (datetime.datetime.now(), formatted_exc)
        logger.info(f"{mail_content}")
        mail_message = prepare_message(config["MAIL"]["sender"],
                                       config["MAIL"]["recipient"],
                                       "PB Analyzer error",
                                       mail_content)
        send_mail(config["MAIL"]["server"],
                  config["MAIL"]["port"],
                  config["MAIL"]["user"],
                  config["MAIL"]["password"],
                  mail_message)


if __name__ == "__main__":
    main()
