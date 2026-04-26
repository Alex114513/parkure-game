import pygame
import const
import tools
import scenes.main_title
from sprites.work.masks import mask
from sprites.buttons import button
from scenes import real_game
from pygame.locals import *

buttons_group = pygame.sprite.Group()

def start():
    tools.log("new save scene start" , const.INFO)
    done = False

    #start mask
    start_mask = mask.Mask(const.BLACK)
    scenes.main_title.masks_group.add(start_mask)

    #fade
    start_mask.fade(1)

    #buttons
    create_button = button.Button("create", const.REAL_GAME)
    buttons_group.add(create_button)

    #message connection
    const.SCREEN_RESIZE.connect(create_button.messege)

    while not done:
        scenes.main_title.clock.tick(const.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tools.log("game quit" , const.INFO)
                done = True

            if event.type == const.SWITCH_TO_REAL_GAME_EVENT_CODE:
                tools.log("switching to real game scene" , const.INFO)
                tools.new_save("player1")  # Replace "player1" with the actual player name
                done = True
                switch(const.REAL_GAME)
            
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

        #draw
        scenes.main_title.screen.fill(const.DARK_BLUE)
        buttons_group.update()
        buttons_group.draw(scenes.main_title.screen)
        scenes.main_title.masks_group.update()
        scenes.main_title.masks_group.draw(scenes.main_title.screen)
        pygame.display.update()

def switch(scene):
    global done, buttons_group, masks_group
    done = True

    buttons_group.empty()
    scenes.main_title.masks_group.empty()
    if scene == const.REAL_GAME:
        real_game.start("player1")  # Replace "player1" with the actual player name