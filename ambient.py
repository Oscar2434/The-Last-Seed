import constants
import pygame
import os
class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        tree_path = os.path.join('assets', 'images', 'objects', 'treedes.png')
        self.image = pygame.image.load(tree_path).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (constants.TREES, constants.TREES))  
        self.size = self.image.get_width()

    def draw(self, screen):
       screen.blit(self.image, (self.x, self.y))

class Rock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        rock_path = os.path.join('assets', 'images', 'objects', 'rock.png')
        self.image = pygame.image.load(rock_path).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (constants.ROCK, constants.ROCK))  
        self.size = self.image.get_width()

    def draw(self, screen):
       screen.blit(self.image, (self.x, self.y))

class Bush:
    def __init__(self, x, y):
        self.x = x
        self.y = y