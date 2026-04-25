import pygame
import const
import tools
import json
import scenes.main_title
from sprites.player import Player
from sprites.work.masks import mask
from pygame.locals import *

#save
Save_name = None

#player data
player_x = None
player_y = None

player = Player(0, 0) #placeholder, will be updated in init()

score = None
level = None
player_name = None

player_acc = None
player_max_speed = None
player_friction = None
player_gravity = None

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
        with open(f"configs/players/{player_data['name']}..json", "r") as f:
            player_config = json.load(f)
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
    player_name = player_data["name"]

    #physics attributes
    player_acc = player_config["accseleration"]
    player_max_speed = player_config["max_speed"]
    player_friction = player_config["friction"]
    player_gravity = player_config["gravity"]


    #level
    global current_level, unlocked_levels, level_sprites
    current_level = level_data["current_level"]
    unlocked_levels = level_data["unlocked_levels"]
    level_sprites = level_data[str(current_level)]["enemies"]

    tools.log(f"player position: ({player_x}, {player_y}), score: {score}, level: {level}" , const.DEBUG)
    tools.log(f"current level: {current_level}, unlocked levels: {unlocked_levels}, level sprites: {level_sprites}" , const.DEBUG)
    tools.log(f"player accseleration: {player_acc}, player max speed: {player_max_speed}" , const.DEBUG)

    #TODO: initialize level sprites based on level_sprites data
    player.rect.x = player_x
    player.rect.y = player_y
    player.score = score
    player.level = level
    player.name = player_name
    player.accseleration = player_acc
    player.max_speed = player_max_speed
    player.friction = player_friction
    player.gravity = player_gravity

def start(save_name):
    global Save_name

    Save_name = save_name
    tools.log("real game scene start" , const.INFO)
    done = False

    #groups and sprites
    init_start_mask = mask.Mask(const.BLACK)
    scenes.main_title.masks_group.add(init_start_mask)

    player_group = pygame.sprite.Group()
    player_group.add(player)

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
            
            if event.type == VIDEORESIZE:
                #resize window
                scenes.main_title.screen = pygame.display.set_mode((event.w , event.h) , RESIZABLE)
                tools.log(f"window resized to w:{event.w}h:{event.h}" , const.INFO)
                const.SCREEN_RESIZE.send(data=(const.SCREEN_RESIZE_CODE, (event.w, event.h)))
                scenes.main_title.window_size = (event.w, event.h)
            
        
        #keys
        keys = pygame.key.get_pressed()
        #player movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.velocity_x -= player.accseleration[0]
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.velocity_x += player.accseleration[0]


        #draw
        scenes.main_title.screen.fill(const.DARK_BLUE)
        scenes.main_title.masks_group.update()
        scenes.main_title.masks_group.draw(scenes.main_title.screen)
        player_group.update()
        player_group.draw(scenes.main_title.screen)
        pygame.display.update()