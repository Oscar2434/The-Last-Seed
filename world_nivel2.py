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
            (0, 0), (100, 0), (200, 0), (300, 0), (400, 0), (500, 0), (600, 0), (700, 0),  # Techo
            # ⬇️ QUITAR MURO INFERIOR o dejarlo más arriba para dejar espacio para spawn
            (0, 400), (100, 400), (200, 400), (300, 400), (400, 400), (500, 400), (600, 400), (700, 400),  # Piso más arriba
            (0, 0), (0, 30), (0, 60), (0, 90), (0, 120), (0, 150), (0, 180), (0, 210), (0, 240), (0, 270), (0, 300), (0, 330), (0, 360),  # Pared izquierda (más corta)
            (760, 0), (760, 30), (760, 60), (760, 90), (760, 120), (760, 150), (760, 180), (760, 210), (760, 240), (760, 270), (760, 300), (760, 330), (760, 360),  # Pared derecha (más corta)
            
            # Algunos muros internos para formar pasillos (evitar área de spawn)
            (200, 100), (300, 100), (400, 100),
            (100, 200), (200, 200), (300, 200),
            (500, 300), (600, 300),
            # ⬇️ QUITAR muros cerca del área de spawn inferior
            # (200, 400), (300, 400), (400, 400),  # Estos bloqueaban el spawn
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
            
            # ⬇️ DEBUG: Dibujar rectángulo de colisión en ROJO ⬇️
            debug_rect = pygame.Rect(
                wall.x, 
                wall.y, 
                wall.size * 0.7,  # Lo mismo que usa check_collision
                wall.size * 0.7
            )
            pygame.draw.rect(screen, (255, 0, 0), debug_rect, 2)  # Rojo, línea de 2px