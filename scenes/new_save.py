import pygame
import const
import tools
import global_var
import scenes.main_title
from sprites.work.masks import mask
from sprites.buttons import button
from sprites.buttons.input_tab import InputTab
from scenes import real_game
from scenes import game_prep
from pygame.locals import *

buttons_group = pygame.sprite.Group()
ui_group = None
done = False

def start():
    global done, buttons_group

    #return button
    global_var.return_button = tools.create_return_button(tools.get_return_target(const.TARGET_NEW_SAVE))

    #manage scene stack
    tools.push_scene(const.TARGET_NEW_SAVE)
    tools.log(f"NEW_SAVE: scene start, stack:{global_var.scene_stack}", const.DEBUG)

    tools.reset_exit_request()
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
    buttons_group.add(global_var.return_button, create_button)

    #message connection
    const.SCREEN_RESIZE.connect(create_button.messege)
    const.SCREEN_RESIZE.connect(input_tab.messege)

    #func var
    should_jump_to_real_game = False
    should_jump_to_game_prep = False

    while not done:
        scenes.main_title.clock.tick(const.FPS)
        events = pygame.event.get()
        if any(event.type == pygame.QUIT for event in events):
            tools.log("game quit" , const.INFO)
            tools.request_exit()
            done = True
            continue

        for event in events:
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
                if global_var.return_button.rect.collidepoint(event.pos):
                    tools.log(f"NEW_SAVE: return button pressed, returning to {global_var.return_button.target_scene}", const.INFO)
                    tools.pop_scene()
                    global_var.return_button.clicked()

            if event.type == const.SWICH_TO_GAME_PREP_EVENT_CODE:
                should_jump_to_game_prep = True
                done = True

            if event.type == MOUSEMOTION:
                for button_ in buttons_group:
                    if button_.rect.collidepoint(event.pos):
                        #tools.log(f"mouse is hovering on {button_.type} button", const.INFO)
                        if button_.target_size_mul != 0.8:
                            button_.target_size_mul = 1.2
                    else:
                        if button_.target_size_mul != 0.8:
                            button_.target_size_mul = 1
            
            input_tab.handle_event(event)

        #draw
        scenes.main_title.screen.fill(const.DARK_BLUE)
        ui_group.update()
        global_var.return_button_group.update()
        ui_group.draw(scenes.main_title.screen)
        scenes.main_title.masks_group.update()
        global_var.return_button_group.draw(scenes.main_title.screen)
        scenes.main_title.masks_group.draw(scenes.main_title.screen)

        #get the text surface and rect from the input tab
        text_surface, text_rect = input_tab._render_text()
        #blit the text surface onto the screen
        scenes.main_title.screen.blit(text_surface, text_rect)

        pygame.display.update()

    if tools.exit_requested:
        tools.log("NEW_SAVE: exit requested; skipping scene transition", const.INFO)
        pygame.quit()
    elif should_jump_to_real_game:
        tools.log("jumping to real game scene from new save scene" , const.INFO)
        switch(const.REAL_GAME, save_name)  # Pass the save name to the switch function
    elif should_jump_to_game_prep:
        tools.log("jumping to game prep scene from new_save scene", const.INFO)
        switch(const.TARGET_GAME_PREP)
    else:
        pygame.quit()


def switch(scene, save_name = None):
    global done, buttons_group, masks_group
    done = True
    tools.prepare_for_new_scene()

    buttons_group.empty()
    scenes.main_title.masks_group.empty()
    if scene == const.REAL_GAME:
        real_game.start(save_name)  # Use the provided save name
    if scene == const.TARGET_GAME_PREP:
        tools.log(f"switching to {global_var.scene_stack[global_var.scene_stack_top]} scene, current stack:{global_var.scene_stack}, stack_top:{global_var.scene_stack_top}" , const.INFO)
        tools.prepare_for_new_scene()
        scenes.game_prep.start()