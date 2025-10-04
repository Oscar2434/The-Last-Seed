import pygame
import constants
import os

class Resource:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.collected = False

        #Cargar sprite del recurso de curación
        image_path = os.path.join('assets', 'images', 'objects', 'seed.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, (self.x, self.y))
