import pygame
import sys
import constants
from button import Button
import config
import main
import os

pygame.init()

cambio= True # false = Eli, true = nino
# ventana
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
if config.lenguaje:
    pygame.display.set_caption("Configuration")
else:
    pygame.display.set_caption("Configuración")

# imágenes
Fondo = pygame.image.load("imagenes/portada.png")  # Cambia el nombre si es necesario
Fondo = pygame.transform.scale(Fondo, (constants.WIDTH, constants.HEIGHT))

# Bucle de configuración
def config_menu():
    global cambio  # Permitir modificar la variable global
    run = True
    while run:
        if config.lenguaje:
            button_next_img = pygame.image.load("assets/images/effects/nivel 1.png") # imagen next si esta en ingles
        else:
            button_next_img = pygame.image.load("assets/images/effects/nivel 1.png") # imagen next si esta en español
        if cambio:
            button_cambio_img = pygame.image.load("imagenes/Exit.png")  # Cambia la imagen si es necesario
        else:
            button_cambio_img = pygame.image.load("imagenes/Salida.png")  # Cambia la imagen si es necesario
        
        # escalado de imagenes
        button_next_img = pygame.transform.scale(button_next_img, (200, 100))  # Escalar la imagen
        button_cambio_img = pygame.transform.scale(button_cambio_img, (200, 100))  # Escalar la imagen

        # Crear el botón de cambio
        button_cambio = Button(
            constants.WIDTH // 2 - button_cambio_img.get_width() // 2,
            constants.HEIGHT // 2 - button_cambio_img.get_height() // 2,
            button_cambio_img, 1
        )
        # Coloca el botón "next" relativo al centro y debajo del botón de cambio
        nx = constants.WIDTH // 2 - button_next_img.get_width() // 2
        ny = constants.HEIGHT // 2 + button_cambio_img.get_height() // 2 + 20
        button_next = Button(nx, ny, button_next_img, 1)
        # (opcional) depuración:
        # print("next rect:", button_next.rect)

        screen.blit(Fondo, (0, 0))

        # Dibujar el botón y cambiar el cambio al presionarlo
        if button_cambio.draw(screen):
            cambio = not cambio  # Alternar entre True y False            import pygame
            import os
            
            class CharacterManager:
                def __init__(self):
                    self.characters = {
                        "nino": {
                            "sprite": os.path.join('assets', 'images', 'character', 'nino.png'),
                            "speed": 5,
                            "size": 64
                        },
                        "eli": {
                            "sprite": os.path.join('assets', 'images', 'character', 'Eli.png'),
                            "speed": 5,
                            "size": 64
                        }
                    }
                    self.current_character = "nino"
                
                def switch_character(self):
                    self.current_character = "eli" if self.current_character == "nino" else "nino"
                    
                def get_current_sprite(self):
                    return self.characters[self.current_character]["sprite"]
            
        if button_next.draw(screen):
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
    config_menu()