import pygame
import const
import tools
import json
import scenes.main_title
import global_var
from sprites.player import Player
from sprites.work.masks import mask
from pygame.locals import *
from sprites.ground.platform import Platform
from sprites.enemys.normal import Normal_enemy

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
player_air_friction = None
player_gravity = None
player_jump_strength = None

#level data
current_level = None
unlocked_levels = None
level_sprites = None

#global groups
platforms_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
done = False

#funcnial variables
should_jump_to_main_title = False

@tools.Check_time(10)
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
        with open(f"configs/players/player1.json", "r") as f:
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
    player_air_friction = player_config["air_friction"]
    player_gravity = player_config["gravity"]
    player_jump_strength = player_config["jump_strength"]


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
    player.air_friction = player_air_friction
    player.gravity = player_gravity
    player.jump_strength = player_jump_strength

    #sumon platforms, enemies, etc based on level_sprites data

    this_level_data = level_data[str(current_level)]

    #platforms
    for platform in this_level_data["platforms"]:
        pos = platform["position"]
        size = platform["size"]
        rotation = platform["rotation"]
        new_platform = Platform(pos[0], pos[1], size[0], size[1], rotation)
        platforms_group.add(new_platform)
        tools.log(f"platform created at position: {pos} with size: {size} and rotation: {rotation}" , const.DEBUG)
        #add new_platform to the appropriate sprite group for platforms
    
    #enemys
    for enemy in this_level_data["enemies"]:
        this_pos = enemy["position"]
        this_type = enemy["type"]
        if this_type == const.NORMAL_ENEMY:
            new_enemy = Normal_enemy(this_pos[0], this_pos[1])

        enemies_group.add(new_enemy)
        tools.log(f"REAL_GAME/INIT: Created new enemy at {this_pos} with type {this_type}", const.INFO)

def reload_level():
    global current_level, unlocked_levels, level_sprites
    platforms_group.empty()
    try:
        with open(f"saves/{Save_name}/level.json", "r") as f:
            level_data = json.load(f)
    except Exception as e:
        tools.log(f"error loading save data for reloading ground: {e}" , const.ERROR)
        return
    
    tools.log(f"level data: {level_data}" , const.DEBUG)

    this_level_data = level_data[str(current_level)]

    #platforms
    for platform in this_level_data["platforms"]:
        pos = platform["position"]
        size = platform["size"]
        rotation = platform["rotation"]
        new_platform = Platform(pos[0], pos[1], size[0], size[1], rotation)
        platforms_group.add(new_platform)
        tools.log(f"platform created at position: {pos} with size: {size} and rotation: {rotation}" , const.DEBUG)
        #add new_platform to the appropriate sprite group for platforms
    
    #level
    current_level = level_data["current_level"]
    unlocked_levels = level_data["unlocked_levels"]
    level_sprites = level_data[str(current_level)]["enemies"]

