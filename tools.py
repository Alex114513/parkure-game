import logging
from logging.handlers import RotatingFileHandler
import const

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="parkure.log",
    filemode="w"
)

def log(log , type):
    if type == const.DEBUG:
        logging.debug(log)
    elif type == const.INFO:
        logging.info(log)
    elif type == const.WARNING:
        logging.warning(log)
    elif type == const.ERROR:
        logging.error(log)
    elif type == const.CRIC:
        logging.critical(log)

def save_game():
    log("save game function called" , const.DEBUG)
    pass