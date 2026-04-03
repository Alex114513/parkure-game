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