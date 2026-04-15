import pygame
import const
import tools
import scenes.main_title
from sprites.work.masks import mask
from sprites.buttons import button
from pygame.locals import *

def start():
    tools.log("new save scene start" , const.INFO)
    done = False

    #start mask
    start_mask = mask.Mask(const.BLACK)
    scenes.main_title.masks_group.add(start_mask)

    #fade
    start_mask.fade(1)

    #buttons
    buttons_group = pygame.sprite.Group()
    create_button = button.Button("create", const.REAL_GAME)
    buttons_group.add(create_button)

    while not done:
        scenes.main_title.clock.tick(const.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tools.log("game quit" , const.INFO)
                done = True

            if event.type == const.SWITCH_TO_REAL_GAME_EVENT_CODE:
                tools.log("switching to real game scene" , const.INFO)
                done = True
                switch(const.REAL_GAME)

        #draw
        scenes.main_title.screen.fill(const.DARK_BLUE)
        scenes.main_title.masks_group.update()
        scenes.main_title.masks_group.draw(scenes.main_title.screen)
        pygame.display.update()