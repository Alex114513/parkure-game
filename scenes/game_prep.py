import pygame
import const
import tools
import scenes.main_title
import sprites.buttons.button as button
import sprites.work.masks.mask as mask
from pygame.locals import *

def start():
    tools.log("game scene start" , const.INFO)
    done = False

    #sprites
    sprites_group = pygame.sprite.Group()
    new_save_button = button.Button("new_save", const.TARGET_NEW_SAVE)
    sprites_group.add(new_save_button)
    load_save_button = button.Button("load_save", const.TARGET_LOAD_SAVE)
    sprites_group.add(load_save_button)

    const.SCREEN_RESIZE.connect(load_save_button.messege)
    const.SCREEN_RESIZE.connect(new_save_button.messege)

    start_mask = mask.Mask(const.BLACK)
    scenes.main_title.masks_group.add(start_mask)

    #init mask
    start_mask.fade(1)

    while not done:

        scenes.main_title.clock.tick(const.FPS)

        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tools.log("game quit" , const.INFO)
                done = True

            if event.type == const.SWITCH_TO_NEW_SAVE_EVENT_CODE:
                tools.log("switching to new save scene" , const.INFO)
                done = True
                swich(const.TARGET_NEW_SAVE)

            if event.type == const.SWITCH_TO_LOAD_SAVE_EVENT_CODE:
                tools.log("switching to load save scene" , const.INFO)
                done = True
                swich(const.TARGET_LOAD_SAVE)

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

        #draw
        scenes.main_title.screen.fill(const.DARK_BLUE)
        sprites_group.draw(scenes.main_title.screen)
        scenes.main_title.masks_group.draw(scenes.main_title.screen)
        pygame.display.update()

        #call sprites update
        scenes.main_title.masks_group.update()

def swich(to):
    tools.log(f"switching to {to}" , const.INFO)
    if to == const.TARGET_NEW_SAVE:
        import scenes.new_save as new_save
        new_save.start()
    #if to == const.TARGET_LOAD_SAVE:
    #    import scenes.load_save as load_save
    #    load_save.start()