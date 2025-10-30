import pygame
import sys
import config
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

# imagen que depende el idioma del juego para los botones
if config.lenguaje:
    button_nivel_1 = pygame.image.load("assets/images/effects/nivel 1.png")  # Usa la imagen proporcionada
    button_nivel_2 = pygame.image.load("assets/images/effects/nivel 2.png")  # Usa la imagen proporcionada
else:
    button_nivel_1 = pygame.image.load("assets/images/effects/nivel 1.png")  # Usa la imagen proporcionada
    button_nivel_2 = pygame.image.load("assets/images/effects/nivel 2.png")  # Usa la imagen proporcionada
# botones de niveles
button_nivel_1 = pygame.transform.scale(button_nivel_1, (161, 80))  # Escala la imagen
button_nivel_1 = Button(200 - button_nivel_1.get_width() // 2, 200 - button_nivel_1.get_height() // 2, button_nivel_1, 1)
button_nivel_2 = pygame.transform.scale(button_nivel_2, (322, 161))  # Escala la imagen
button_nivel_2 = Button(1080 // 2 - button_nivel_2.get_width() // 2, 700 // 2 - button_nivel_2.get_height() // 2, button_nivel_2, 1)

# Bucle de configuración
def niveles():
    run = True
    while run:
        screen.blit(Fondo, (0, 0))
        
        # Dibujar el botón de Play
        if button_nivel_1.draw(screen):
            main.main()  # Llama a la función principal del archivo main.py
        
        if button_nivel_2.draw(screen):
            import nivel_2
            nivel_2.main()  # Llama a la función principal del archivo nivel_2.py
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