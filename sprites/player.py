import pygame
import tools
import global_var
from sprites import edit_mode_currsor
from scenes import  real_game
import const

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("pict/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.calc_x = x
        self.calc_y = y

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
        self.air_friction = 0.95
        self.gravity = 0.5
        self.jump_strength = 10

        #debugging
        self.edit_mode = False
    
    def update(self):
        #TODO: add player movement and physics here
        
        if self.edit_mode:
            self.edit_stuff()
        else:
            self.normal_phisics_update()

        #update player position based on velocity
        self.try_move(self.velocity_x, self.velocity_y)

        #camera stuff
        left_limit = global_var.window_size[0] * const.CAMERA_MOVE_THRESHOLD
        right_limit = global_var.window_size[0] * (1 - const.CAMERA_MOVE_THRESHOLD)
        screen_x = self.calc_x - global_var.camera_x

        if screen_x < left_limit:
            global_var.camera_x -= left_limit - screen_x
        elif screen_x > right_limit:
            global_var.camera_x += screen_x - right_limit

        if global_var.camera_x < const.LEAST_CAMERA_X:
            global_var.camera_x = const.LEAST_CAMERA_X
        
        self.rect.x = self.calc_x - global_var.camera_x
        self.rect.y = self.calc_y

        return
    
    def try_move(self, dx, dy):
        self.move_axis(dx, 0)
        self.move_axis(0, dy)
        self.on_ground = self.check_on_ground()

    def move_axis(self, dx, dy):
        tmp_x = self.rect.x
        tmp_y = self.rect.y
        if dx != 0:
            self.rect.x += dx
            self.calc_x += dx
            if self.collide():
                direction = 1 if dx > 0 else -1
                while self.collide():
                    self.rect.x -= direction
                    self.calc_x -= direction
                self.velocity_x = 0

        if dy != 0:
            self.rect.y += dy
            self.calc_y += dy
            if self.collide():
                direction = 1 if dy > 0 else -1
                while self.collide():
                    self.rect.y -= direction
                    self.calc_y -= direction
                self.velocity_y = 0

    def collide(self):
        if self.calc_x < 0:
            return True
        for platform in real_game.platforms_group:
            if self.rect.colliderect(platform.rect):
                return True
        return False

    def check_on_ground(self):
        test_rect = self.rect.copy()
        test_rect.y += 1
        for platform in real_game.platforms_group:
            if test_rect.colliderect(platform.rect):
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
        else:
            if self.velocity_x > 0:
                self.velocity_x *= self.air_friction
            elif self.velocity_x < 0:
                self.velocity_x *= self.air_friction

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
        
        #friction
        if self.velocity_x > 0:
            self.velocity_x *= self.air_friction
        elif self.velocity_x < 0:
            self.velocity_x *= self.air_friction

        if self.velocity_y > 0:
            self.velocity_y *= self.air_friction
        elif self.velocity_y < 0:
            self.velocity_y *= self.air_friction
        
        if abs(self.velocity_x) < 0.1:
            self.velocity_x = 0
        
        if abs(self.velocity_y) < 0.1:
            self.velocity_y = 0

        #up and down for edit mode
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = max(self.velocity_y - self.accseleration[1], -self.max_speed[1])
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = min(self.velocity_y + self.accseleration[1], self.max_speed[1])
        
        self.velocity_x = max(min(self.velocity_x, self.max_speed[0]), -self.max_speed[0])
        self.velocity_y = max(min(self.velocity_y, self.max_speed[1]), -self.max_speed[1])