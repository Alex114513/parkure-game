import blinker
import pygame

pygame.init()

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
SWITCH_TO_MAIN_TITLE_EVENT_CODE = pygame.USEREVENT + 5
SWICH_TO_GAME_PREP_EVENT_CODE = pygame.USEREVENT + 6

TARGET_NEW_SAVE = "new_save"
TARGET_LOAD_SAVE = "load_save"
TARGET_GAME = "game"
TARGET_MAIN_TITLE = "main_title"
REAL_GAME = "real_game"
TARGET_GAME_PREP = "game_prep"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARK_BLUE = (50, 50, 80)

FPS = 60

#camera
CAMERA_SCROLL_SPEED = 5
CAMERA_MOVE_THRESHOLD = 0.2
LEAST_CAMERA_X = 0
LEAST_CAMERA_Y = 0
CAMERA_MOVE_STEP = 0.75

PLAYER_COLIDE_STEP = 5

CLOCK = pygame.time.Clock()

#fonts
DEAFAULT_FONT  = pygame.font.Font(None, 20)

#animation
clap_abs = 0.05
change_speed = 0.4