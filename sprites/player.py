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
        self.mask = pygame.mask.from_surface(self.image)

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
        self._ground_buffer = 0
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
        self.try_move(self.velocity_x, 0)
        self.try_move(0, self.velocity_y)

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
        if self.collide():
            tools.log(f"player may be stuck in a platform at ({self.rect.x}, {self.rect.y})", const.WARNING)
        self.move_axis(dx, 0)
        self.move_axis(0, dy)
        self.update_ground_state()

    def move_axis(self, dx, dy):
        tmp_x = self.rect.x
        tmp_y = self.rect.y
        if dx != 0:
            self.rect.x += dx
            self.calc_x += dx
            if self.collide():
                direction = 1 if dx > 0 else -1
                flag = False
                for i in range(10):  # Limit the number of iterations to prevent infinite loops
                    self.rect.y -= 1
                    self.calc_y -= 1
                    tools.log(f"Resovling smooth up-slope: step{i}, player_pos: (x: {self.calc_x} y: {self.calc_y})", const.DEBUG)
                    if not self.collide():
                        tools.log(f"Resovled smooth up-slope, coliding?:{self.collide()}, player_pos: (x: {self.calc_x} y: {self.calc_y})", const.DEBUG)
                        flag = True
                        break
                
                if flag == False:
                    self.rect.y = tmp_y
                    self.calc_y = tmp_y
                
            flag2 = False
            for i in range(10):  # Limit the number of iterations to prevent infinite loops
                self.rect.y += 1
                self.calc_y += 1
                tools.log(f"Resolving smooth down-slope: step{i}, player_pos: (x: {self.calc_x} y: {self.calc_y})", const.DEBUG)
                if self.collide():
                    self.rect.y -= 1
                    self.calc_y -= 1
                    self.velocity_y = 0
                    tools.log(f"Resovled smooth down-slope, coliding?:{self.collide()}, player_pos: (x: {self.calc_x} y: {self.calc_y})", const.DEBUG)
                    flag2 = True
                    break
            if flag2 == False:
                tools.log("Faild to resolve smooth down-slope", const.DEBUG)
                self.rect.y = tmp_y  # Reset to original position if no collision detected
                self.calc_y = tmp_y
            
            if self.collide():
                tools.log("Faild to resovle smooth up-slope", const.DEBUG)
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
                offset = (platform.rect.left - self.rect.left, platform.rect.top - self.rect.top)
                if self.mask.overlap(platform.mask, offset):
                    return True
        return False

    def update_ground_state(self):
        if self.check_on_ground():
            self._ground_buffer = 3
        elif self._ground_buffer > 0:
            self._ground_buffer -= 1
        self.on_ground = self._ground_buffer > 0

    def check_on_ground(self):
        probe_y = self.rect.bottom - 2
        probe_xs = [self.rect.left + 1, self.rect.centerx, self.rect.right - 1]

        for probe_x in probe_xs:
            for platform in real_game.platforms_group:
                if not platform.rect.collidepoint(probe_x, probe_y):
                    continue

                local_x = int(probe_x - platform.rect.left)
                local_y = int(probe_y - platform.rect.top)
                if 0 <= local_x < platform.mask.get_size()[0] and 0 <= local_y < platform.mask.get_size()[1]:
                    if platform.mask.get_at((local_x, local_y)):
                        return True

        return False
    
    def normal_phisics_update(self):
        #velocity
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.velocity_x = max(self.velocity_x - self.accseleration[0], -self.max_speed[0])
        if keys[pygame.K_d]:
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
        if keys[pygame.K_a]:
            self.velocity_x = max(self.velocity_x - self.accseleration[0], -self.max_speed[0])
        if keys[pygame.K_d]:
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
        if keys[pygame.K_w]:
            self.velocity_y = max(self.velocity_y - self.accseleration[1], -self.max_speed[1])
        if keys[pygame.K_s]:
            self.velocity_y = min(self.velocity_y + self.accseleration[1], self.max_speed[1])
        
        self.velocity_x = max(min(self.velocity_x, self.max_speed[0]), -self.max_speed[0])
        self.velocity_y = max(min(self.velocity_y, self.max_speed[1]), -self.max_speed[1])
        global_var.Edit_mode_currsor.update()
    def init_edit_mode(self):
        global_var.Edit_mode_currsor = edit_mode_currsor.Edit_mode_cursor(self)
        