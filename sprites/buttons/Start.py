import pygame
import const
import tools
import json

#load button configuration from JSON file
with open("pict/buttons/Start.json", "r") as f:
    button_config = json.load(f)

class StartButton(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(button_config["Start"]["path"]).convert_alpha()
        self.original_image = self.image
        self.original_x = x
        self.original_y = y
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
            new_width = int(button_config["Start"]["size"][0] * x_multiplier)
            new_height = int(button_config["Start"]["size"][1] * y_multiplier)
            #apply the new width and height to the button image
            self.image = pygame.transform.scale(self.original_image , (new_width , new_height))
            #calculate the new x and y position of the button
            new_x = int(self.original_x * x_multiplier)
            new_y = int(self.original_y * y_multiplier)
            #apply the new x and y position to the button rect
            self.rect.x = new_x
            self.rect.y = new_y
    def clicked(self):
        self.image = pygame.transform.scale(self.original_image , (int(button_config["Start"]["size"][0] * 1.2) , int(button_config["Start"]["size"][1] * 1.2)))
        self.rect = self.image.get_rect(center=self.rect.center)