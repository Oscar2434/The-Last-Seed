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
        
        # LABERINTO SIMPLIFICADO PARA 780x480 - DEJAR ESPACIO PARA SPAWN
        wall_positions = [
            # Bordes de la pantalla (dejar espacio abajo para spawn)
            (0, 0), (51, 0), (102, 0), (153, 0), (204, 0), (255, 0), (306, 0), (357, 0), (408, 0), (459, 0), (510, 0), (561, 0), (612, 0), (663, 0), (714, 0),  # Techo
            (0, 440), (51, 440), (102, 440), (153, 440), (204, 440), (255, 440), (306, 440), (357, 440), (408, 440), (459, 440), (510, 440), (561, 440), (612, 440), (663, 440), (714, 440),  # Piso más arriba
            (-30, 0), (-30, 30), (-30, 60), (-30, 90), (-30, 120), (-30, 150), (-30, 180), (-30, 210), (-30, 240), (-30, 270), (-30, 300), (-30, 330), (-30, 360),  # Pared izquierda (más corta)
            (760, 0), (760, 30), (760, 60), (760, 90), (760, 120), (760, 150), (760, 180), (760, 210), (760, 240), (760, 270), (760, 300), (760, 330), (760, 360), (760, 385)  # Pared derecha (más corta)
        ]
        
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
            
            # ⬇️ DEBUG ACTUALIZADO: Dibujar rectángulo de colisión en ROJO ⬇️
            debug_rect = pygame.Rect(
                wall.x, 
                wall.y, 
                wall.image.get_width() * 1,  # 80% del ancho visual (nuevo cálculo)
                wall.image.get_height() * 0.7   # 80% del alto visual (nuevo cálculo)
            )
            pygame.draw.rect(screen, (255, 0, 0), debug_rect, 2)  # Rojo, línea de 2px