def start(save_name):
    global Save_name, done, should_jump_to_main_title

    tools.reset_exit_request()
    Save_name = save_name
    tools.log("real game scene start" , const.INFO)
    done = False
    paused = False
    should_jump_to_main_title = False

    #groups and sprites
    init_start_mask = mask.Mask(const.BLACK)
    scenes.main_title.masks_group.add(init_start_mask)

    player_group = pygame.sprite.Group()
    player_group.add(player)

    #init start mask
    init_start_mask.fade(1) 

    init()

    while not done:
        const.CLOCK.tick(const.FPS)
        if paused:
            continue
        #events
        events = pygame.event.get()
        if any(event.type == pygame.QUIT for event in events):
            tools.log("game quit" , const.INFO)
            tools.request_exit()
            done = True
            continue
            
        for event in events:
            if event.type == VIDEORESIZE:
                #resize window
                scenes.main_title.screen = pygame.display.set_mode((event.w , event.h) , RESIZABLE)
                global_var.window_size = (event.w, event.h)
                tools.log(f"window resized to w:{event.w}h:{event.h}" , const.INFO)
                const.SCREEN_RESIZE.send(data=(const.SCREEN_RESIZE_CODE, (event.w, event.h)))
                scenes.main_title.window_size = (event.w, event.h)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if player.on_ground:
                        player.velocity_y -= player.jump_strength
                
                #change platform size in edit mode
                if global_var.Edit_mode_currsor:
                    cursor = global_var.Edit_mode_currsor
                    if event.key == pygame.K_LEFT:
                        cursor.target_platform_size = (
                            max(10, cursor.target_platform_size[0] - 10), 
                            cursor.target_platform_size[1]
                        )
                        cursor.image = pygame.transform.scale(
                            cursor.image, 
                            cursor.target_platform_size
                        )
                    if event.key == pygame.K_RIGHT:
                        cursor.target_platform_size = (
                            max(10, cursor.target_platform_size[0] + 10), 
                            cursor.target_platform_size[1]
                        )
                        cursor.image = pygame.transform.scale(
                            cursor.image, 
                            cursor.target_platform_size
                        )

                    if event.key == pygame.K_UP:
                        cursor.target_platform_size = (
                            cursor.target_platform_size[0],
                            max(10, cursor.target_platform_size[1] - 10)
                        )
                        cursor._refresh_image()
                    if event.key == pygame.K_DOWN:
                        cursor.target_platform_size = (
                            cursor.target_platform_size[0],
                            max(10, cursor.target_platform_size[1] + 10)
                        )
                        cursor._refresh_image()
                    if event.key == pygame.K_r:
                        cursor.target_platform_rotation = (cursor.target_platform_rotation + 15) % 360
                        cursor._refresh_image()
                    if event.key == pygame.K_e:
                        cursor.target_platform_rotation = (cursor.target_platform_rotation - 15) % 360
                        cursor._refresh_image()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: #left click
                    if player.edit_mode:
                        #let currsor place a platform
                        tools.log(f"placing platform at cursor position: {global_var.Edit_mode_currsor.rect.topleft}" , const.DEBUG)
                        global_var.Edit_mode_currsor.place_platform()
                if event.button == 3: #right click
                    if player.edit_mode:
                        #let currsor remove a platform
                        tools.log(f"trying to remove platform at cursor position: {global_var.Edit_mode_currsor.rect.topleft}" , const.DEBUG)
                        global_var.Edit_mode_currsor.remove_platform()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    if const.debug_mode:
                        if player.edit_mode:
                            tools.log(f"Edit mode disabled", const.INFO)
                            player.edit_mode = False
                            global_var.Edit_mode_currsor = None
                        else:    
                            tools.log(f"Edit mode enabled", const.INFO)
                            player.edit_mode = True
                            player.init_edit_mode() #reset player physics attributes to default values for edit mode
                    else:
                        tools.log(f"Could not enable edit mode, because debug mode is {const.debug_mode}", const.INFO)
                #pause menu
                if event.key == pygame.K_ESCAPE:
                    tools.log(f"pause menu opened", const.INFO)
                    from scenes.pause_menu import start as pause_menu_start
                    paused = True
                    should_exit = pause_menu_start(Save_name)
                    paused = False
                    tools.log(f"pause menu closed", const.INFO)
                    if should_exit == 1:
                        done = True
                        tools.log("game exit requested from pause menu", const.INFO)
                    elif should_exit == 3:
                        #reload level data after pause menu is closed
                        reload_level()
                    else:
                        tools.log("returning to main menu from pause menu", const.INFO)
                        should_jump_to_main_title = True
                        done = True

        #draw
        scenes.main_title.screen.fill(const.DARK_BLUE)
        scenes.main_title.masks_group.update()
        scenes.main_title.masks_group.draw(scenes.main_title.screen)
        platforms_group.draw(scenes.main_title.screen)
        player_group.update()
        platforms_group.update()
        enemies_group.update()
        enemies_group.draw(scenes.main_title.screen)
        player_group.draw(scenes.main_title.screen)
        if global_var.Edit_mode_currsor:
            scenes.main_title.screen.blit(global_var.Edit_mode_currsor.image, global_var.Edit_mode_currsor.rect)
        
        if const.debug_mode:
            #draw player hitbox and on_ground and colision points
            if player.on_ground:
                pygame.draw.rect(scenes.main_title.screen, const.RED, player.rect, 1)
            else:
                pygame.draw.rect(scenes.main_title.screen, const.BLUE, player.rect, 1)
            pygame.draw.circle(
                surface = scenes.main_title.screen, 
                color = const.RED, 
                center = (player.rect.left + 1, player.rect.bottom - 2), 
                radius = 5, 
                width = 2
            )
            pygame.draw.circle(
                surface = scenes.main_title.screen, 
                color = const.RED, 
                center = (player.rect.centerx, player.rect.bottom - 2), 
                radius = 5, 
                width = 2
            )
            pygame.draw.circle(
                surface = scenes.main_title.screen, 
                color = const.RED,
                center = (player.rect.right - 1, player.rect.bottom - 2) , 
                radius = 5, 
                width = 2
            )
            #draw player velocity vector
            pygame.draw.line(
                scenes.main_title.screen, 
                const.GREEN, 
                (player.rect.centerx, player.rect.centery), 
                (player.rect.centerx + player.velocity_x * 10, player.rect.centery + player.velocity_y * 10), 
                2
            )
            #draw player calc position
            text = f"player_calc_position: (x: {player.calc_x} y: {player.calc_y})"
            text_surface = const.DEAFAULT_FONT.render(text, True, const.BLACK)
            text_rect = text_surface.get_rect(center = (100, 590))

            scenes.main_title.screen.blit(text_surface, text_rect)

            # draw collision boxes for all platforms
            for platform in platforms_group:
                pygame.draw.rect(
                    scenes.main_title.screen,
                    const.GREEN,
                    platform.rect,
                    1
                )
            #draw player rect position
            text = f"player_rect_position: (x: {player.rect.x} y: {player.rect.y})"
            text_surface = const.DEAFAULT_FONT.render(text, True, const.BLACK)
            text_rect = text_surface.get_rect(center = (100, 600))

            scenes.main_title.screen.blit(text_surface, text_rect)

            #draw camera move threshold lines
            left_limit = global_var.window_size[0] * const.CAMERA_MOVE_THRESHOLD
            right_limit = global_var.window_size[0] * (1 - const.CAMERA_MOVE_THRESHOLD)
            up_limit = global_var.window_size[1] * const.CAMERA_MOVE_THRESHOLD
            down_limit = global_var.window_size[1] * (1 - const.CAMERA_MOVE_THRESHOLD)
            pygame.draw.line(
                scenes.main_title.screen,
                const.GRAY,
                (left_limit, 0),
                (left_limit, global_var.window_size[1]),
                1
            )
            pygame.draw.line(
                scenes.main_title.screen,
                const.GRAY,
                (right_limit, 0),
                (right_limit, global_var.window_size[1]),
                1
            )
            pygame.draw.line(
                scenes.main_title.screen,
                const.GRAY,
                (0, up_limit),
                (global_var.window_size[0], up_limit),
                1
            )
            pygame.draw.line(
                scenes.main_title.screen,
                const.GRAY,
                (0, down_limit),
                (global_var.window_size[0], down_limit),
                1
            )

        pygame.display.update()
    
    if should_jump_to_main_title:
        tools.log("jumping to main title scene from real game scene", const.INFO)
        tools.clear_scene_transition_timers()
        tools.kill_buttons()
        scenes.main_title.start()
    else:
        pygame.quit()