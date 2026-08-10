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
        self.raw_image = pygame.image.load("pict/ground/platform.png").convert_alpha()
        self.base_image = pygame.transform.scale(self.raw_image, (width, height))
        self.world_x = x
        self.world_y = y
        self.width = width
        self.height = height
        self.degree = degree  # Rotation degree, if needed
        self._update_image()
        self.rect.topleft = (x, y)
    
    def _update_image(self):
        self.image = pygame.transform.rotate(self.base_image, self.degree)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.world_x - global_var.camera_x, self.world_y - global_var.camera_y))
    
    def update(self):
        # adjust platform position based on camera offset, not cumulative movement
        self.rect.topleft = (self.world_x - global_var.camera_x, self.world_y - global_var.camera_y)