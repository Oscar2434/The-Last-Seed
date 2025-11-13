import pygame
import sys
import constants
from button import Button
import main
import config
import nivels

pygame.init()

if config.music:
    pygame.mixer.init()
    pygame.mixer.music.load('music/prueba1.mp3')
    pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("The Last Seed")

# imágenes
Fondo = pygame.image.load("imagenes\\portada.png")
button_config = pygame.image.load("imagenes\\confi.png")
title_img = pygame.image.load("imagenes\\titulo1.png").convert_alpha()

Fondo = pygame.transform.scale(Fondo, (constants.WIDTH, constants.HEIGHT))
button_config = pygame.transform.scale(button_config, (120, 100))

# escala del título 
title_img = pygame.transform.scale(
    title_img,
    (
        int(title_img.get_width() * 0.90),
        int(title_img.get_height() * 0.90)
    )
)

title_rect = title_img.get_rect(center=(constants.WIDTH // 2, 250))

# botón config
config_button = Button(
    150 // 2 - button_config.get_width() // 2,
    800 // 2 - button_config.get_height() // 2,
    button_config, 1
)

def menu():
    run = True
    while run:

        # cargar imágenes por idioma
        if config.lenguaje:
            play_normal = pygame.image.load("imagenes\\Play.png")
            play_hover  = pygame.image.load("imagenes\\PlayR.png")

            exit_normal = pygame.image.load("imagenes\\Exit.png")
        else:
            play_normal = pygame.image.load("imagenes\\Jugar.png")
            play_hover  = pygame.image.load("imagenes\\playR.png")

            exit_normal = pygame.image.load("imagenes\\Salida.png")

        # ESCALAR
        play_normal = pygame.transform.scale(play_normal, (300, 100))
        play_hover  = pygame.transform.scale(play_hover,  (300, 100))
        exit_normal = pygame.transform.scale(exit_normal, (200, 100))

        # rects
        play_rect = play_normal.get_rect(
            center=(constants.WIDTH // 2, 500 // 2)
        )
        exit_rect = exit_normal.get_rect(
            center=(constants.WIDTH // 2, 800 // 2)
        )

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        screen.blit(Fondo, (0, 0))
        screen.blit(title_img, title_rect)

        # HOVER PLAY
        if play_rect.collidepoint(mouse):
            screen.blit(play_hover, play_rect)
            if click:
                nivels.niveles()
        else:
            screen.blit(play_normal, play_rect)

        # botón config
        if config_button.draw(screen):
            config.config_menu()

        # EXIT
        if exit_rect.collidepoint(mouse):
            screen.blit(exit_normal, exit_rect)
            if click:
                pygame.quit()
                sys.exit()
        else:
            screen.blit(exit_normal, exit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def main_loop():
    main.main()


if __name__ == "__main__":
    menu()
