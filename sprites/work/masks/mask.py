import pygame
import tools
import scenes.main_title as main_title

class Mask(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface(main_title.window_size, pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.alpha = 255
        self.fading = False
        self.target_alpha = 255
        self.speed = 0
        self.image.set_alpha(self.alpha)
        main_title.masks_group.add(self)
    
    def update(self):
        if self.fading:
            if self.alpha < self.target_alpha:
                self.alpha += self.speed
                if self.alpha >= self.target_alpha:
                    self.alpha = self.target_alpha
                    self.fading = False
                    if self.target_alpha == 255:
                        self.kill()
                    
                    if abs(self.target_alpha - 250)<2:
                        #kill all buttons just before swithing scene
                        tools.kill_buttons()

            elif self.alpha > self.target_alpha:
                self.alpha -= self.speed
                if self.alpha <= self.target_alpha:
                    self.alpha = self.target_alpha
                    self.fading = False
                    if self.target_alpha == 0:
                        self.kill()
            self.image.set_alpha(int(self.alpha))
    
    def fade(self, time):
        self.fading = True
        self.target_alpha = 0
        self.speed = 255 / (time * 60)
    
    def fade_in(self, time):
        self.fading = True
        self.alpha = 0
        self.target_alpha = 255
        self.speed = 255 / (time * 60)