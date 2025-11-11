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
            (250, 130, "composta"),
            (170, 260, "agua"),      # Este usará WaterResource
            (710, 425, "semillas")
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
            (115, 80), (204, 80), (476, 80),
              
             (120, 220), (156, 220), (220, 220), (284, 220)#, (358, 230)
            
        ]
        internal_walls_2 = [
            (604, 80),
            (204, 150), (476, 150), (545, 150),
            (120, 302), (209, 302), (348, 302), (412, 302), (604, 302)
        ]
        internal_walls_3 = [
            (150, 302), (360, 302), (540, 80), (530, 150), (689, 80)
        ]
        
        # MUROS (de izquierda a derecha) INTERNOS DEL LABERINTO
        vertical_con_final = [
            (290, 80), (455, 80), 
            (350, 220)
        ]
        vertical_walls_sin = [
            (90, 80), (90, 140), (90, 200), (90, 260), (90, 320), (90, 340)
        ]
        vertical_walls_sin_2 = [
            (90, 380)
        ]

        # AGREGAR MUROS INTERNOS
        for wall in vertical_walls_sin_2:
            wall_positions.append((wall[0], wall[1], "vertical_con_final"))
        for wall in internal_walls:
            wall_positions.append((wall[0], wall[1], "horizontal_sin_final"))

        for wall in internal_walls_2:
            self.walls.append(Wall(wall[0], wall[1], "horizontal_con_final", constants.WALL_SCALE))
        for wall in internal_walls_3:
            self.walls.append(Wall(wall[0], wall[1], "horizontal_sin_final", constants.WALL_SCALE))
        for wall in vertical_walls_sin:
            self.walls.append(Wall(wall[0], wall[1], "vertical_sin_final", constants.WALL_SCALE))
        
        #------Inicio-------
        # Techo (y = 0) - línea horizontal superior
        for x in range(0, 780, 51):
            wall_positions.append((x, 0, "normal"))
        
        # PARED IZQUIERDA COMPLETA (x = 0) - desde techo hasta piso
        for y in range(0, 350, 30):
            wall_positions.append((0, y, "vertical_sin_final"))
        
        # PARED DERECHA COMPLETA - desde techo hasta piso
        right_wall_x = 747
        for y in range(0, 480, 30):
            wall_positions.append((right_wall_x, y, "vertical_sin_final"))
            
        # Piso (y = 440) - línea horizontal inferior  
        for x in range(0, 780, 51):
            wall_positions.append((x, 460, "normal"))
        #--------fin de muros--------#
        
        
        
        # Crear muros en las posiciones definidas CON ESCALA
        for x, y, wall_type in wall_positions:
            self.walls.append(Wall(x, y, wall_type, constants.WALL_SCALE))
        for wall in vertical_con_final:
            self.walls.append(Wall(wall[0], wall[1], "vertical_con_final", constants.WALL_SCALE))


        

    def draw(self, screen):
        # Fondo de pasto
        for y in range(0, self.height, constants.GRASS):
            for x in range(0, self.width, constants.GRASS):
                screen.blit(self.grass_image, (x, y))

        # Dibujar muros del laberinto
        for wall in self.walls:
            wall.draw(screen)
        
        # Dibujar recursos (se dibujan desde nivel_2.py para mejor control)