import pygame
import sys
import constants
from button import Button

pygame.init()

lenguaje = True  # false = español, true = ingles
music = False  # false = sin música, true = con música
cambio= False
# ventana
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
if lenguaje:
    pygame.display.set_caption("Configuration")
else:
    pygame.display.set_caption("Configuración")

# imágenes
Fondo = pygame.image.load("imagenes/portada.png")  # Cambia el nombre si es necesario
Fondo = pygame.transform.scale(Fondo, (constants.WIDTH, constants.HEIGHT))

# Bucle de configuración
def config_menu():
    global lenguaje  # Permitir modificar la variable global
    run = True
    while run:
        if lenguaje:
            button_lenguaje_img = pygame.image.load("imagenes/Exit.png")  # Cambia la imagen si es necesario
        else:
            button_lenguaje_img = pygame.image.load("imagenes/Salida.png")  # Cambia la imagen si es necesario
        
        button_lenguaje_img = pygame.transform.scale(button_lenguaje_img, (200, 100))  # Escalar la imagen
        # Crear el botón de lenguaje
        button_lenguaje = Button(constants.WIDTH // 2 - button_lenguaje_img.get_width() // 2, constants.HEIGHT // 2 - button_lenguaje_img.get_height() // 2, button_lenguaje_img, 1)

        screen.blit(Fondo, (0, 0))

        # Dibujar el botón y cambiar el lenguaje al presionarlo
        if button_lenguaje.draw(screen):
            lenguaje = not lenguaje  # Alternar entre True y False
            

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