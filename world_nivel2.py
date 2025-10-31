import constants
import pygame
from ambient_nivel2 import Wall, Resource
import os

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.trees = []
        self.central_tree = None
        self.resources = []

        grass_path = os.path.join('assets', 'images', 'objects', 'grass3.png')
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_image = pygame.transform.scale(self.grass_image, (constants.GRASS, constants.GRASS))

        self.create_maze()
        self.create_resources()

    def create_resources(self):
        # POSICIONES FIJAS para los 3 recursos en el laberinto
        resource_positions = [
            (150, 150, "composta"),
            (400, 300, "agua"),
            (600, 200, "semillas")
        ]
        
        self.resources.clear()
        for x, y, resource_type in resource_positions:
            self.resources.append(Resource(x, y, resource_type))

    def create_maze(self):
        # ... (código existente igual) ...
        self.walls.clear()
        
        wall_positions = []
        
        # MUROS INTERNOS DEL LABERINTO
        internal_walls = [
            (102, 110), (166, 110), (230, 110), (614, 110), (550, 110), (486, 110),
            (102, 230), (102, 190), (230, 190), (102, 270), (166, 270), (230, 270), 
            (294, 270), (358, 270), (102, 310), (358, 310), (102, 350), (166, 350), 
            (230, 350), (358, 350), (422, 350), (486, 190), (550, 190), (614, 350),
            (102, 390)
        ]
        
        # BORDES CON BUCLES - PAREDES COMPLETAS
        
        # Techo (y = 0) - línea horizontal superior
        for x in range(0, 780, 51):
            wall_positions.append((x, 0, "normal"))
        
        # PARED IZQUIERDA COMPLETA (x = 0) - desde techo hasta piso
        for y in range(0, 350, 30):
            wall_positions.append((0, y, "left"))
        
        # PARED DERECHA COMPLETA - desde techo hasta piso
        right_wall_x = 747
        for y in range(0, 480, 30):
            wall_positions.append((right_wall_x, y, "right"))
        
        # Piso (y = 440) - línea horizontal inferior  
        for x in range(0, 780, 51):
            wall_positions.append((x, 440, "normal"))
        
        # AGREGAR MUROS INTERNOS
        for wall in internal_walls:
            wall_positions.append((wall[0], wall[1], "normal"))
        
        # Crear muros en las posiciones definidas
        for x, y, wall_type in wall_positions:
            self.walls.append(Wall(x, y, wall_type))

    def draw(self, screen):
        # Fondo de pasto
        for y in range(0, self.height, constants.GRASS):
            for x in range(0, self.width, constants.GRASS):
                screen.blit(self.grass_image, (x, y))

        # Dibujar muros del laberinto
        for wall in self.walls:
            wall.draw(screen)
        
        # Dibujar recursos (se dibujan desde nivel_2.py para mejor control)