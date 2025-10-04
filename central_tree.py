import pygame
import constants
import os

class CentralTree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 80
        self.health = constants.TREE_HEALTH

        #Cargar sprite del árbol central
        image_path = os.path.join('assets', 'images', 'objects', 'treeC.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > constants.TREE_HEALTH:
            self.health = constants.TREE_HEALTH

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

        #Barra de vida encima del árbol
        bar_width = self.size
        bar_height = 8
        fill = (self.health / constants.TREE_HEALTH) * bar_width
        outline_rect = pygame.Rect(self.x, self.y - 12, bar_width, bar_height)
        fill_rect = pygame.Rect(self.x, self.y - 12, fill, bar_height)
        pygame.draw.rect(screen, constants.RED, outline_rect)
        pygame.draw.rect(screen, constants.GREEN, fill_rect)
