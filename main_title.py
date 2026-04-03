import pygame
import const
from pygame.locals import *
import tools
from sprites.buttons.Start import StartButton

def start():
    #window
    pygame.init()
    screen = pygame.display.set_mode(const.window_size , RESIZABLE)
    pygame.display.set_caption("parkure")

    #build buttons
    start_button = StartButton(100, 100)

    #connect signal to button instance
    const.SCREEN_RESIZE.connect(start_button.messege)

    #build groups
    buttons_group = pygame.sprite.Group()
    buttons_group.add(start_button)

    done = False
    #main loop
    while not done:
        #events
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                #resize window
                screen = pygame.display.set_mode((event.w , event.h) , RESIZABLE)
                tools.log(f"window resized to w:{event.w}h:{event.h}" , const.INFO)
                const.SCREEN_RESIZE.send(data=(const.SCREEN_RESIZE_CODE, (event.w, event.h)))

            if event.type == QUIT:
                tools.log("game quit" , const.INFO)
                done = True

        #draw
        screen.fill ((50 , 50 , 80))
        buttons_group.draw(screen)
        pygame.display.update()

pygame.quit()