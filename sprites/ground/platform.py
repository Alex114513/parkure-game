import pygame
import json

with open("configs/ground_objects_config.json", "r") as f:
    platform_config = json.load(f)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, degree=0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image = pygame.image.load("pict/ground/platform.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.degree = degree  # Rotation degree, if needed