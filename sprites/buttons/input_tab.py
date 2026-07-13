import pygame
import tools
import const
from sprites.buttons.button import button_config

class InputTab(pygame.sprite.Sprite):
    def __init__(self, text, font, color):
        super().__init__()
        self.text = text
        self.font = font
        self.color = color
        config = button_config["input_tab"]

        self.original_image = pygame.image.load(config["path"]).convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = tuple(config["position"])
        self.active = False

        tools.log(f"INPUT TAB: Initialized with text: '{self.text}', font: '{self.font}', color: {self.color}, position: {self.rect.topleft}" , const.INFO)

        self._render_text()

    def _render_text(self):
        self.image = self.original_image.copy()
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        #self.image.blit(text_surface, text_rect)
        return text_surface, text_rect  # Return the text surface and its rect for drawing

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            tools.log(f"INPUT TAB: input tab clicked at position: {event.pos}" , const.DEBUG)
            self.active = self.rect.collidepoint(event.pos)

        if self.active and event.type == pygame.KEYDOWN:
            tools.log(f"INPUT TAB: key pressed: {event.unicode}, text: {self.text}" , const.DEBUG)
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                pass
            elif event.unicode and event.unicode.isprintable():
                self.text += event.unicode
            self._render_text()

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def messege(self , sender , **kwargs):
        data = kwargs.get('data')
        if data[0] == const.SCREEN_RESIZE_CODE:
            tools.log(f"start button received screen resize messege from {sender} with data:{data}" , const.DEBUG)
            #calculate the multiplier for the x and y axis
            x_multiplier = data[1][0] / const.window_size[0]
            y_multiplier = data[1][1] / const.window_size[1]
            #calculate the new width and height of the button
            multiplier = min(x_multiplier , y_multiplier)
            new_width = int(button_config[self.type]["size"][0] * multiplier)
            new_height = int(button_config[self.type]["size"][1] * multiplier)
            #apply the new width and height to the button image
            self.image = pygame.transform.scale(self.original_image , (new_width , new_height))
            #calculate the new x and y position of the button
            new_x = int(self.original_x * x_multiplier)
            new_y = int(self.original_y * y_multiplier)
            #apply the new x and y position to the button rect
            self.rect.x = new_x
            self.rect.y = new_y