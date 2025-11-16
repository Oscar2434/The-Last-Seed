import pygame
import sys
import os

# === CORRECCIÓN DE IMPORTS ===
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import constants 
# === FIN DE CORRECCIÓN ===

class WaterResource:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = "agua"
        self.size = 50
        self.collected = False
        self.current_frame = 0
        self.animation_timer = 0
        self.total_frames = 10
        self.row = 0

        # Cargar spritesheet del cubo de agua
        image_path = os.path.join('assets', 'images', 'Items', 'agua.png')
        try:
            self.sprite = pygame.image.load(image_path).convert_alpha()
            self.frame_size = self.sprite.get_width() // self.total_frames
        except:
            self.sprite = None
            self.frame_size = self.size
        
        # Rectángulo de colisión AGREGADO
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen):
        if not self.collected:
            if self.sprite:
                current_time = pygame.time.get_ticks()
                if current_time - self.animation_timer > 100:
                    self.animation_timer = current_time
                    self.current_frame = (self.current_frame + 1) % self.total_frames

                rect = pygame.Rect(
                    self.current_frame * self.frame_size,
                    self.row * self.frame_size,
                    self.frame_size,
                    self.frame_size
                )
                
                frame_surface = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
                frame_surface.blit(self.sprite, (0, 0), rect)
                
                frame_surface = pygame.transform.scale(frame_surface, (self.size, self.size))
                screen.blit(frame_surface, (self.x, self.y))
            else:
                placeholder = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (0, 100, 255), (0, 0, self.size, self.size))
                screen.blit(placeholder, (self.x, self.y))
            
            # Actualizar posición del rectángulo AGREGADO
            self.rect.x = self.x
            self.rect.y = self.y
    
    # Método para colisiones AGREGADO
    def get_rect(self):
        return self.rect

    def get_dialog_text(self):
        return "¡Perfecto! ¡El agua es importante para las plantas y transporta sus \nnutrientes por toda la planta!"