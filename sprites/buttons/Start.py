import pygame
import const
import tools

class StartButton(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("pict\\buttons\\Start.png").convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def messege(self , sender , **kwargs):
        data = kwargs.get('data')
        if data[0] == const.SCREEN_RESIZE_CODE:
            tools.log(f"start button received screen resize messege with data:{data}" , const.INFO)
            #calculate the multiplier for the x and y axis
            x_multiplier = data[1][0] / const.window_size[0]
            y_multiplier = data[1][1] / const.window_size[1]
            #calculate the new width and height of the button
            new_width = int(64 * x_multiplier)
            new_height = int(32 * y_multiplier)
            #apply the new width and height to the button image
            self.image = pygame.transform.scale(self.original_image , (new_width , new_height))