import importlib
import sys
import types
import unittest

import const
import pygame
import scenes
import sprites


class PlayerGroundStateTests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))
        missing = object()
        self._missing = missing
        self._original_modules = {
            "sprites.player": sys.modules.get("sprites.player", missing),
            "sprites.edit_mode_currsor": sys.modules.get("sprites.edit_mode_currsor", missing),
            "scenes.real_game": sys.modules.get("scenes.real_game", missing),
        }
        self._original_package_attributes = {
            (sprites, "player"): getattr(sprites, "player", missing),
            (sprites, "edit_mode_currsor"): getattr(sprites, "edit_mode_currsor", missing),
            (scenes, "real_game"): getattr(scenes, "real_game", missing),
        }

        fake_edit_mode = types.ModuleType("sprites.edit_mode_currsor")
        class DummyCursor:
            pass

        fake_edit_mode.Edit_mode_cursor = DummyCursor
        sys.modules["sprites.edit_mode_currsor"] = fake_edit_mode
        sprites.edit_mode_currsor = fake_edit_mode

        fake_real_game = types.ModuleType("scenes.real_game")
        fake_real_game.platforms_group = pygame.sprite.Group()
        sys.modules["scenes.real_game"] = fake_real_game
        scenes.real_game = fake_real_game

        sys.modules.pop("sprites.player", None)
        self.player_module = importlib.import_module("sprites.player")
        sprites.player = self.player_module

        original_load = pygame.image.load
        pygame.image.load = lambda *args, **kwargs: pygame.Surface((10, 10), pygame.SRCALPHA)
        try:
            self.player = self.player_module.Player(0, 0)
        finally:
            pygame.image.load = original_load

    def tearDown(self):
        for module_name, module in self._original_modules.items():
            if module is self._missing:
                sys.modules.pop(module_name, None)
            else:
                sys.modules[module_name] = module

        for (package, attribute), value in self._original_package_attributes.items():
            if value is self._missing:
                delattr(package, attribute)
            else:
                setattr(package, attribute, value)

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

    def test_ground_contact_works_on_a_slope(self):
        platform = pygame.sprite.Sprite()
        platform.rect = pygame.Rect(0, 0, 20, 20)
        platform.mask = pygame.mask.Mask((20, 20))
        for x in range(20):
            for y in range(10 if x < 10 else 8, 20):
                platform.mask.set_at((x, y), 1)
        sys.modules["scenes.real_game"].platforms_group.add(platform)

        self.player.rect = pygame.Rect(2, 0, 10, 10)
        self.player.calc_x = 2
        self.player.calc_y = 0
        self.player.mask.fill()

        self.player.update_ground_state()

        self.assertTrue(self.player.on_ground)

    def test_step_up_does_not_zero_horizontal_velocity(self):
        platform = pygame.sprite.Sprite()
        platform.rect = pygame.Rect(0, 0, 20, 20)
        platform.mask = pygame.mask.Mask((20, 20))
        step_height = (
            const.CLICES_WHILE_MOVING
            * const.SINGLE_STEP_WHILE_FINDING_VALID_POSITION
        )
        for x in range(20):
            for y in range(10 if x < 10 else 10 - step_height, 20):
                platform.mask.set_at((x, y), 1)
        sys.modules["scenes.real_game"].platforms_group.add(platform)

        self.player.rect = pygame.Rect(0, 0, 10, 10)
        self.player.calc_x = 0
        self.player.calc_y = 0
        self.player.mask.fill()
        self.player.on_ground = True
        self.player.velocity_x = 2

        self.player.move_axis(2, 0)

        self.assertEqual(self.player.rect.x, 2)
        self.assertEqual(self.player.rect.y, -step_height)
        self.assertEqual(self.player.velocity_x, 2)

    def test_horizontal_movement_does_not_climb_a_wall_while_airborne(self):
        wall = pygame.sprite.Sprite()
        wall.rect = pygame.Rect(10, 6, 20, 4)
        wall.mask = pygame.mask.Mask((20, 4))
        wall.mask.fill()
        sys.modules["scenes.real_game"].platforms_group.add(wall)

        self.player.rect = pygame.Rect(0, 0, 10, 10)
        self.player.calc_x = 0
        self.player.calc_y = 0
        self.player.mask.fill()
        self.player.on_ground = False
        self.player.velocity_x = 2

        for _ in range(8):
            self.player.move_axis(2, 0)

        self.assertEqual(self.player.rect.x, 0)
        self.assertEqual(self.player.rect.y, 0)

    def test_diagonal_upward_collision_does_not_leave_player_inside_slope(self):
        platform_surface = pygame.Surface((80, 16), pygame.SRCALPHA)
        platform_surface.fill((255, 255, 255, 255))
        platform_image = pygame.transform.rotate(platform_surface, 30)
        platform = pygame.sprite.Sprite()
        platform.rect = platform_image.get_rect(topleft=(100, 100))
        platform.mask = pygame.mask.from_surface(platform_image)
        sys.modules["scenes.real_game"].platforms_group.add(platform)

        self.player.rect = pygame.Rect(90, 141, 10, 10)
        self.player.calc_x = 90
        self.player.calc_y = 141
        self.player.mask.fill()
        self.player.on_ground = False

        self.assertFalse(self.player.collide())
        self.player.move_axis(1, 0)
        self.player.move_axis(0, -1)

        self.assertFalse(self.player.collide())


if __name__ == "__main__":
    unittest.main()
