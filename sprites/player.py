import pygame
from scenes import  real_game

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
        self.accseleration = [0, 0]
        self.max_speed = [5, 10]
        self.friction = 0.1
        self.gravity = 0.5
        self.jump_strength = 10
    
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
        self.try_move(self.velocity_x, self.velocity_y)
    
    def try_move(self, dx, dy):
        self.rect.x += dx
        if self.collide():
            self.rect.x -= dx
        self.rect.y += dy
        if self.collide():
            self.rect.y -= dy
    
    def collide(self):
        for platform in real_game.platforms_group:
            if self.rect.colliderect(platform.rect):
                self.on_ground = True
                return True
        self.on_ground = False
        return False