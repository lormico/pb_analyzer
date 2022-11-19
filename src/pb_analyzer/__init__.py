import configparser

from loguru import logger

DEFAULT_CONFIG_FILE = "../../config.ini"

def load_config(config_file=DEFAULT_CONFIG_FILE):
    logger.debug(f"Reading configuration from {config_file}")
    config = configparser.ConfigParser()
    config.read(config_file)
    logger.debug("Done reading configuration")
    return config
