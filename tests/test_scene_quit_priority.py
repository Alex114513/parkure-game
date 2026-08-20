import importlib
import unittest
from unittest.mock import patch

import const
import pygame


class SceneQuitPriorityTests(unittest.TestCase):
    def test_quit_event_prevents_later_scene_switch_event_from_running(self):
        game_prep = importlib.import_module("scenes.game_prep")
        surface = pygame.Surface((800, 600))

        class DummyButton(pygame.sprite.Sprite):
            def __init__(self, *args, **kwargs):
                super().__init__()
                self.image = pygame.Surface((1, 1))
                self.rect = self.image.get_rect()
                self.target_scene = kwargs.get("target_scene")

            def clicked(self):
                pass

            def messege(self, *args, **kwargs):
                pass

        with patch.object(game_prep.button, "Button", DummyButton), \
             patch.object(game_prep.scenes.main_title, "screen", surface), \
             patch.object(game_prep.pygame.display, "update"), \
             patch.object(game_prep.pygame, "quit"), \
             patch.object(game_prep, "switch") as mock_switch, \
             patch.object(game_prep.pygame.event, "get", return_value=[
                 pygame.event.Event(pygame.QUIT),
                 pygame.event.Event(const.SWITCH_TO_LOAD_SAVE_EVENT_CODE),
             ]):
            game_prep.start()

        mock_switch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
