import pygame

#camera
camera_x = 0
camera_y = 0

#window
window_size = (800, 800)

#sprites
Edit_mode_currsor = None
return_button = None
return_button_group = pygame.sprite.Group()

#scenes
scene_stack = []
scene_stack_top = -1