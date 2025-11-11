import constants
import pygame
from ambient_nivel2 import Wall, Resource
from resources_nivel_2 import WaterResource  # Importar la nueva clase
import os

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.trees = []
        self.central_tree = None  # Inicializar como None
        self.resources = []

        grass_path = os.path.join('assets', 'images', 'objects', 'grass3.png')
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_image = pygame.transform.scale(self.grass_image, (constants.GRASS, constants.GRASS))

        self.create_maze()
        self.create_resources()

    def set_central_tree(self, central_tree):
        """Método para establecer el árbol central desde nivel_2.py"""
        self.central_tree = central_tree

    def create_resources(self):
        # POSICIONES FIJAS para los 3 recursos en el laberinto
        resource_positions = [
            (250, 160, "composta"),
            (170, 300, "agua"),      # Este usará WaterResource
            (500, 160, "semillas")
        ]
        
        self.resources.clear()
        for x, y, resource_type in resource_positions:
            if resource_type == "agua":
                # Usar WaterResource para el agua animada
                self.resources.append(WaterResource(x, y))
            else:
                # Usar Resource normal para los demás
                self.resources.append(Resource(x, y, resource_type))

    def create_maze(self):
        # Limpiar muros existentes
        self.walls.clear()
        
        wall_positions = []
        
        # MUROS INTERNOS DEL LABERINTO
        internal_walls = [
            (125, 130), (214, 130), (614, 130), (550, 130), (486, 130),
            (214, 190), (486, 190), (550, 190),  
            (294, 270), (358, 270), (130, 270), (166, 270), (230, 270),
            (130, 350), (219, 350), (358, 350), (422, 350), (614, 350)
        ]
        
        # MUROS (de izquierda a derecha) INTERNOS DEL LABERINTO
        internal_walls_left = [
            (300, 110), (465, 110), (430, 270)
        ]
        internal_walls_right = [
            (100, 120), (100, 180), (100, 240), (100, 300), (100, 360), (100, 420)
        ]
        internal_walls_fin = [
            (150, 161)
        ]
        internal_walls_inicio = [
            (150, 120)
        ]

        # BORDES CON BUCLES - PAREDES COMPLETAS
        # AGREGAR MUROS INTERNOS
        for wall in internal_walls:
            wall_positions.append((wall[0], wall[1], "normal"))
            
        # Techo (y = 0) - línea horizontal superior
        for x in range(0, 780, 51):
            wall_positions.append((x, 0, "normal"))
        
        # PARED IZQUIERDA COMPLETA (x = 0) - desde techo hasta piso
        for y in range(0, 350, 30):
            wall_positions.append((0, y, "left"))
        
        # PARED DERECHA COMPLETA - desde techo hasta piso
        right_wall_x = 747
        for y in range(0, 480, 30):
            wall_positions.append((right_wall_x, y, "left"))
            
        
        for wall in internal_walls_right:
            self.walls.append(Wall(wall[0], wall[1], "left", constants.WALL_SCALE))

        # Piso (y = 440) - línea horizontal inferior  
        for x in range(0, 780, 51):
            wall_positions.append((x, 460, "normal"))
        
        
        
        # Crear muros en las posiciones definidas CON ESCALA
        for x, y, wall_type in wall_positions:
            self.walls.append(Wall(x, y, wall_type, constants.WALL_SCALE))




        
        for wall in internal_walls_left:
            self.walls.append(Wall(wall[0], wall[1], "right", constants.WALL_SCALE))

    def draw(self, screen):
        # Fondo de pasto
        for y in range(0, self.height, constants.GRASS):
            for x in range(0, self.width, constants.GRASS):
                screen.blit(self.grass_image, (x, y))

        # Dibujar muros del laberinto
        for wall in self.walls:
            wall.draw(screen)
        
        # Dibujar recursos (se dibujan desde nivel_2.py para mejor control)