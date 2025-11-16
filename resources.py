import pygame
import constants 
import os

class Resource:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = constants.WATER_SIZE
        self.collected = False
        self.current_frame = 0
        self.animation_timer = 0
        self.total_frames = constants.WATER_FRAMES  # columnas

        
        image_path = os.path.join('assets', 'images', 'objects', 'water.png')
        self.sprite = pygame.image.load(image_path).convert_alpha()
        self.frame_size = constants.WATER_F_SIZE  # tamaño real del frame en el spritesheet

    def draw(self, screen):
        if not self.collected:
            # fila 0 = cubeta quieta
            row = 0

            current_time = pygame.time.get_ticks()
            if current_time - self.animation_timer > constants.WATER_ANIM_DELAY:
                self.animation_timer = current_time
                self.current_frame = (self.current_frame + 1) % self.total_frames

            rect = pygame.Rect(
                self.current_frame * self.frame_size,
                row * self.frame_size,
                self.frame_size,
                self.frame_size
            )
            surface = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
            surface.blit(self.sprite, (0, 0), rect)

            # Escalar al tamaño definido para pantalla
            surface = pygame.transform.scale(surface, (self.size, self.size))

            screen.blit(surface, (self.x, self.y))
