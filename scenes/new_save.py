import pygame
import const
import tools
import scenes.main_title

def start():
    tools.log("new save scene start" , const.INFO)
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tools.log("game quit" , const.INFO)
                done = True

        #draw
        scenes.main_title.screen.fill(const.DARK_BLUE)
        pygame.display.update()