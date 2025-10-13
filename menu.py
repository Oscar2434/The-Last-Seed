import pygame
import sys
import constants
from button import Button
import main
import config
import nivels

pygame.init() #Inicializar pygame

if config.music: #Reproducir las instruciones para que se reprodusca la musica del juego si la variable music que se encuentra en config es true que es verdadero
    pygame.mixer.init()
    pygame.mixer.music.load('music/prueba1.mp3')  #Ruta al archivo de música
    pygame.mixer.music.play(-1)#Reproducir la música

#ventana
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("The Last Seed")

#imágenes
Fondo = pygame.image.load("imagenes\portada.png")
button_config = pygame.image.load("imagenes\confi.png")

if config.lenguaje: # si la variable lenguaje que se encuentra en config es true que es verdadero cargara las imagenes en ingles
    button_play = pygame.image.load("imagenes\Play.png")
    button_exit = pygame.image.load("imagenes\Exit.png")
else: # si la variable lenguaje es false que es falso cargara las imagenes en español
    button_play = pygame.image.load("imagenes\Jugar.png")
    button_exit = pygame.image.load("imagenes\Salida.png")

#escalar imágenes
Fondo = pygame.transform.scale(Fondo, (constants.WIDTH, constants.HEIGHT))
button_play = pygame.transform.scale(button_play, ( 300, 100))
button_config = pygame.transform.scale(button_config, ( 120, 100))
button_exit = pygame.transform.scale(button_exit, ( 200, 100))

#botones 
    #play
play_button = Button( 780 // 2 - button_play.get_width() // 2, 500 // 2 - button_play.get_height() // 2, button_play, 1)
    #config
config_button = Button( 150 // 2 - button_config.get_width() // 2, 800 // 2 - button_config.get_height() // 2, button_config, 1)
    #salir
exit_button = Button( 780 // 2 - button_exit.get_width() // 2, 800// 2 - button_exit.get_height() // 2, button_exit, 1)

#Bucle
def menu():
    run = True
    while run:
        screen.blit(Fondo, (0, 0))
        
        if play_button.draw(screen):
            nivels.niveles()  # llama el menu de niveles
            
        if config_button.draw(screen):
            config.config_menu()  # llama al menú de configuración

        if exit_button.draw(screen):
            pygame.quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()  # actualiza la pantalla

def main_loop():
    main.main()

if __name__ == "__main__":
    menu()