import logging
import json
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

def new_save(name):
    log("save game function called" , const.DEBUG)
    
    #sprite data
    player_data = {
        "name": name,
        "level": 1,
        "score": 0
    }

    #level data
    level_data = {
        "current_level": 1,
        "unlocked_levels": [1],
        "lv1": {
            "enemies": [
                {"type": "enemy1", "position": [100, 100]},
                {"type": "enemy2", "position": [200, 200]}
            ]
        }

    }
    try:
        with open(f"saves/{name}/player.json", "w") as f:
            json.dump(player_data, f)
        with open(f"saves/{name}/level.json", "w") as f:
            json.dump(level_data, f)
        log("game saved successfully" , const.INFO)
    except Exception as e:
        log(f"error saving game: {e}" , const.ERROR)