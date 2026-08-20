import unittest
import pygame
import tools
import scenes.main_title as main_title


class MaskCleanupTests(unittest.TestCase):
    def test_prepare_for_new_scene_clears_mask_group(self):
        sprite = pygame.sprite.Sprite()
        main_title.masks_group.add(sprite)

        tools.prepare_for_new_scene()

        self.assertEqual(len(main_title.masks_group), 0)


if __name__ == "__main__":
    unittest.main()
