import pygame
import sys
import constants
from button import Button
import main  # Importar el archivo main para acceder a su funcionalidad

pygame.init()

# ventana
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("nivels")

# imágenes
Fondo = pygame.image.load("imagenes/portada.png")  # Cambia el nombre si es necesario
Fondo = pygame.transform.scale(Fondo, (constants.WIDTH, constants.HEIGHT))

# Botón de Play
button_play = pygame.image.load("imagenes/Play.png")  # Usa la imagen proporcionada
button_play = pygame.transform.scale(button_play, (300, 100))  # Escala la imagen
play_button = Button(780 // 2 - button_play.get_width() // 2, 500 // 2 - button_play.get_height() // 2, button_play, 1)

# Bucle de configuración
def niveles():
    run = True
    while run:
        screen.blit(Fondo, (0, 0))
        
        # Dibujar el botón de Play
        if play_button.draw(screen):
            main.main()  # Llama a la función principal del archivo main.py

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Salir con la tecla ESC
                    run = False

        pygame.display.update()  # Actualiza la pantalla

if __name__ == "__main__":
    niveles()