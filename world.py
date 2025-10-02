import constants
import pygame
from ambient import Tree, Rock, Bush
import random
import os
import math

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.trees = []
        self.rock = []
        self.central_tree = None  # se asigna después en main

        grass_path = os.path.join('assets', 'images', 'objects', 'grass3.png')
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_image = pygame.transform.scale(self.grass_image, (constants.GRASS, constants.GRASS))

        # generar árboles con distribución controlada
        self.generate_trees(num_trees=10, min_distance=70)

    def generate_trees(self, num_trees=10, min_distance=70):
        """Genera árboles secundarios evitando colisiones y el árbol central"""
        attempts = 0
        while len(self.trees) < num_trees and attempts < num_trees * 20:
            attempts += 1
            x = random.randint(0, self.width - constants.TREES)
            y = random.randint(0, self.height - constants.TREES)
            new_tree = Tree(x, y)

            # evitar cercanía con el árbol central
            if self.central_tree:
                dx = (new_tree.x + new_tree.size//2) - (self.central_tree.x + self.central_tree.size//2)
                dy = (new_tree.y + new_tree.size//2) - (self.central_tree.y + self.central_tree.size//2)
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < (self.central_tree.size//2 + min_distance):
                    continue  # muy cerca del árbol central

            # evitar colisión con otros árboles secundarios
            overlap = False
            for tree in self.trees:
                dx = (new_tree.x + new_tree.size//2) - (tree.x + tree.size//2)
                dy = (new_tree.y + new_tree.size//2) - (tree.y + tree.size//2)
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < min_distance:
                    overlap = True
                    break

            if not overlap:
                self.trees.append(new_tree)

        # generar rocas (sin control estricto, pero puedes aplicar la misma lógica si quieres)
        self.rock = [
            Rock(random.randint(0, self.width-constants.ROCK),
                 random.randint(0, self.height-constants.ROCK))
            for _ in range(20)
        ]

    def draw(self, screen):
        # fondo de pasto
        for y in range(0, self.height, constants.GRASS):
            for x in range(0, self.width, constants.GRASS):
                screen.blit(self.grass_image, (x, y))

        # dibujar objetos
        for tree in self.trees:
            tree.draw(screen)
        for rock in self.rock:
            rock.draw(screen)
