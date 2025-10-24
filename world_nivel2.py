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
        self.walls = []  # Nueva lista para los muros
        self.central_tree = None  

        grass_path = os.path.join('assets', 'images', 'objects', 'grass3.png')
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_image = pygame.transform.scale(self.grass_image, (constants.GRASS, constants.GRASS))


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
        for wall in self.walls:  # Dibujar los muros
            wall.draw(screen)