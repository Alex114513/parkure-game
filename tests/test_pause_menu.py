import importlib
import unittest
from unittest.mock import call, patch

import const
import pygame
import tools


class PauseMenuTests(unittest.TestCase):
    def test_clear_scene_transition_timers_clears_all_pending_scene_switch_events(self):
        with patch.object(pygame.time, "set_timer") as mock_set_timer, \
             patch.object(pygame.event, "clear") as mock_clear:
            tools.clear_scene_transition_timers()

        self.assertEqual(
            mock_set_timer.call_args_list,
            [
                call(const.SWITCH_TO_GAME_EVENT_CODE, 0),
                call(const.SWITCH_TO_NEW_SAVE_EVENT_CODE, 0),
                call(const.SWITCH_TO_LOAD_SAVE_EVENT_CODE, 0),
                call(const.SWITCH_TO_REAL_GAME_EVENT_CODE, 0),
                call(const.SWICH_TO_GAME_PREP_EVENT_CODE, 0),
                call(const.SWITCH_TO_MAIN_TITLE_EVENT_CODE, 0),
            ],
        )
        mock_clear.assert_called_once_with()

    def test_quit_event_requests_game_exit_without_quitting_pygame(self):
        pause_menu = importlib.import_module("scenes.pause_menu")
        surface = pygame.Surface((1, 1))

        with patch.object(pause_menu.pygame.display, "get_surface", return_value=surface), \
             patch.object(pause_menu.pygame.display, "set_mode", return_value=surface), \
             patch.object(pause_menu.pygame.display, "flip"), \
             patch.object(pause_menu.pygame.event, "get", return_value=[pygame.event.Event(pygame.QUIT)]):
            result = pause_menu.start("test-save")

        self.assertTrue(result)

    def test_save_and_exit_button_saves_and_exits(self):
        pause_menu = importlib.import_module("scenes.pause_menu")
        surface = pygame.Surface((800, 600), pygame.SRCALPHA)
        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(200, 500))

        class DummyClock:
            def tick(self, *_args, **_kwargs):
                raise RuntimeError("stop")

        with patch.object(pause_menu.pygame.display, "get_surface", return_value=surface), \
             patch.object(pause_menu.pygame.display, "set_mode", return_value=surface), \
             patch.object(pause_menu.pygame.display, "flip"), \
             patch.object(pause_menu.pygame.image, "load", return_value=pygame.Surface((256, 128), pygame.SRCALPHA)), \
             patch.object(pause_menu.pygame.event, "get", return_value=[click_event]), \
             patch.object(pause_menu.pygame.time, "Clock", return_value=DummyClock()), \
             patch.object(pause_menu.tools, "new_save") as mock_new_save:
            result = pause_menu.start("test-save")

        self.assertTrue(result)
        mock_new_save.assert_called_once_with("test-save")


if __name__ == "__main__":
    unittest.main()
