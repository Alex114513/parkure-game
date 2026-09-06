import importlib
import sys
import types
import unittest

import pygame


class PlayerGroundStateTests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))

        fake_edit_mode = types.ModuleType("sprites.edit_mode_currsor")
        class DummyCursor:
            pass

        fake_edit_mode.Edit_mode_cursor = DummyCursor
        sys.modules["sprites.edit_mode_currsor"] = fake_edit_mode

        fake_real_game = types.ModuleType("scenes.real_game")
        fake_real_game.platforms_group = pygame.sprite.Group()
        sys.modules["scenes.real_game"] = fake_real_game

        sys.modules.pop("sprites.player", None)
        self.player_module = importlib.import_module("sprites.player")

        original_load = pygame.image.load
        pygame.image.load = lambda *args, **kwargs: pygame.Surface((10, 10), pygame.SRCALPHA)
        try:
            self.player = self.player_module.Player(0, 0)
        finally:
            pygame.image.load = original_load

    def test_ground_contact_buffer_keeps_player_on_ground_for_a_short_time(self):
        platform = pygame.sprite.Sprite()
        platform.rect = pygame.Rect(0, 50, 20, 20)
        surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        surface.fill((255, 255, 255))
        platform.mask = pygame.mask.from_surface(surface)
        sys.modules["scenes.real_game"].platforms_group.add(platform)

        self.player.rect = pygame.Rect(0, 40, 10, 10)
        self.player.calc_x = 0
        self.player.calc_y = 40
        self.player.mask = pygame.mask.from_surface(pygame.Surface((10, 10), pygame.SRCALPHA))
        pygame.Surface((10, 10), pygame.SRCALPHA).fill((255, 255, 255))

        self.player.mask = pygame.mask.from_surface(
            pygame.Surface((10, 10), pygame.SRCALPHA)
        )
        self.player.mask.fill()

        self.player.update_ground_state()
        self.assertTrue(self.player.on_ground)

        self.player.rect = pygame.Rect(0, 0, 10, 10)
        self.player.calc_x = 0
        self.player.calc_y = 0
        self.player._ground_buffer = 0
        self.player.update_ground_state()
        self.assertFalse(self.player.on_ground)

    def test_wall_contact_does_not_count_as_ground_contact(self):
        wall = pygame.sprite.Sprite()
        wall.rect = pygame.Rect(10, 0, 20, 40)
        surface = pygame.Surface((20, 40), pygame.SRCALPHA)
        surface.fill((255, 255, 255))
        wall.mask = pygame.mask.from_surface(surface)
        sys.modules["scenes.real_game"].platforms_group.add(wall)

        self.player.rect = pygame.Rect(0, 0, 10, 10)
        self.player.calc_x = 0
        self.player.calc_y = 0
        self.player.mask = pygame.mask.from_surface(
            pygame.Surface((10, 10), pygame.SRCALPHA)
        )
        self.player.mask.fill()

        self.player.update_ground_state()
        self.assertFalse(self.player.on_ground)

    def test_ground_contact_works_when_player_mask_bottom_row_is_transparent(self):
        platform = pygame.sprite.Sprite()
        platform.rect = pygame.Rect(0, 50, 20, 20)
        surface = pygame.Surface((20, 20), pygame.SRCALPHA)
        surface.fill((255, 255, 255))
        platform.mask = pygame.mask.from_surface(surface)
        sys.modules["scenes.real_game"].platforms_group.add(platform)

        player_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
        player_surface.fill((255, 255, 255))
        player_surface.fill((0, 0, 0, 0), pygame.Rect(0, 9, 10, 1))
        self.player.rect = pygame.Rect(0, 40, 10, 10)
        self.player.calc_x = 0
        self.player.calc_y = 40
        self.player.mask = pygame.mask.from_surface(player_surface)

        self.player.update_ground_state()
        self.assertTrue(self.player.on_ground)


if __name__ == "__main__":
    unittest.main()
