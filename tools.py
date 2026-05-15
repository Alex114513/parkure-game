import logging
import json
from logging.handlers import RotatingFileHandler
import const
from pathlib import Path
import pygame

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
    """Creates a new save file for the player with the given name. The save file will contain default player data and level data.
    format of save data:
        saves/save_name/player.json{
            "name": "player1",
            "level": 1,
            "score": 0,
            "position": [0, 0]
        }
        saves/save_name/level.json{
            "current_level": 1,
            "unlocked_levels": [1],
            "lv1": {
                "enemies": [
                    {"type": "enemy1", "position": [100, 100]},
                    {"type": "enemy2", "position": [200, 200]}
                ]
            }

        }"""
    log("save game function called" , const.DEBUG)

    #path for save file
    save_path = Path(f"saves/{name}")
    save_path.mkdir(parents=True, exist_ok=True)

    #sprite data
    player_data = {
        "name": name,
        "level": 1,
        "score": 0,
        "position": [0, 0]
    }

    #level data
    level_data = {
        "current_level": 1,
        "unlocked_levels": [1],
        "1": {
            "enemies": [
                {"type": "enemy1", "position": [100, 100]},
                {"type": "enemy2", "position": [200, 200]}
            ],
            "platforms": [
                {"position": [0, 150], "size": [100, 20]},
                {"position": [200, 300], "size": [150, 20]}
            ]
        }

    }
    try:
        (save_path / "player.json").write_text(json.dumps(player_data, indent=4))
        (save_path / "level.json").write_text(json.dumps(level_data, indent=4))
        log("game saved successfully" , const.INFO)
    except Exception as e:
        log(f"error saving game: {e}" , const.ERROR)

def Check_time(max):
    """used to check if the time since the last call to this function is greater than the given max time. This can be used to limit how often certain actions can be performed, such as attacking or using a skill."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = pygame.time.get_ticks()
            func(*args, **kwargs)
            end_time = pygame.time.get_ticks()
            if end_time - start_time > max:
                log(f"{func.__name__} used {end_time - start_time} ms since last use, wich exeded{max}ms." , const.WARNING)
            else:
                log(f"{func.__name__} used {end_time - start_time} ms since last use, wich is within the limit of {max}ms." , const.INFO)

        return wrapper
    return decorator
