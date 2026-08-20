import pygame
import const
import tools
import global_var
import scenes.main_title
import sprites.buttons.button as button
import sprites.work.masks.mask as mask
from pygame.locals import *

buttons_group = pygame.sprite.Group()

#func var
should_jump_scene = None

def start():
    global should_jump_scene

    #return button
    global_var.return_button = tools.create_return_button(tools.get_return_target(const.TARGET_GAME_PREP))

    #manage scene stack
    tools.push_scene(const.TARGET_GAME_PREP)
    tools.log(f"GAME_PREP: scene start, stack:{global_var.scene_stack}", const.DEBUG)

    tools.reset_exit_request()
    tools.log("game scene start" , const.INFO)
    done = False

    #sprites
    new_save_button = button.Button("new_save", const.TARGET_NEW_SAVE)
    buttons_group.add(new_save_button)
    load_save_button = button.Button("load_save", const.TARGET_LOAD_SAVE)
    buttons_group.add(load_save_button)
    buttons_group.add(global_var.return_button)

    const.SCREEN_RESIZE.connect(load_save_button.messege)
    const.SCREEN_RESIZE.connect(new_save_button.messege)

    start_mask = mask.Mask(const.BLACK)
    scenes.main_title.masks_group.add(start_mask)

    #init mask
    start_mask.fade(1)

    while not done:
        scenes.main_title.clock.tick(const.FPS)

        #events
        events = pygame.event.get()
        if any(event.type == pygame.QUIT for event in events):
            tools.log("game quit" , const.INFO)
            tools.request_exit()
            done = True
            continue

        for event in events:
            if event.type == const.SWITCH_TO_NEW_SAVE_EVENT_CODE:
                tools.log("switching to new save scene" , const.INFO)
                done = True
                should_jump_scene = "new_save"

            if event.type == const.SWITCH_TO_LOAD_SAVE_EVENT_CODE:
                tools.log("switching to load save scene" , const.INFO)
                done = True
                should_jump_scene = "load_save"
            
            if event.type == const.SWITCH_TO_MAIN_TITLE_EVENT_CODE:
                tools.log("GAME_PREP: swiching to main_title", const.INFO)
                done = True
                should_jump_scene = const.TARGET_MAIN_TITLE

            if event.type == VIDEORESIZE:
                #resize window
                scenes.main_title.screen = pygame.display.set_mode((event.w , event.h) , RESIZABLE)
                tools.log(f"window resized to w:{event.w}h:{event.h}" , const.INFO)
                const.SCREEN_RESIZE.send(data=(const.SCREEN_RESIZE_CODE, (event.w, event.h)))
                scenes.main_title.window_size = (event.w, event.h)

            if event.type == MOUSEBUTTONDOWN:
                if new_save_button.rect.collidepoint(event.pos):
                    tools.log("new save button clicked.start new save scene" , const.INFO)
                    new_save_button.clicked()
                if load_save_button.rect.collidepoint(event.pos):
                    tools.log("load save button clicked.start load save scene" , const.INFO)
                    load_save_button.clicked()
                if global_var.return_button.rect.collidepoint(event.pos):
                    tools.log(f"GAME_PREP: return button pressed, returning to{global_var.return_button.target_scene}", const.INFO)
                    tools.pop_scene()
                    global_var.return_button.clicked()

            if event.type == MOUSEMOTION:
                for button_ in buttons_group:
                    if button_.rect.collidepoint(event.pos):
                        tools.log(f"mouse is hovering on {button_.type} button", const.INFO)
                        if button_.target_size_mul != 0.8:
                            button_.target_size_mul = 1.2
                    else:
                        if button_.target_size_mul != 0.8:
                            button_.target_size_mul = 1

        #draw
        scenes.main_title.screen.fill(const.DARK_BLUE)
        buttons_group.draw(scenes.main_title.screen)
        global_var.return_button_group.draw(scenes.main_title.screen)
        scenes.main_title.masks_group.draw(scenes.main_title.screen)
        pygame.display.update()

        #call sprites update
        scenes.main_title.masks_group.update()
        global_var.return_button_group.update()
        buttons_group.update()
    
    if tools.exit_requested:
        tools.log("GAME_PREP: exit requested; skipping scene transition", const.INFO)
        pygame.quit()
    elif should_jump_scene == "new_save":
        switch("new_save")
    elif should_jump_scene == "load_save":
        switch("load_save")
    elif should_jump_scene == const.TARGET_MAIN_TITLE:
        switch(const.TARGET_MAIN_TITLE)
    else:
        pygame.quit()

def switch(to):
    global done, buttons_group, masks_group
    done = True
    tools.log(f"switching to {to}" , const.INFO)
    tools.prepare_for_new_scene()
    buttons_group.empty()
    scenes.main_title.masks_group.empty()
    if to == const.TARGET_NEW_SAVE:
        import scenes.new_save as new_save
        tools.log(f"switching to {global_var.scene_stack[global_var.scene_stack_top]} scene, current stack:{global_var.scene_stack}, stack_top:{global_var.scene_stack_top}" , const.INFO)
        new_save.start()
    if to == const.TARGET_LOAD_SAVE:
        import scenes.load_save as load_save
        tools.log(f"switching to {global_var.scene_stack[global_var.scene_stack_top]} scene, current stack:{global_var.scene_stack}, stack_top:{global_var.scene_stack_top}" , const.INFO)
        load_save.start()
    if to == const.TARGET_MAIN_TITLE:
        import scenes.main_title as main_title
        tools.log("GAME_PREP: swithcing to main_title", const.INFO)
        main_title.start()
