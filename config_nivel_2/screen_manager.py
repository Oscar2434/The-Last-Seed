# Pantallas de victoria y derrota
import pygame
import os

victory_img = None
defeat_img = None

def scale_screen_images(width, height):
    """Carga y escala las imágenes de pantallas"""
    global victory_img, defeat_img
    victory_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'ganar.png')).convert_alpha()
    defeat_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'perder.png')).convert_alpha()
    victory_img = pygame.transform.scale(victory_img, (width, height))
    defeat_img = pygame.transform.scale(defeat_img, (width, height))

def show_defeat_screen(screen):
    """Muestra la pantalla de derrota"""
    screen.blit(defeat_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)

def show_victory_screen(screen):
    """Muestra la pantalla de victoria"""
    screen.blit(victory_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)
