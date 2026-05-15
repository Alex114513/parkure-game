import pygame
import tools
import global_var
from scenes import  real_game
import const

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

        #debugging
        self.edit_mode = False
    
    def update(self):
        #TODO: add player movement and physics here
        
        if self.edit_mode:
            self.velocity_x = 0
            self.velocity_y = 0
            
            self.edit_stuff()
        else:
            self.normal_phisics_update()

        #update player position based on velocity
        self.try_move(self.velocity_x, self.velocity_y)

        #camera stuff
        if self.rect.x > (const.window_size[0] * (1 - const.CAMERA_MOVE_THRESHOLD)):
            global_var.camera_x += min((self.rect.x - (const.window_size[0] - const.CAMERA_MOVE_THRESHOLD)) * const.CAMERA_MOVE_STEP, const.CAMERA_SCROLL_SPEED)
        elif self.rect.x < (const.window_size[0] * const.CAMERA_MOVE_THRESHOLD):
            global_var.camera_x -= min((const.CAMERA_MOVE_THRESHOLD - self.rect.x) * const.CAMERA_MOVE_STEP, const.CAMERA_SCROLL_SPEED)
        
        #limmit camera movement based on player position
        if self.rect.x - global_var.camera_x < (const.window_size[0] * const.CAMERA_MOVE_THRESHOLD):
            global_var.camera_x = self.rect.x - (const.window_size[0] * const.CAMERA_MOVE_THRESHOLD)
        elif self.rect.x - global_var.camera_x > (const.window_size[0] * (1 - const.CAMERA_MOVE_THRESHOLD)):
            global_var.camera_x = self.rect.x - (const.window_size[0] * (1 - const.CAMERA_MOVE_THRESHOLD))
        
        #least limmit for camera
        if global_var.camera_x < const.LEAST_CAMERA_X:
            global_var.camera_x = const.LEAST_CAMERA_X
        
        #adjust player position based on camera
        self.rect.x -= global_var.camera_x * const.CAMERA_MOVE_STEP
    
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
        if self.rect.x < 0:
            return True
        return False
    
    def normal_phisics_update(self):
        #velocity
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = max(self.velocity_x - self.accseleration[0], -self.max_speed[0])
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = min(self.velocity_x + self.accseleration[0], self.max_speed[0])

        #friction
        if self.on_ground:
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
        if not self.on_ground:
            self.velocity_y += self.gravity
            if self.velocity_y > self.max_speed[1]:
                self.velocity_y = self.max_speed[1]
        
    def edit_stuff(self):
        #velocity
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = max(self.velocity_x - self.accseleration[0], -self.max_speed[0])
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = min(self.velocity_x + self.accseleration[0], self.max_speed[0])
        
        #up and down for edit mode
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = max(self.velocity_y - self.accseleration[1], -self.max_speed[1])
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = min(self.velocity_y + self.accseleration[1], self.max_speed[1])
        
        self.velocity_x = max(min(self.velocity_x, self.max_speed[0]), -self.max_speed[0])
        self.velocity_y = max(min(self.velocity_y, self.max_speed[1]), -self.max_speed[1])