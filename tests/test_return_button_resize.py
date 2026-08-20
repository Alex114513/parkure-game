import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import unittest

import const
import pygame
import tools


class ReturnButtonResizeTests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))
        self.original_window_size = const.window_size
        const.window_size = (800, 600)

    def tearDown(self):
        const.window_size = self.original_window_size
        pygame.quit()

    def test_create_return_button_registers_for_resize_updates(self):
        button = tools.create_return_button(const.TARGET_MAIN_TITLE)
        initial_rect = button.rect.copy()

        const.SCREEN_RESIZE.send(data=(const.SCREEN_RESIZE_CODE, (1200, 900)))

        self.assertNotEqual(button.rect.x, initial_rect.x)
        self.assertNotEqual(button.rect.y, initial_rect.y)
        self.assertNotEqual(button.rect.width, initial_rect.width)
        self.assertNotEqual(button.rect.height, initial_rect.height)


if __name__ == "__main__":
    unittest.main()
