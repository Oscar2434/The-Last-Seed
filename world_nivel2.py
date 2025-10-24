import constants
import pygame
from ambient_nivel2 import Wall
import os

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []  # Lista para los muros del laberinto
        self.trees = []  # IMPORTANTE: Mantener esta lista (aunque vacía)
        self.central_tree = None  # También mantener este atributo

        grass_path = os.path.join('assets', 'images', 'objects', 'grass3.png')
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_image = pygame.transform.scale(self.grass_image, (constants.GRASS, constants.GRASS))

        # CREAR LABERINTO CON MUROS - coordenadas por definir
        self.create_maze()

    def create_maze(self):
        # Aquí vamos a crear el diseño del laberinto con muros
        # Por ahora vacío - lo implementaremos después
        pass

    def draw(self, screen):
        # Fondo de pasto
        for y in range(0, self.height, constants.GRASS):
            for x in range(0, self.width, constants.GRASS):
                screen.blit(self.grass_image, (x, y))

        # Dibujar muros del laberinto
        for wall in self.walls:
            wall.draw(screen)