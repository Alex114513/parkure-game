import unittest

import const
import global_var
import tools


class SceneReturnTargetTests(unittest.TestCase):
    def test_get_return_target_uses_parent_scene_when_reentering_current_scene(self):
        global_var.scene_stack = [const.TARGET_MAIN_TITLE, const.TARGET_GAME_PREP]
        global_var.scene_stack_top = 1

        self.assertEqual(
            tools.get_return_target(const.TARGET_GAME_PREP),
            const.TARGET_MAIN_TITLE,
        )


if __name__ == "__main__":
    unittest.main()
