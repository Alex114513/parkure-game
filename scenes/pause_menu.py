import pygame
from scenes import real_game
from scenes import main_title
from sprites.buttons import button
import tools
import const

pygame.init()


def start(save_name):
    screen = pygame.display.get_surface()
    if screen is None:
        screen = pygame.display.set_mode((800, 600))

    clock = pygame.time.Clock()

    save_and_exit_button = button.Button("save_and_exit", "exit")
    buttons_group = pygame.sprite.Group(save_and_exit_button)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                real_game.done = True
                return 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                return 3

            if event.type == pygame.MOUSEBUTTONDOWN:
                if save_and_exit_button.rect.collidepoint(event.pos):
                    save_and_exit_button.clicked()
                    tools.new_save(save_name)
                    running = False
                    return 2

        screen.fill((0, 0, 0))
        buttons_group.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    return 3
