import constants
import pygame

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        
    def draw(self, screen):
        pygame.draw.rect(screen, constants.BROWN, (self.x, self.y, self.size, self.size))
