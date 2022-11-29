import configparser
import os
from importlib.resources import files

import appdirs
from loguru import logger

from . import templates

CONFIG_DIR = appdirs.user_data_dir("pb_analyzer", "lormico")
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_DIR, "config.ini")
CONFIG_STRUCTURE = {
    "SEARCH": {
        "min_lat": float,
        "min_long": float,
        "max_lat": float,
        "max_long": float,
    },
    "PERSISTENCE": {
        "db_file": str,
    },
    "LOGGING": {
        "file_name": str,
        "rotation": str,
    },
    "MAIL": {
        "server": str,
        "port": int,
        "user": str,
        "password": str,
        "sender": str,
        "recipient": str,
    }
}


def _create_default_config_file():
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    with files(templates).joinpath("config.ini.template").open() as template, open(DEFAULT_CONFIG_FILE, "w") as config:
        config.writelines(template.readlines())


def _validate_config(config: configparser.ConfigParser):
    try:
        assert all(section in config for section in CONFIG_STRUCTURE.keys())
        return True
    except AssertionError:
        logger.exception("duh")
        return False


def load_config(config_file=DEFAULT_CONFIG_FILE):
    if not os.path.isfile(config_file) and config_file != DEFAULT_CONFIG_FILE:
        logger.warning(f"Specified configuration file ({config_file}) not found, falling back to defaults")
        config_file = DEFAULT_CONFIG_FILE

    if not os.path.isfile(config_file):
        logger.warning(f"Default configuration file ({config_file}) not initialized, creating template")
        _create_default_config_file()
        return None

    logger.debug(f"Reading configuration from {config_file}")
    config = configparser.ConfigParser()
    config.read(config_file)
    if not _validate_config(config):
        logger.error("Invalid configuration!")
        exit(1)  # TODO
    logger.debug("Done reading configuration")
    return config
