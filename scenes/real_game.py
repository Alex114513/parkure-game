import pygame
import const
import tools
import json
import scenes.main_title
from sprites.work.masks import mask

#save
Save_name = None

#player data
player_x = None
player_y = None

score = None

level = None

#level data
current_level = None
unlocked_levels = None
level_sprites = None

def init():
    global Save_name
    tools.log(f"initializing real game scene with save name: {Save_name}" , const.DEBUG)

    #loading save data
    save_path = f"saves/{Save_name}"
    try:
        with open(f"{save_path}/player.json", "r") as f:
            player_data = json.load(f)
        with open(f"{save_path}/level.json", "r") as f:
            level_data = json.load(f)
        tools.log("save data loaded successfully" , const.INFO)
    except Exception as e:
        tools.log(f"error loading save data: {e}" , const.ERROR)
        return
    
    tools.log(f"player data: {player_data}" , const.DEBUG)
    tools.log(f"level data: {level_data}" , const.DEBUG)
    #player
    global player_x, player_y, score, level
    player_x = player_data["position"][0]
    player_y = player_data["position"][1]

    score = player_data["score"]
    level = player_data["level"]

    #level
    global current_level, unlocked_levels, level_sprites
    current_level = level_data["current_level"]
    unlocked_levels = level_data["unlocked_levels"]
    level_sprites = level_data[str(current_level)]["enemies"]

    tools.log(f"player position: ({player_x}, {player_y}), score: {score}, level: {level}" , const.DEBUG)
    tools.log(f"current level: {current_level}, unlocked levels: {unlocked_levels}, level sprites: {level_sprites}" , const.DEBUG)

def start(save_name):
    global Save_name

    Save_name = save_name
    tools.log("real game scene start" , const.INFO)
    done = False

    #groups and sprites
    init_start_mask = mask.Mask(const.BLACK)
    scenes.main_title.masks_group.add(init_start_mask)

    #init start mask
    init_start_mask.fade(1) 

    init()

    while not done:
        scenes.main_title.clock.tick(const.FPS)

        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tools.log("game quit" , const.INFO)
                done = True

        #draw
        scenes.main_title.screen.fill(const.DARK_BLUE)
        scenes.main_title.masks_group.update()
        scenes.main_title.masks_group.draw(scenes.main_title.screen)
        pygame.display.update()