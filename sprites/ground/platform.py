import pygame
import json
import global_var
import tools
import const

with open("configs/ground_objects_config.json", "r") as f:
    platform_config = json.load(f)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, degree=0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image = pygame.image.load("pict/ground/platform.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.world_x = x
        self.world_y = y
        self.rect.topleft = (x, y)
        self.degree = degree  # Rotation degree, if needed
    
    def update(self):
        #adjust platform position based on camera offset, not cumulative movement
        self.rect.x = self.world_x - global_var.camera_x * const.CAMERA_MOVE_STEP
        self.rect.y = self.world_y