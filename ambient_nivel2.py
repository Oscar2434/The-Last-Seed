import constants
import pygame
import os
class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        tree_path = os.path.join('assets', 'images', 'objects', 'tree.png')
        self.image = pygame.image.load(tree_path).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (50, 30))  
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

        bush_path = os.path.join('assets', 'images', 'objects', 'bush.png')
        self.image = pygame.image.load(bush_path).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (40, 20))  
        self.size = self.image.get_width()

    def draw(self, screen):
       screen.blit(self.image, (self.x, self.y))

class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        wall_path = os.path.join('assets', 'images', 'objects', 'lave.png')
        self.image = pygame.image.load(wall_path).convert_alpha() 
        # ⬇️ USAR EL TAMAÑO REAL SIN ESCALAR ⬇️
        # self.image = pygame.transform.scale(self.image, (64, 51))  # QUITA ESTA LÍNEA
        self.size = self.image.get_width()  # Esto será el tamaño real

    def draw(self, screen):
       screen.blit(self.image, (self.x, self.y))      