import pygame
import sys
import config
import constants
from button import Button
import main  # Nivel 1
import nivel_2  # Nivel 2

pygame.init()

# ventana
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("nivels")

# imágenes
Fondo = pygame.image.load("imagenes/portada.png")
Fondo = pygame.transform.scale(Fondo, (constants.WIDTH, constants.HEIGHT))

# imagen que depende del idioma del juego para los botones
if config.lenguaje:
    button_nivel_1 = pygame.image.load("assets/images/effects/nivel 1.png")
    button_nivel_2 = pygame.image.load("assets/images/effects/nivel 2.png")
else:
    button_nivel_1 = pygame.image.load("assets/images/effects/nivel 1.png")
    button_nivel_2 = pygame.image.load("assets/images/effects/nivel 2.png")

# Escalar imágenes y crear botones
button_nivel_1 = pygame.transform.scale(button_nivel_1, (322, 161))
button_nivel_1 = Button(480 // 2 - button_nivel_1.get_width() // 2, 700 // 2 - button_nivel_1.get_height() // 2, button_nivel_1, 1)

button_nivel_2 = pygame.transform.scale(button_nivel_2, (322, 161))
button_nivel_2 = Button(1080 // 2 - button_nivel_2.get_width() // 2, 700 // 2 - button_nivel_2.get_height() // 2, button_nivel_2, 1)

# Bucle principal
def niveles():
    run = True
    while run:
        screen.blit(Fondo, (0, 0))

        # Dibujar botones
        if button_nivel_1.draw(screen):
            import select_character
            select_character.show(level=1)  # Nueva pantalla antes de iniciar nivel 1

        if button_nivel_2.draw(screen):
            import select_character
            select_character.show(level=2)  # Nueva pantalla antes de iniciar nivel 2

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        pygame.display.update()

if __name__ == "__main__":
    niveles()
