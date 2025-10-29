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

        # CREAR LABERINTO CON MUROS
        self.create_maze()

    def create_maze(self):
        # Limpiar muros existentes
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
        
        # BORDES CON BUCLES
        
        # Techo (y = 0)
        for x in range(0, 780, 51):  # Desde 0 hasta 780, cada 51px
            wall_positions.append((x, 0))
        
        # Piso (y = 440)  
        for x in range(0, 780, 51):
            wall_positions.append((x, 440))
        
        # Pared izquierda (x = -30)
        for y in range(0, 390, 30):  # Desde 0 hasta 390, cada 30px
            wall_positions.append((-30, y))
        
        # Pared derecha (x = 760)
        for y in range(0, 420, 30):  # Hasta 420 para cubrir más área
            wall_positions.append((760, y))
        
        # AGREGAR MUROS INTERNOS
        wall_positions.extend(internal_walls)
        
        # Crear muros en las posiciones definidas
        for x, y in wall_positions:
            self.walls.append(Wall(x, y))

    def draw(self, screen):
        # Fondo de pasto
        for y in range(0, self.height, constants.GRASS):
            for x in range(0, self.width, constants.GRASS):
                screen.blit(self.grass_image, (x, y))

        # Dibujar muros del laberinto
        for wall in self.walls:
            wall.draw(screen)