import sys
import os

# === CORRECCIÓN DE IMPORTS ===
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import constants
import pygame
from nivel_2.ambient import Wall, Resource
from nivel_2.resources import WaterResource  
from nivel_2.enemy import Enemy 
# === FIN DE CORRECCIÓN ===

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
                self.resources.append(WaterResource(x, y))
            else:
                self.resources.append(Resource(x, y, resource_type))

    def create_enemies(self, difficulty="normal"):
        level2_settings = constants.LEVEL_2_SETTINGS[difficulty]
        max_enemies = level2_settings["max_enemies"]
        enemy_positions = level2_settings["enemy_positions"]
        
        self.enemies.clear()
        for x, y in enemy_positions:
            self.enemies.append(Enemy(x, y))

    def create_maze(self):
        self.walls.clear()
        
        wall_positions = []
        
        internal_walls = [
            (30, 220), (115, 220),  
        ]
        internal_walls_2 = [
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
        ]
        
        vertical_con_final = [
            (240, 90),
            (160, 80),
            (520, 30), 
            (348, 250),(348, 302),
            (470, 250),(470, 302),
            (564, 382),
        ]
        vertical_con_final_2 = [
            (160, 232),(664, 292),
        ]
        vertical_walls_sin = [
        ]
        vertical_walls_sin_2 = [
            (90, 380),(90, 340),(348, 270),
        ]
        Union_wall_vertical = [
             (240, 30),
             (348, 290), (470, 280)
            ]
        Union_wall_vertical_2 = [
        ]

        for wall in vertical_con_final_2: 
            wall_positions.append((wall[0], wall[1], "vertical_con_final"))
        for wall in internal_walls:
            wall_positions.append((wall[0], wall[1], "horizontal_sin_final"))

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
        
        for y in range(0, 350, 30):
            wall_positions.append((0, y, "vertical_sin_final"))
        
        right_wall_x = 747
        for y in range(0, 480, 30):
            wall_positions.append((right_wall_x, y, "vertical_sin_final"))
            
        for x in range(0, 780, 51):
            wall_positions.append((x, 460, "normal"))
        
        for x, y, wall_type in wall_positions:
            self.walls.append(Wall(x, y, wall_type, constants.WALL_SCALE))
       
    def draw(self, screen):
        for y in range(0, self.height, constants.GRASS):
            for x in range(0, self.width, constants.GRASS):
                screen.blit(self.grass_image, (x, y))

        for wall in self.walls:
            wall.draw(screen)