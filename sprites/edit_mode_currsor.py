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
        self.image = pygame.image.load(f"pict/ground/{self.selected_thing}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.image.set_alpha(128) #make the cursor semi-transparent
    
    def update(self):
        self.rect.center = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    
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
                platform_size = [100, 20]
                mouse_x, mouse_y = pygame.mouse.get_pos()
                world_x = mouse_x + global_var.camera_x - platform_size[0] // 2
                world_y = mouse_y + global_var.camera_y - platform_size[1] // 2
                new_platform = {"position": [world_x, world_y], "size": platform_size}
                save_data[str(real_game.current_level)]["platforms"].append(new_platform)

                try:
                    with open(f"saves/{real_game.Save_name}/level.json", "w") as f:
                        json.dump(save_data, f, indent=4)
                except Exception as e:
                    tools.log(f"error saving level data after placing platform: {e}" , const.ERROR)
                    return

            real_game.reload_level()
                