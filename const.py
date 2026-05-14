import blinker
import pygame

debug_mode = True
window_size = (800 , 800)

DEBUG=1
INFO=2
WARNING=3
ERROR=4
CRIC=5

SCREEN_RESIZE = blinker.signal("screen_resize")

SCREEN_RESIZE_CODE = 1 
SWITCH_TO_GAME_EVENT_CODE = pygame.USEREVENT + 1
SWITCH_TO_NEW_SAVE_EVENT_CODE = pygame.USEREVENT + 2
SWITCH_TO_LOAD_SAVE_EVENT_CODE = pygame.USEREVENT + 3
SWITCH_TO_REAL_GAME_EVENT_CODE = pygame.USEREVENT + 4

TARGET_NEW_SAVE = "new_save"
TARGET_LOAD_SAVE = "load_save"
TARGET_GAME = "game"
REAL_GAME = "real_game"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_BLUE = (50, 50, 80)

FPS = 60

#camera
camera_scroll_speed = 5
least_move_threshold = 0.3
least_camera_x = 0
cam_move_step = 0.1