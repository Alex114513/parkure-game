import logging
import json
import global_var
from logging.handlers import RotatingFileHandler
import const
from pathlib import Path
import pygame
from pygame import math

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="parkure.log",
    filemode="w"
)

exit_requested = False


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
                {"position": [0, 150], "size": [100, 20], "rotation": 0},
                {"position": [200, 300], "size": [150, 20], "rotation": 0}
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

def axis_aligned_bbox_from_rect(rect, angle):
    cx, cy = rect.center
    w, h = rect.size
    corners = [
        math.Vector2(-w/2, -h/2),
        math.Vector2( w/2, -h/2),
        math.Vector2( w/2,  h/2),
        math.Vector2(-w/2,  h/2),
    ]
    rotated = [math.Vector2(cx, cy) + p.rotate(angle) for p in corners]
    xs = [p.x for p in rotated]; ys = [p.y for p in rotated]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)#, rotated  # 返回包围盒和四个顶点

def request_exit():
    """Mark the app as exiting and clear any queued scene-switch state."""
    global exit_requested
    exit_requested = True
    clear_scene_transition_timers()
    log("TOOLS: exit requested", const.INFO)


def reset_exit_request():
    """Clear the global exit-request flag for a new scene loop."""
    global exit_requested
    exit_requested = False
    log("TOOLS: exit request reset", const.DEBUG)


def clear_scene_transition_timers():
    """Clear pending scene-switch timers and queued events so stale transitions do not fire in the next scene."""
    for event_code in (
        const.SWITCH_TO_GAME_EVENT_CODE,
        const.SWITCH_TO_NEW_SAVE_EVENT_CODE,
        const.SWITCH_TO_LOAD_SAVE_EVENT_CODE,
        const.SWITCH_TO_REAL_GAME_EVENT_CODE,
        const.SWICH_TO_GAME_PREP_EVENT_CODE,
        const.SWITCH_TO_MAIN_TITLE_EVENT_CODE
    ):
        pygame.time.set_timer(event_code, 0)

    pygame.event.clear()
    log("TOOLS: cleared scene transition timers and queued events", const.INFO)


def kill_buttons():
    from scenes import main_title
    import scenes.game_prep as game_prep
    import scenes.new_save as new_save
    for button in main_title.buttons_group:
        button.kill()
    for button in game_prep.buttons_group:
        button.kill()
    for button in new_save.buttons_group:
        button.kill()
    if new_save.ui_group != None:
        for ui in new_save.ui_group:
            ui.kill()
    if global_var.return_button_group != None:
        for item in global_var.return_button_group:
            item.kill()

    log("TOOLS: deleted all buttons", const.INFO)


def clear_masks():
    """Remove all active overlay masks so new scenes do not inherit old black screens."""
    from scenes import main_title
    for mask in list(main_title.masks_group):
        mask.kill()
    log("TOOLS: cleared masks", const.INFO)


def prepare_for_new_scene():
    """runs kill_buttons() and clear_scene_transition_timers() to get ready for scene swich"""
    kill_buttons()
    clear_masks()
    clear_scene_transition_timers()