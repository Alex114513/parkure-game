import pygame
import const
import tools
import scenes.main_title

def start():
    tools.log("game scene start" , const.INFO)
    done = False
    while not done:
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tools.log("game quit" , const.INFO)
                done = True
        
        #draw
        scenes.main_title.screen.fill(const.RED)
        pygame.display.update()