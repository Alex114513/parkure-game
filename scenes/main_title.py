import pygame
import const
import global_var
from pygame.locals import *
import tools
from sprites.buttons.button import Button
import scenes.game_prep
import sprites.work.masks.mask as mask

masks_group = pygame.sprite.Group()

window_size = const.window_size

buttons_group = pygame.sprite.Group()

done = False

#func var
should_jump_scene = None

#window
pygame.init()
screen = pygame.display.set_mode(const.window_size , RESIZABLE)
pygame.display.set_caption("parkure")

#clock
clock = pygame.time.Clock()

def start():
    global window_size , done , screen, should_jump_scene
    
    tools.reset_exit_request()
    tools.clear_scene_transition_timers()
    should_jump_scene = None
    done = False
    pygame.init()

    #build buttons
    start_button = Button("Start", const.TARGET_GAME)

    #connect signal to button
    const.SCREEN_RESIZE.connect(start_button.messege)

    buttons_group.add(start_button)

    #main loop
    while not done:

        clock.tick(const.FPS)

        #events
        events = pygame.event.get()
        if any(event.type == QUIT for event in events):
            tools.log("game quit" , const.INFO)
            tools.request_exit()
            done = True
            continue

        for event in events:
            if event.type == VIDEORESIZE:
                #resize window
                screen = pygame.display.set_mode((event.w , event.h) , RESIZABLE)
                tools.log(f"window resized to w:{event.w}h:{event.h}" , const.INFO)
                const.SCREEN_RESIZE.send(data=(const.SCREEN_RESIZE_CODE, (event.w, event.h)))
                window_size = (event.w, event.h)
            
            if event.type == MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    tools.log("start button clicked.start game" , const.INFO)
                    start_button.clicked()
            
            if event.type == const.SWITCH_TO_GAME_EVENT_CODE:
                tools.log("switch to game event received, switching to game scene" , const.INFO)
                swich()

        #draw
        masks_group.update()
        screen.fill (const.DARK_BLUE)
        buttons_group.draw(screen)
        masks_group.draw(screen)
        pygame.display.update()
    
    tools.log("main title loop ended" , const.DEBUG)

    if tools.exit_requested:
        tools.log("MAIN_TITLE: exit requested; skipping scene transition", const.INFO)
        pygame.quit()
    elif should_jump_scene == "game_prep":
        tools.log("jumping to game prep scene" , const.INFO)
        scenes.game_prep.start()

    pygame.quit()

def swich():
    global done, buttons_group, masks_group, should_jump_scene
    tools.log("switching to game prep scene" , const.INFO)
    tools.prepare_for_new_scene()
    global_var.return_button = Button("return", const.TARGET_MAIN_TITLE)
    global_var.return_button_group = pygame.sprite.Group()
    global_var.return_button_group.add(global_var.return_button)
    done = True
    should_jump_scene = "game_prep"
    