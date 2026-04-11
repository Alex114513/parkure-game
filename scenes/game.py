import pygame
import const
import tools
import scenes.main_title
import sprites.buttons.button as button
import sprites.work.masks.mask as mask

def start():
    tools.log("game scene start" , const.INFO)
    done = False

    #sprites
    sprites_group = pygame.sprite.Group()
    new_save_button = button.Button("new_save", None)
    sprites_group.add(new_save_button)
    load_save_button = button.Button("load_save", None)
    sprites_group.add(load_save_button)

    mask_group = pygame.sprite.Group()
    start_mask = mask.Mask(const.BLACK)
    mask_group.add(start_mask)

    #init mask
    start_mask.fade(3)

    while not done:
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tools.log("game quit" , const.INFO)
                done = True
        
        #draw
        scenes.main_title.screen.fill(const.DARK_BLUE)
        sprites_group.draw(scenes.main_title.screen)
        mask_group.draw(scenes.main_title.screen)
        pygame.display.update()

        #call sprites update
        mask_group.update()