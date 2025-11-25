import pygame
import sys
import constants
from button import Button
import main
import config
import nivels

pygame.init()  

# Variables globales para control de música
music_initialized = False

def initialize_music():
    """Inicializa el sistema de música una sola vez"""
    global music_initialized
    if not music_initialized and config.music:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        try:
            pygame.mixer.music.load('music/m4.mp3')
            pygame.mixer.music.set_volume(config.volume_master)
            pygame.mixer.music.play(-1)
            music_initialized = True
        except pygame.error as e:
            print(f"Error cargando música: {e}")
            music_initialized = False

def apply_current_config():
    """Aplica la configuración actual cargada sin reiniciar la música"""
    config.update_global_config()  # Actualizar variables globales
    
    # Actualizar volumen si la música está reproduciéndose
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.set_volume(config.volume_master)
    
    # Manejar estado de música (play/stop)
    if config.music:
        if not pygame.mixer.music.get_busy():
            initialize_music()
    else:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

# Aplicar configuración al inicio
config.update_global_config()
initialize_music()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("The Last Seed")

Fondo = pygame.image.load("imagenes/portada.png")
button_config = pygame.image.load("imagenes/confi.png")
title_img = pygame.image.load("imagenes/titulo1.png").convert_alpha()

Fondo = pygame.transform.scale(Fondo, (constants.WIDTH, constants.HEIGHT))
button_config = pygame.transform.scale(button_config, (120, 100))

title_img = pygame.transform.scale(
    title_img,
    (
        int(title_img.get_width() * 0.90),
        int(title_img.get_height() * 0.90)
    )
)

title_rect = title_img.get_rect(center=(constants.WIDTH // 2, 250))

config_button = Button(
    150 // 2 - button_config.get_width() // 2,
    800 // 2 - button_config.get_height() // 2,
    button_config, 1
)

def menu():
    run = True
    while run:
        # ACTUALIZAR CONFIGURACIÓN EN CADA ITERACIÓN
        config.update_global_config()
        
        # Cargar imágenes según idioma ACTUAL
        if config.lenguaje:  # Español
            play_normal = pygame.image.load("imagenes/Jugar.png")
            play_hover  = pygame.image.load("imagenes/JugarR.png")
            exit_normal = pygame.image.load("imagenes/SalidaR.png")
        else:  # Inglés
            play_normal = pygame.image.load("imagenes/PlayR.png")
            play_hover  = pygame.image.load("imagenes/Play.png")
            exit_normal = pygame.image.load("imagenes/Exit.png")

        play_normal = pygame.transform.scale(play_normal, (300, 100))
        play_hover  = pygame.transform.scale(play_hover,  (300, 100))
        exit_normal = pygame.transform.scale(exit_normal, (200, 100))

        play_rect = play_normal.get_rect(center=(constants.WIDTH // 2, 500 // 2))
        exit_rect = exit_normal.get_rect(center=(constants.WIDTH // 2, 800 // 2))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        screen.blit(Fondo, (0, 0))
        screen.blit(title_img, title_rect)

        if play_rect.collidepoint(mouse):
            screen.blit(play_hover, play_rect)
            if click:
                pygame.time.delay(150)
                nivels.niveles()

        else:
            screen.blit(play_normal, play_rect)

        if config_button.draw(screen):
            config.open_config_menu(from_menu="main")
            # Después de regresar de configuración, actualizar música
            apply_current_config()

        if exit_rect.collidepoint(mouse):
            screen.blit(exit_normal, exit_rect)
            if click:
                config.save_current_config()  # Guardar antes de salir
                pygame.quit()
                sys.exit()
        else:
            screen.blit(exit_normal, exit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.save_current_config()  # Guardar antes de salir
                pygame.quit()
                sys.exit()

            if event.type == config.OPEN_MENU_EVENT:
                # Este evento nos trae de vuelta al menú principal
                apply_current_config()  # Actualizar configuración
                continue

        pygame.display.update()

def main_loop():
    main.main()

if __name__ == "__main__":
    menu()