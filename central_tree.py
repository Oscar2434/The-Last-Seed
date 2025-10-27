import pygame
import constants
import os
from fire import Fire

class CentralTree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = constants.TREE_SIZE
        self.health = constants.TREE_HEALTH
        self.fires = [] 

        # Cargar sprite del árbol central
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
        # 💧 Apagar fuegos al curar
        self.fires.clear()

    def add_fire(self, big=False):
        fx = self.x + self.size // 2 - constants.FIRE_SIZE // 2 - 5
        fy = self.y + self.size - int(constants.FIRE_SIZE * 0.85)
        self.fires.append(Fire(fx, fy, big))

    def draw(self, screen):
        # Dibujar árbol
        screen.blit(self.image, (self.x, self.y))

        # Barra de vida
        bar_width = self.size
        bar_height = 8
        fill = (self.health / constants.TREE_HEALTH) * bar_width
        outline_rect = pygame.Rect(self.x, self.y - 12, bar_width, bar_height)
        fill_rect = pygame.Rect(self.x, self.y - 12, fill, bar_height)
        pygame.draw.rect(screen, constants.RED, outline_rect)
        pygame.draw.rect(screen, constants.GREEN, fill_rect)

        # Dibujar fuegos
        for fire in self.fires:
            fire.draw(screen)
