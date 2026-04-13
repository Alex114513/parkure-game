import pygame
import const
import tools
import json
from sprites.work.masks.mask import Mask
from scenes import game_prep

#load button configuration from JSON file
with open("pict/buttons/buttons_config.json", "r") as f:
    button_config = json.load(f)

class Button(pygame.sprite.Sprite):
    def __init__(self, type, target_scene):
        """type is the type of button to create, it should be a key in the button_config dictionary loaded from the JSON file"""
        super().__init__()
        self.image = pygame.image.load(button_config[type]["path"]).convert_alpha()
        self.original_image = self.image
        self.original_x = button_config[type]["position"][0]
        self.original_y = button_config[type]["position"][1]
        self.rect = self.image.get_rect()
        self.rect.x = self.original_x
        self.rect.y = self.original_y
        self.target_scene = target_scene
        self.type = type
    def messege(self , sender , **kwargs):
        data = kwargs.get('data')
        if data[0] == const.SCREEN_RESIZE_CODE:
            tools.log(f"start button received screen resize messege from {sender} with data:{data}" , const.DEBUG)
            #calculate the multiplier for the x and y axis
            x_multiplier = data[1][0] / const.window_size[0]
            y_multiplier = data[1][1] / const.window_size[1]
            #calculate the new width and height of the button
            multiplier = min(x_multiplier , y_multiplier)
            new_width = int(button_config[self.type]["size"][0] * multiplier)
            new_height = int(button_config[self.type]["size"][1] * multiplier)
            #apply the new width and height to the button image
            self.image = pygame.transform.scale(self.original_image , (new_width , new_height))
            #calculate the new x and y position of the button
            new_x = int(self.original_x * x_multiplier)
            new_y = int(self.original_y * y_multiplier)
            #apply the new x and y position to the button rect
            self.rect.x = new_x
            self.rect.y = new_y
    def clicked(self):
        self.image = pygame.transform.scale(self.original_image , (int(button_config[self.type]["size"][0] * 1.2) , int(button_config[self.type]["size"][1] * 1.2)))
        self.rect = self.image.get_rect(center=self.rect.center)
        Mask(const.BLACK).fade_in(3)
        if self.target_scene == const.TARGET_GAME:
            tools.log("start button clicked,scene will switch in about 3 seconds" , const.DEBUG)
            pygame.time.set_timer(const.SWITCH_TO_GAME_EVENT_CODE, 2900)

        if self.target_scene == const.TARGET_NEW_SAVE:
            tools.log("new save button clicked,scene will switch in about 3 seconds" , const.DEBUG)
            pygame.time.set_timer(const.SWITCH_TO_NEW_SAVE_EVENT_CODE, 2900)

        if self.target_scene == const.TARGET_LOAD_SAVE:
            tools.log("load save button clicked,scene will switch in about 3 seconds" , const.DEBUG)
            pygame.time.set_timer(const.SWITCH_TO_LOAD_SAVE_EVENT_CODE, 2900)