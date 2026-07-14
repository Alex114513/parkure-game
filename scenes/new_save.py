import pygame
import const
import tools
import scenes.main_title
from sprites.work.masks import mask
from sprites.buttons import button
from sprites.buttons.input_tab import InputTab
from scenes import real_game
from pygame.locals import *

buttons_group = pygame.sprite.Group()
ui_group = None
done = False

def start():
    global done, buttons_group
    done = False
    tools.log("new save scene start" , const.INFO)

    #start mask
    start_mask = mask.Mask(const.BLACK)
    scenes.main_title.masks_group.add(start_mask)

    #fade
    start_mask.fade(1)

    #saving
    save_name = None  # Initialize save_name to None

    #buttons
    create_button = button.Button("create", const.REAL_GAME)
    input_tab = InputTab("", const.DEAFAULT_FONT, const.WHITE)
    ui_group = pygame.sprite.Group(create_button, input_tab)

    #message connection
    const.SCREEN_RESIZE.connect(create_button.messege)
    const.SCREEN_RESIZE.connect(input_tab.messege)

    #func var
    should_jump_to_real_game = False

    while not done:
        scenes.main_title.clock.tick(const.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tools.log("game quit" , const.INFO)
                done = True

            if event.type == const.SWITCH_TO_REAL_GAME_EVENT_CODE:
                save_name = input_tab.text
                tools.log(f"switching to real game scene with save name: {save_name}" , const.INFO)
                tools.new_save(save_name)  # Use the entered save name
                done = True
                should_jump_to_real_game = True
            
            if event.type == VIDEORESIZE:
                #resize window
                scenes.main_title.screen = pygame.display.set_mode((event.w , event.h) , RESIZABLE)
                tools.log(f"window resized to w:{event.w}h:{event.h}" , const.INFO)
                const.SCREEN_RESIZE.send(data=(const.SCREEN_RESIZE_CODE, (event.w, event.h)))
                scenes.main_title.window_size = (event.w, event.h)

            if event.type == MOUSEBUTTONDOWN:
                if create_button.rect.collidepoint(event.pos):
                    tools.log("create button clicked.start real game scene" , const.INFO)
                    create_button.clicked()
            
            input_tab.handle_event(event)

        #draw
        scenes.main_title.screen.fill(const.DARK_BLUE)
        ui_group.update()
        ui_group.draw(scenes.main_title.screen)
        scenes.main_title.masks_group.update()
        scenes.main_title.masks_group.draw(scenes.main_title.screen)

        #get the text surface and rect from the input tab
        text_surface, text_rect = input_tab._render_text()
        #blit the text surface onto the screen
        scenes.main_title.screen.blit(text_surface, text_rect)

        pygame.display.update()

    if should_jump_to_real_game:
        tools.log("jumping to real game scene from new save scene" , const.INFO)
        switch(const.REAL_GAME, save_name)  # Pass the save name to the switch function


def switch(scene, save_name):
    global done, buttons_group, masks_group
    done = True

    buttons_group.empty()
    scenes.main_title.masks_group.empty()
    if scene == const.REAL_GAME:
        real_game.start(save_name)  # Use the provided save name
