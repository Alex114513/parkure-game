import blinker

debug_mode = True
window_size = (800 , 800)

DEBUG=1
INFO=2
WARNING=3
ERROR=4
CRIC=5

SCREEN_RESIZE = blinker.signal("screen_resize")

SCREEN_RESIZE_CODE = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)