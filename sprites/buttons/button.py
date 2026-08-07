import pygame
import const
import tools
import json

#load button configuration from JSON file
with open("configs/buttons_config.json", "r") as f:
    button_config = json.load(f)

class Button(pygame.sprite.Sprite):
    def __init__(self, type, target_scene):
        """type is the type of button to create, it should be a key in the button_config dictionary loaded from the JSON file"""
        super().__init__()
        self.image = pygame.image.load(button_config[type]["path"]).convert_alpha()
        tools.log(f"button of type {type} created with image path {button_config[type]['path']}" , const.DEBUG)
        self.original_image = self.image
        self.original_x = button_config[type]["position"][0]
        self.original_y = button_config[type]["position"][1]
        self.rect = self.image.get_rect()
        self.rect.x = self.original_x
        self.rect.y = self.original_y
        self.target_scene = target_scene
        self.type = type

        #animation
        self.target_size_mul = 1
        self.real_size_mul = 1
    def messege(self , sender , **kwargs):
        data = kwargs.get('data')
        if data[0] == const.SCREEN_RESIZE_CODE:
            tools.log(f"{self.type} button received screen resize messege from {sender} with data:{data}" , const.DEBUG)
            #calculate the multiplier for the x and y axis
            x_multiplier = data[1][0] / const.window_size[0]
            y_multiplier = data[1][1] / const.window_size[1]
            #calculate the new width and height of the button
            multiplier = min(x_multiplier , y_multiplier)
            new_width = int(button_config[self.type]["size"][0] * multiplier)
            new_height = int(button_config[self.type]["size"][1] * multiplier)
            #apply the new width and height to the button image
            self.image = pygame.transform.scale(self.original_image , (new_width , new_height))
            #update self.target_size_mul
            self.target_size_mul = multiplier
            self.real_size_mul = multiplier
            #calculate the new x and y position of the button
            new_x = int(self.original_x * x_multiplier)
            new_y = int(self.original_y * y_multiplier)
            #apply the new x and y position to the button rect and update its size
            self.rect = self.image.get_rect(x=new_x, y=new_y)
    def clicked(self):
        from scenes import main_title
        from sprites.work.masks.mask import Mask

        self.target_size_mul = 0.8
        mask = Mask(const.BLACK)
        mask.fade_in(1)
        main_title.masks_group.add(mask)
        if self.target_scene == const.TARGET_GAME:
            tools.log(f"{self.type} button clicked,scene will switch in about 1 seconds" , const.DEBUG)
            pygame.time.set_timer(const.SWITCH_TO_GAME_EVENT_CODE, 900)

        if self.target_scene == const.TARGET_NEW_SAVE:
            tools.log(f"{self.type} button clicked,scene will switch in about 1 seconds" , const.DEBUG)
            pygame.time.set_timer(const.SWITCH_TO_NEW_SAVE_EVENT_CODE, 900)

        if self.target_scene == const.TARGET_LOAD_SAVE:
            tools.log(f"{self.type} button clicked,scene will switch in about 1 seconds" , const.DEBUG)
            pygame.time.set_timer(const.SWITCH_TO_LOAD_SAVE_EVENT_CODE, 900)

        if self.target_scene == const.REAL_GAME:
            tools.log(f"{self.type} button clicked,scene will switch in about 1 seconds" , const.DEBUG)
            pygame.time.set_timer(const.SWITCH_TO_REAL_GAME_EVENT_CODE, 900)
        
        if self.target_scene == const.TARGET_MAIN_TITLE:
            tools.log(f"{self.type} button clicked,scene will switch in about 1 seconds" , const.DEBUG)
            pygame.time.set_timer(const.SWITCH_TO_MAIN_TITLE_EVENT_CODE, 900)
        
        if self.target_scene == const.TARGET_GAME_PREP:
            tools.log(f"{self.type} button clicked,scene will switch in about 1 seconds" , const.DEBUG)
            pygame.time.set_timer(const.SWICH_TO_GAME_PREP_EVENT_CODE, 900)
    def update(self):
        #change button size by  target_size  .
        self.real_size_mul += (self.target_size_mul - self.real_size_mul) * const.change_speed
        if abs(self.target_size_mul - self.real_size_mul) <= const.clap_abs:
            self.real_size_mul = self.target_size_mul

        self.image = pygame.transform.scale(
            self.original_image, 
            (button_config[self.type]["size"][0] * self.real_size_mul,
            button_config[self.type]["size"][1] * self.real_size_mul)
        )
        self.rect = self.image.get_rect(center = self.rect.center)