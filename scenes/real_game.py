import pygame
import const
import tools
import scenes.main_title

def start():
    tools.log("real game scene start" , const.INFO)
    done = False

    while not done:
        scenes.main_title.clock.tick(const.FPS)

        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tools.log("game quit" , const.INFO)
                done = True

        #draw
        scenes.main_title.screen.fill(const.DARK_BLUE)
        pygame.display.update()