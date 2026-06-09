import pygame
import global_var
import tools
import const
import json
import scenes.real_game as real_game

class Edit_mode_cursor(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.selected_thing = 'platform' #name must be a thing's name in pict/ground
        self.raw_image = pygame.image.load(f"pict/ground/{self.selected_thing}.png").convert_alpha()

        self.target_platform_size = (100, 20) #default platform size
        self.target_platform_rotation = 0 #default platform rotation
        self.rect = pygame.Rect(0, 0, *self.target_platform_size)
        self._refresh_image()

    def _refresh_image(self):
        self.base_image = pygame.transform.scale(self.raw_image, self.target_platform_size)
        self.image = pygame.transform.rotate(self.base_image, self.target_platform_rotation)
        self.image.set_alpha(128)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self._refresh_image()
        self.rect.center = pygame.mouse.get_pos()
    
    def remove_platform(self):
        if global_var.Edit_mode_currsor:
            # Implementation for removing a platform at the cursor's position
            try:
                with open(f"saves/{real_game.Save_name}/level.json", "r") as f:
                    save_data = json.load(f)
            except Exception as e:
                tools.log(f"error loading save data for removing platform: {e}" , const.ERROR)
                return
            if self.selected_thing == 'platform':
                mouse_x, mouse_y = pygame.mouse.get_pos()
                world_x = mouse_x + global_var.camera_x
                world_y = mouse_y + global_var.camera_y
                platform_to_remove = None
                for platform in save_data[str(real_game.current_level)]["platforms"]:
                    pos = platform["position"]
                    size = platform["size"]
                    rotation = platform.get("rotation", 0)
                    test_image = pygame.transform.scale(self.raw_image, size)
                    test_rotated = pygame.transform.rotate(test_image, rotation)
                    test_rect = test_rotated.get_rect(topleft=(pos[0], pos[1]))
                    if test_rect.collidepoint(world_x, world_y):
                        offset_x = int(world_x - test_rect.left)
                        offset_y = int(world_y - test_rect.top)
                        mask = pygame.mask.from_surface(test_rotated)
                        if 0 <= offset_x < test_rect.width and 0 <= offset_y < test_rect.height:
                            if mask.get_at((offset_x, offset_y)):
                                platform_to_remove = platform
                                break
                if platform_to_remove:
                    save_data[str(real_game.current_level)]["platforms"].remove(platform_to_remove)

                    try:
                        with open(f"saves/{real_game.Save_name}/level.json", "w") as f:
                            json.dump(save_data, f, indent=4)
                    except Exception as e:
                        tools.log(f"error saving level data after removing platform: {e}" , const.ERROR)
                        return

            real_game.reload_level()

    def place_platform(self):
        if global_var.Edit_mode_currsor:
            # Implementation for placing a platform at the cursor's position
            try:
                with open(f"saves/{real_game.Save_name}/level.json", "r") as f:
                    save_data = json.load(f)
            except Exception as e:
                tools.log(f"error loading save data for placing platform: {e}" , const.ERROR)
                return
            if self.selected_thing == 'platform':
                platform_size = self.target_platform_size
                mouse_x, mouse_y = pygame.mouse.get_pos()
                world_rect = self.image.get_rect(center=(mouse_x, mouse_y))
                world_x = world_rect.left + global_var.camera_x
                world_y = world_rect.top + global_var.camera_y
                new_platform = {
                    "position": [world_x, world_y],
                    "size": platform_size,
                    "rotation": self.target_platform_rotation
                }
                save_data[str(real_game.current_level)]["platforms"].append(new_platform)

                try:
                    with open(f"saves/{real_game.Save_name}/level.json", "w") as f:
                        json.dump(save_data, f, indent=4)
                except Exception as e:
                    tools.log(f"error saving level data after placing platform: {e}" , const.ERROR)
                    return

            real_game.reload_level()
                