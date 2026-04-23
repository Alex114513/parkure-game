import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("pict/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #TODO: add more player attributes like health, speed, etc.
        self.score = 0
        self.level = 1
        self.name = None
        self.accseleration = [0, 0]
        self.max_speed = [5, 10]

        #These are placeholder values, will be updated in init() based on save data
        self.health = 100
        self.speed = 5

        #physics attributes
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
    
    def update(self):
        #TODO: add player movement and physics here
        pass