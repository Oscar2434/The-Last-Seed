import constants
import pygame
from ambient_nivel2 import Wall, Resource
from resources_nivel_2 import WaterResource  
from enemy_nivel2 import Enemy 
import os

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.trees = []
        self.central_tree = None  
        self.resources = []
        self.enemies = []  

        grass_path = os.path.join('assets', 'images', 'objects', 'grass3.png')
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_image = pygame.transform.scale(self.grass_image, (constants.GRASS, constants.GRASS))

        self.create_maze()
        self.create_resources()
       

    def set_central_tree(self, central_tree):
        
        self.central_tree = central_tree

    def create_resources(self):
      
        resource_positions = [
            (570, 50, "composta"),
            (110, 100, "agua"),      
            (610, 425, "semillas")
        ]
        
        self.resources.clear()
        for x, y, resource_type in resource_positions:
            if resource_type == "agua":
                # Usar WaterResource para el agua animada
                self.resources.append(WaterResource(x, y))
            else:
                # Usar Resource normal para los demás
                self.resources.append(Resource(x, y, resource_type))

    def create_enemies(self, difficulty="normal"):
       
        
        level2_settings = constants.LEVEL_2_SETTINGS[difficulty]
        max_enemies = level2_settings["max_enemies"]
        enemy_positions = level2_settings["enemy_positions"]
        
       
        self.enemies.clear()
        for x, y in enemy_positions:
            self.enemies.append(Enemy(x, y))

  

    def create_maze(self):
        # Limpiar muros existentes
        self.walls.clear()
        
        wall_positions = []
        
        # MUROS INTERNOS DEL LABERINTO
        internal_walls = [
            #(476, 80),
              
             (30, 220), (115, 220),  
            
        ]
        internal_walls_2 = [
            #604, 80),
            (90, 150), 
            (284, 220),
            (120, 220),(265, 220),
            (600, 90), (530, 90),

            (475, 220), (580, 220),

            (80, 302), (199, 302),
            (80, 382), (199, 382),  
            (380, 382),
            (564, 302), (604, 302),
            (564, 382), (604, 382)
        ]
        internal_walls_3 = [
            (30, 80), (100, 80),
            (570, 90), 
            (274, 220),
            (150, 302), 
            (140, 382),
            (530, 220),
            (584, 302),
            (584, 382),
            #(689, 80)
        ]
        
        # MUROS INTERNOS DEL LABERINTO
        vertical_con_final = [
            (240, 90),
            (160, 80),
            #(630, 100), 
            (520, 30), 
            (348, 250),(348, 302),
            (470, 250),(470, 302),
            
            (564, 382),
        ]
        vertical_con_final_2 = [
            (160, 232),(664, 292),
            ]
        vertical_walls_sin = [
            #(90, 80), (90, 140), (90, 200), (90, 260), (90, 320), 
        ]
        vertical_walls_sin_2 = [
            (90, 380),(90, 340),(348, 270),
        ]
        Union_wall_vertical = [
             (240, 30),
             (348, 290), (470, 280)
             #(79, 470)
            ]
        Union_wall_vertical_2 = [
             
             ]

        # AGREGAR MUROS INTERNOS
        for wall in vertical_con_final_2: 
            wall_positions.append((wall[0], wall[1], "vertical_con_final"))
        for wall in internal_walls:
            wall_positions.append((wall[0], wall[1], "horizontal_sin_final"))
        #for wall in vertical_walls_sin_2:
        #    wall_positions.append((wall[0], wall[1], "vertical_con_final"))

        for wall in internal_walls_2:
            self.walls.append(Wall(wall[0], wall[1], "horizontal_con_final", constants.WALL_SCALE))
        for wall in internal_walls_3:
            self.walls.append(Wall(wall[0], wall[1], "horizontal_sin_final", constants.WALL_SCALE))
        for wall in vertical_walls_sin:
            self.walls.append(Wall(wall[0], wall[1], "vertical_sin_final", constants.WALL_SCALE))
        for wall in Union_wall_vertical_2:
            self.walls.append(Wall(wall[0], wall[1], "vertical_sin_final", constants.WALL_SCALE))
        for wall in vertical_con_final:
            self.walls.append(Wall(wall[0], wall[1], "vertical_con_final", constants.WALL_SCALE))
        for wall in Union_wall_vertical:
            self.walls.append(Wall(wall[0], wall[1], "vertical_sin_final", constants.WALL_SCALE))

        
        for x in range(0, 780, 51):
            wall_positions.append((x, 0, "normal"))
        
        # PARED IZQUIERDA COMPLETA 
        for y in range(0, 350, 30):
            wall_positions.append((0, y, "vertical_sin_final"))
        
        # PARED DERECHA COMPLETA 
        right_wall_x = 747
        for y in range(0, 480, 30):
            wall_positions.append((right_wall_x, y, "vertical_sin_final"))
            
        # Piso  
        for x in range(0, 780, 51):
            wall_positions.append((x, 460, "normal"))
        
        # Crear muros en las posiciones definidas CON ESCALA
        for x, y, wall_type in wall_positions:
            self.walls.append(Wall(x, y, wall_type, constants.WALL_SCALE))
       
        

    def draw(self, screen):
        # Fondo de pasto
        for y in range(0, self.height, constants.GRASS):
            for x in range(0, self.width, constants.GRASS):
                screen.blit(self.grass_image, (x, y))

        # Dibujar muros del laberinto
        for wall in self.walls:
            wall.draw(screen)
        
        # Dibujar recursos (se dibujan desde nivel_2.py para mejor control)