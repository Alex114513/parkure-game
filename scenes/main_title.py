import pygame
import const
from pygame.locals import *
import tools
from sprites.buttons.Start import StartButton
import json
import scenes.game

# Load button configuration from JSON file
with open("pict/buttons/Start.json", "r") as f:
    button_config = json.load(f)

masks_group = pygame.sprite.Group()

window_size = const.window_size

done = False

#window
pygame.init()
screen = pygame.display.set_mode(const.window_size , RESIZABLE)
pygame.display.set_caption("parkure")

def start():
    global window_size , done , screen
    
    #build buttons
    start_button = StartButton(
        button_config["Start"]["position"][0],
        button_config["Start"]["position"][1]
    )

    #connect signal to button
    const.SCREEN_RESIZE.connect(start_button.messege)

    #build groups
    buttons_group = pygame.sprite.Group()
    
    buttons_group.add(start_button)

    #main loop
    while not done:
        #events
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                #resize window
                screen = pygame.display.set_mode((event.w , event.h) , RESIZABLE)
                tools.log(f"window resized to w:{event.w}h:{event.h}" , const.INFO)
                const.SCREEN_RESIZE.send(data=(const.SCREEN_RESIZE_CODE, (event.w, event.h)))
                window_size = (event.w, event.h)

            if event.type == QUIT:
                tools.log("game quit" , const.INFO)
                done = True
            
            if event.type == MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    tools.log("start button clicked.start game" , const.INFO)
                    start_button.clicked()

        #draw
        masks_group.update()
        screen.fill ((50 , 50 , 80))
        buttons_group.draw(screen)
        masks_group.draw(screen)
        pygame.display.update()
    
    tools.log("main title loop ended" , const.DEBUG)

    pygame.quit()

def swich():
    global done
    done = True
    scenes.game.start()