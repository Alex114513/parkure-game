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
        up_limit = global_var.window_size[1] * const.CAMERA_MOVE_THRESHOLD
        down_limit = global_var.window_size[1] * (1 - const.CAMERA_MOVE_THRESHOLD)
        screen_x = self.calc_x - global_var.camera_x
        screen_y = self.calc_y - global_var.camera_y

        if screen_x < left_limit:
            global_var.camera_x -= left_limit - screen_x
        elif screen_x > right_limit:
            global_var.camera_x += screen_x - right_limit

        if screen_y < up_limit:
            global_var.camera_y -= up_limit - screen_y
        elif screen_y > down_limit:
            global_var.camera_y += screen_y - down_limit

        if global_var.camera_x < const.LEAST_CAMERA_X:
            global_var.camera_x = const.LEAST_CAMERA_X
        if global_var.camera_y < const.LEAST_CAMERA_Y:
            global_var.camera_y = const.LEAST_CAMERA_Y

        self.rect.x = self.calc_x - global_var.camera_x
        self.rect.y = self.calc_y - global_var.camera_y
        self.calc_x = self.rect.x + global_var.camera_x
        self.calc_y = self.rect.y + global_var.camera_y

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

        # move the player along the x-axis
        self.rect.x += dx
        self.calc_x += dx
        if self.collide():
            can_move_up = False
            if dx != 0 and dy == 0 and self.on_ground:
                for _ in range(const.CLICES_WHILE_MOVING):
                    self.rect.y -= const.SINGLE_STEP_WHILE_FINDING_VALID_POSITION
                    self.calc_y -= const.SINGLE_STEP_WHILE_FINDING_VALID_POSITION
                    if not self.collide() and self.check_on_ground():
                        can_move_up = True
                        break
            if not can_move_up:
                self.rect.y = tmp_y
                self.calc_y = tmp_y + global_var.camera_y
                # move step by step to find a valid position
                while self.collide() and self.rect.x != tmp_x:
                    if dx > 0:
                        self.rect.x -= const.SINGLE_STEP_WHILE_FINDING_VALID_POSITION
                        self.calc_x -= const.SINGLE_STEP_WHILE_FINDING_VALID_POSITION
                    elif dx < 0:
                        self.rect.x += const.SINGLE_STEP_WHILE_FINDING_VALID_POSITION
                        self.calc_x += const.SINGLE_STEP_WHILE_FINDING_VALID_POSITION
                if self.rect.x == tmp_x:
                    self.calc_x = tmp_x + global_var.camera_x
                self.velocity_x = 0
        else:
            #try smooth down-slope movement
            if dy == 0 and self.on_ground:
                self.rect.y += const.SINGLE_STEP_WHILE_FINDING_VALID_POSITION
                self.calc_y += const.SINGLE_STEP_WHILE_FINDING_VALID_POSITION
                if self.collide():
                    self.rect.y = tmp_y
                    self.calc_y = tmp_y + global_var.camera_y

        #move the player along the y-axis
        self.rect.y += dy
        self.calc_y += dy
        if self.collide():
            #move step by step to find a valid position
            while self.collide() and self.rect.y != tmp_y:
                if dy > 0:
                    self.rect.y -= const.SINGLE_STEP_WHILE_FINDING_VALID_POSITION
                    self.calc_y -= const.SINGLE_STEP_WHILE_FINDING_VALID_POSITION
                elif dy < 0:
                    self.rect.y += const.SINGLE_STEP_WHILE_FINDING_VALID_POSITION
                    self.calc_y += const.SINGLE_STEP_WHILE_FINDING_VALID_POSITION
            self.calc_y = tmp_y + global_var.camera_y
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
        else:
            self._ground_buffer = 0
        #elif self._ground_buffer > 0:
        #    self._ground_buffer -= 1
        self.on_ground = self._ground_buffer > 0

    def check_on_ground(self):
        mask_width, _ = self.mask.get_size()
        mask_bounds_list = self.mask.get_bounding_rects()
        if not mask_bounds_list:
            return False

        effective_bottom = max(bounds.bottom for bounds in mask_bounds_list)
        ground_mask = pygame.mask.Mask((mask_width, 1))
        for x in range(mask_width):
            if self.mask.get_at((x, effective_bottom - 1)):
                ground_mask.set_at((x, 0), 1)

        for platform in real_game.platforms_group:
            for gap in range(3):
                offset = (
                    platform.rect.left - self.rect.left,
                    platform.rect.top - (self.rect.top + effective_bottom + gap),
                )
                if ground_mask.overlap(platform.mask, offset):
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

    def ask_position(self):
        ret = {
            "x_pos": self.calc_x, 
            "y_pos": self.calc_y
        }
        return ret
        