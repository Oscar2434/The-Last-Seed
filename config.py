import pygame
import sys
import constants
from button import Button

pygame.init()


lenguaje = True # false = español, true = ingles
music = True # false = sin muisica, true = con musica

# ventana
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
if lenguaje: 
    pygame.display.set_caption("configuration")
else: 
    pygame.display.set_caption("Configuración")
# imágenes
Fondo = pygame.image.load("imagenes/portada.png")  # Cambia el nombre si es necesario
Fondo = pygame.transform.scale(Fondo, (constants.WIDTH, constants.HEIGHT))

# Bucle de configuración
def config_menu():
    run = True
    while run:
        screen.blit(Fondo, (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Salir con la tecla ESC
                    run = False

        pygame.display.update()  # Actualiza la pantalla

if __name__ == "__main__":
    config_menu()