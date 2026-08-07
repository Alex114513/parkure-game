import os
import pygame
import tools
import const
import global_var
import scenes.main_title
import scenes.real_game
from sprites.buttons import button
from scenes import main_title
from pygame.locals import *

pygame.init()

#save variable("save name": "save path")
save_names = {}

def init():
    files = os.listdir("saves")
    tools.log(f"LOAD_SAVE: found save files: {files}" , const.INFO)
    for file in files:
        save_names[file] = f"saves/{file}"

running = True

def start():
    global running, save_names

    #return button
    global_var.return_button = tools.create_return_button(tools.get_return_target(const.TARGET_LOAD_SAVE))

    #manage scene stack
    tools.push_scene(const.TARGET_LOAD_SAVE)
    tools.log(f"LOAD_SAVE: scene start, stack:{global_var.scene_stack}", const.DEBUG)

    tools.reset_exit_request()
    running = True
    pygame.init()

    tools.log("LOAD_SAVE: load save scene start" , const.INFO)
    init()
    tools.log(f"LOAD_SAVE: available saves: {save_names}" , const.INFO)

    screen = scenes.main_title.screen
    if screen is None:
        screen = pygame.display.set_mode((800, 600))

    #init mask
    start_mask = scenes.main_title.mask.Mask((0, 0, 0))
    start_mask.fade(1)
    main_title.masks_group.add(start_mask)

    clock = pygame.time.Clock()

    #func var
    should_jump_to_real_game = False
    real_game_save_name = None  # Variable to hold the selected save name
    should_jump_to_game_prep = False

    #sprite manage
    buttons_group = pygame.sprite.Group()
    buttons_group.add(global_var.return_button)
    
    while running:
        clock.tick(const.FPS)

        events = pygame.event.get()
        if any(event.type == pygame.QUIT for event in events):
            running = False
            tools.log("LOAD_SAVE: game quit" , const.INFO)
            tools.request_exit()
            continue

        for event in events:
            if event.type == VIDEORESIZE:
                #resize window
                screen = pygame.display.set_mode((event.w , event.h) , pygame.RESIZABLE)
                scenes.main_title.window_size = (event.w, event.h)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for save_name, save_path in save_names.items():
                    font = pygame.font.Font(None, 36)
                    text_surface = font.render(save_name, True, const.WHITE)
                    text_rect = text_surface.get_rect(center=(150, 50 + list(save_names.keys()).index(save_name) * 40))
                    if text_rect.collidepoint(mouse_pos):
                        tools.log(f"LOAD_SAVE: selected save: {save_name} at path: {save_path}" , const.INFO)
                        # Here you can add the logic to load the selected save
                        running = False
                        real_game_save_name = save_name  # Store the selected save name
                        should_jump_to_real_game = True
                        break
                if global_var.return_button.rect.collidepoint(event.pos):
                    tools.log(f"LOAD_SAVE: return button pressed, returning to{global_var.return_button.target_scene}", const.INFO)
                    tools.pop_scene()
                    global_var.return_button.clicked()
            
            if event.type == const.SWICH_TO_GAME_PREP_EVENT_CODE:
                tools.log("switch to game event received, switching to game scene" , const.INFO)
                running = False
                should_jump_to_game_prep = True

            if event.type == MOUSEMOTION:
                for button_ in buttons_group:
                    if button_.rect.collidepoint(event.pos):
                        tools.log(f"mouse is hovering on {button_.type} button", const.INFO)
                        if button_.target_size_mul != 0.8:
                            button_.target_size_mul = 1.2
                    else:
                        if button_.target_size_mul != 0.8:
                            button_.target_size_mul = 1

        main_title.masks_group.update()
        global_var.return_button_group.update()

        screen.fill(const.DARK_BLUE)
        draw_y = 50
        for save_name, save_path in save_names.items():
            font = pygame.font.Font(None, 36)
            text_surface = font.render(save_name, True, const.WHITE)
            text_rect = text_surface.get_rect(center=(150, draw_y))
            screen.blit(text_surface, text_rect)
            draw_y += 40
        global_var.return_button_group.draw(scenes.main_title.screen)
        main_title.masks_group.draw(screen)
        pygame.display.flip()
    
    if tools.exit_requested:
        tools.log("LOAD_SAVE: exit requested; skipping scene transition", const.INFO)
        pygame.quit()
    elif should_jump_to_real_game and real_game_save_name is not None:
        tools.log(f"LOAD_SAVE: jumping to real game scene with save name: {real_game_save_name}" , const.INFO)
        tools.prepare_for_new_scene()
        scenes.real_game.start(real_game_save_name)  # Pass the selected save name to the real game scene
    elif should_jump_to_game_prep:
        tools.log(f"switching to {global_var.scene_stack[global_var.scene_stack_top]} scene, current stack:{global_var.scene_stack}, stack_top:{global_var.scene_stack_top}" , const.INFO)
        tools.prepare_for_new_scene()
        scenes.game_prep.start()
    else:
        pygame.quit()