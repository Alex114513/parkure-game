import pygame
import const
from pygame.locals import *
import tools

def start():
    #window
    pygame.init()
    screen = pygame.display.set_mode(const.window_size , RESIZABLE)
    pygame.display.set_caption("parkure")

    done = False
    #main loop
    while not done:
        #events
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                #resize window
                screen = pygame.display.set_mode((event.w , event.h) , RESIZABLE)
                tools.log(f"window resized to w:{event.w}h:{event.h}" , "info")

            if event.type == QUIT:
                done = True

        #draw
        screen.fill ((50 , 50 , 80))
        pygame.display.update()

pygame.quit()