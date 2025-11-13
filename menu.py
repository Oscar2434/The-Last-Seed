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

Fondo = pygame.image.load("imagenes\\portada.png")
button_config = pygame.image.load("imagenes\\confi.png")
title_img = pygame.image.load("imagenes\\titulo1.png").convert_alpha()

title_img = pygame.transform.scale(
    title_img,
    (
        int(title_img.get_width() * 0.90),
        int(title_img.get_height() * 0.90)
    )
)

title_rect = title_img.get_rect(center=(constants.WIDTH // 2, 250))

Fondo = pygame.transform.scale(Fondo, (constants.WIDTH, constants.HEIGHT))
button_config = pygame.transform.scale(button_config, (120, 100))

config_button = Button(
    150 // 2 - button_config.get_width() // 2,
    800 // 2 - button_config.get_height() // 2,
    button_config, 1
)

def menu():
    run = True
    while run:

        # PLAY NORMAL Y HOVER SEGÚN IDIOMA
        if config.lenguaje:
            play_normal = pygame.image.load("imagenes\\Play.png")
            play_hover = pygame.image.load("imagenes\\PlayR.png")
            exit_img = pygame.image.load("imagenes\\Exit.png")
        else:
            play_normal = pygame.image.load("imagenes\\Jugar.png")
            play_hover = pygame.image.load("imagenes\\JugarR.png")
            exit_img = pygame.image.load("imagenes\\Salida.png")

        play_normal = pygame.transform.scale(play_normal, (300, 100))
        play_hover = pygame.transform.scale(play_hover, (300, 100))
        exit_img = pygame.transform.scale(exit_img, (200, 100))

        # BOTÓN PLAY (con hover manual)
        mouse_pos = pygame.mouse.get_pos()

        play_rect = play_normal.get_rect(
            center=(780 // 2, 500 // 2)
        )

        if play_rect.collidepoint(mouse_pos):
            play_button_img = play_hover
        else:
            play_button_img = play_normal

        play_button = Button(
            play_rect.x,
            play_rect.y,
            play_button_img,
            1
        )

        # BOTÓN EXIT (sin hover porque no lo pediste)
        exit_button = Button(
            780 // 2 - exit_img.get_width() // 2,
            800 // 2 - exit_img.get_height() // 2,
            exit_img, 1
        )

        screen.blit(Fondo, (0, 0))
        screen.blit(title_img, title_rect)

        # DRAW PLAY
        if play_button.draw(screen):
            nivels.niveles()

        # DRAW CONFIG
        if config_button.draw(screen):
            config.config_menu()

        # DRAW EXIT
        if exit_button.draw(screen):
            pygame.quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def main_loop():
    main.main()

if __name__ == "__main__":
    menu()
