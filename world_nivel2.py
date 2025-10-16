import constants
import pygame
from ambient_nivel2 import Tree, Rock, Bush
import random
import os
import math

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.trees = []
        self.rock = []
        self.central_tree = None  

        grass_path = os.path.join('assets', 'images', 'objects', 'grass3.png')
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_image = pygame.transform.scale(self.grass_image, (constants.GRASS, constants.GRASS))

        #generar árboles con distribución controlada
        self.generate_trees(num_trees=10, min_distance=70)

    def generate_trees(self, num_trees=10, min_distance=70):
        # Posiciones fijas para los árboles
        tree_positions = [
            (100, 100),
            (200, 150),
            (500, 300),
            (150, 400),
            (600, 100),
            (500, 200),
            (300, 350),
            (550, 300),
            (650, 400),
            (200, 50),
            (420, 35),
            (50, 250)
        ]
        
        for pos in tree_positions:
            new_tree = Tree(pos[0], pos[1])
            self.trees.append(new_tree)

        #generar rocas 
        self.rock = [
            Rock(random.randint(0, self.width-constants.ROCK),
                 random.randint(0, self.height-constants.ROCK))
            for _ in range(20)
        ]

    def draw(self, screen):
        #fondo de pasto
        for y in range(0, self.height, constants.GRASS):
            for x in range(0, self.width, constants.GRASS):
                screen.blit(self.grass_image, (x, y))

        #dibujar objetos
        for tree in self.trees:
            tree.draw(screen)
        for rock in self.rock:
            rock.draw(screen)
