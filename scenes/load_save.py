import os
import pygame
import tools
import const
import scenes.main_title
import scenes.real_game
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
    tools.log("LOAD_SAVE: load save scene start" , const.INFO)
    init()
    tools.log(f"LOAD_SAVE: available saves: {save_names}" , const.INFO)

    screen = scenes.main_title.screen
    if screen is None:
        screen = pygame.display.set_mode((800, 600))

    #groups
    mask_group = pygame.sprite.Group()  # Placeholder for any sprite groups you might want to use
    #init mask
    start_mask = scenes.main_title.mask.Mask((0, 0, 0))
    start_mask.fade(1)
    mask_group.add(start_mask)

    clock = pygame.time.Clock()

    #func var
    should_jump_to_real_game = False
    real_game_save_name = None  # Variable to hold the selected save name
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                tools.log("LOAD_SAVE: game quit" , const.INFO)
                #return

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

        mask_group.update()

        screen.fill(const.DARK_BLUE)
        draw_y = 50
        for save_name, save_path in save_names.items():
            font = pygame.font.Font(None, 36)
            text_surface = font.render(save_name, True, const.WHITE)
            text_rect = text_surface.get_rect(center=(150, draw_y))
            screen.blit(text_surface, text_rect)
            draw_y += 40
        mask_group.draw(screen)
        pygame.display.flip()
        clock.tick(const.FPS)
    
    if should_jump_to_real_game and real_game_save_name is not None:
        tools.log(f"LOAD_SAVE: jumping to real game scene with save name: {real_game_save_name}" , const.INFO)
        scenes.real_game.start(real_game_save_name)  # Pass the selected save name to the real game scene
    
