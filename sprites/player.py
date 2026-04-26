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

        #These are placeholder values, will be updated in init() based on save data
        self.health = 100
        self.speed = 5

        #physics attributes
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.on_ground = True #for now, on_ground is always true, will be updated in the future when we add platforms and jumping
        self.accseleration = [0, 0]
        self.max_speed = [5, 10]
        self.friction = 0.1
        self.gravity = 0.5
    
    def update(self):
        #TODO: add player movement and physics here

        #frichtion
        if self.on_ground:#for now, on_ground is always true, will be updated in the future when we add platforms and jumping
            if self.velocity_x > 0:
                self.velocity_x *= self.friction
            elif self.velocity_x < 0:
                self.velocity_x *= self.friction
        
        if abs(self.velocity_x) < 0.1:
            self.velocity_x = 0

        if self.velocity_x > 0:
            self.velocity_x = min(self.velocity_x, self.max_speed[0])
        elif self.velocity_x < 0:
            self.velocity_x = max(self.velocity_x, -self.max_speed[0])
        self.velocity_y = min(self.velocity_y, self.max_speed[1])
        
        #gravity
        if not self.on_ground:#for now, on_ground is always true, will be updated in the future when we add platforms and jumping
            self.velocity_y += self.gravity
            if self.velocity_y > self.max_speed[1]:
                self.velocity_y = self.max_speed[1]
        
        #update player position based on velocity
        self.rect.x += self.velocity_x