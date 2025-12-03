import pygame
import constants
import os
import desarrollador

class Fire:
    def __init__(self, x, y, big=False):
        self.x = x
        self.y = y
        self.big = big
        self.frame_size = constants.FIRE_F_SIZE
        self.current_frame = 0
        self.animation_timer = 0
        self.total_frames = constants.FIRE_FRAMES

        image_path = os.path.join('assets', 'images', 'objects', 'fire.png')
        self.sprite = pygame.image.load(image_path).convert_alpha()

    def draw(self, screen):
        row = 1 if self.big else 0

        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > constants.FIRE_ANIM_DELAY:
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

        surface = pygame.transform.scale(surface, (constants.FIRE_SIZE, constants.FIRE_SIZE))

        screen.blit(surface, (self.x, self.y))

class FireCentral:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame_size = constants.FIRE_F_SIZE
        self.current_frame = 0
        self.animation_timer = 0
        self.total_frames = constants.FIRE_FRAMES

        image_path = os.path.join('assets', 'images', 'objects', 'fire.png')
        self.sprite = pygame.image.load(image_path).convert_alpha()

    def draw(self, screen):
        row = 1

        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > constants.FIRE_ANIM_DELAY:
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

        scaled_size = int(constants.FIRE_SIZE * desarrollador.ESCALA_FUEGO_ARBOL_CENTRAL)
        surface = pygame.transform.scale(surface, (scaled_size, scaled_size))

        screen.blit(surface, (self.x + desarrollador.OFFSET_X_FUEGO_ARBOL_CENTRAL, 
                              self.y + desarrollador.OFFSET_Y_FUEGO_ARBOL_CENTRAL))