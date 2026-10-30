import pygame
from sprites import player
import json
import const
import tools
import global_var

from scenes import real_game

with open("configs/enemys/normal_enemy.json", "r") as f:
    config = json.load(f)

class Normal_enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(config["image"]["path"]).convert_alpha()
        self.rect = self.image.get_rect()
    
        self.rect.x = x
        self.rect.y = y

        self.calc_x = x
        self.calc_y = y

        self.xvelocity = 0
        self.xspeed = 0
        self.yvelocity = 0
        self.yspeed = 0

    def colide(self):
        for platform in real_game.platforms_group:
            if self.rect.colliderect(platform.rect):
                return True
        return False

    def try_move(self, mx, my):
        self.calc_x += mx
        while self.colide():
            self.calc_x += -mx
            self.rect.x = self.calc_x % global_var.window_size[0]            
        self.calc_y += my
        while self.colide():
            self.calc_y += -my
            self.rect.y = self.calc_y % global_var.window_size[1]
            

    def fix_velocity_by_limmit(self):
        if self.xvelocity > config["movement"]["xmax"]:
            self.xvelocity = config["movement"]["xmax"]
        if self.xvelocity < -config["movement"]["xmax"]:
            self.xvelocity = -config["movement"]["xmax"]

        if self.yvelocity > config["phisics"]["ymaxdrop"]:
            self.yvelocity = config["phisics"]["ymaxdrop"]

    def gravity_tick(self):
        self.yvelocity += config["phisics"]["ygravity"]
        self.fix_velocity_by_limmit()

    def do_phisics(self):
        self.gravity_tick()
    
    def control_ai(self):
        player_position = real_game.player.ask_position()
        player_x = player_position["x_pos"]
        player_y = player_position["y_pos"]
        if player_x < self.calc_x:
            self.xvelocity -= config["movement"]["xaccseleration"]
        else:
            self.xvelocity += config["movement"]["xaccseleration"]

        self.fix_velocity_by_limmit()

    def update_state_by_phisics(self):
        self.try_move(self.xvelocity, self.yvelocity)

        self.rect.x = self.calc_x % global_var.window_size[0]
        self.rect.y = self.calc_y % global_var.window_size[1]

    def update(self):
        self.control_ai()
        self.do_phisics()
        self.update_state_by_phisics()
    