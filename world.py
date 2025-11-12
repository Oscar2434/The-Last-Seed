import constants
import pygame
from ambient import Tree, Rock
import random
import os

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.trees = []
        self.rocks = []
        self.central_tree = None
        self.enemy_slots = []
        self.next_slot = 0

        grass_path = os.path.join('assets', 'images', 'objects', 'grass3.png')
        self.grass_image = pygame.image.load(grass_path).convert()
        self.grass_image = pygame.transform.scale(self.grass_image, (constants.GRASS, constants.GRASS))

        self.generate_trees()
        self.generate_rocks(num_rocks=15)

    def generate_trees(self):
        positions = [
            (200, 120),
            (200, 300),
            (500, 150),
            (600, 350),
            (300, 400)
        ]
        for (x, y) in positions:
            self.trees.append(Tree(x, y))

    def is_area_free(self, x, y, size):
        new_rect = pygame.Rect(x, y, size, size)

        for tree in self.trees:
            tree_rect = pygame.Rect(tree.x, tree.y, tree.size, tree.size)
            if new_rect.colliderect(tree_rect):
                return False

        if self.central_tree:
            central_rect = pygame.Rect(self.central_tree.x, self.central_tree.y,
                                       self.central_tree.size, self.central_tree.size)
            if new_rect.colliderect(central_rect):
                return False

        return True

    def generate_rocks(self, num_rocks=15):
        for _ in range(num_rocks * 3):
            rx = random.randint(0, self.width - constants.ROCK)
            ry = random.randint(0, self.height - constants.ROCK)
            if self.is_area_free(rx, ry, constants.ROCK):
                self.rocks.append(Rock(rx, ry))
            if len(self.rocks) >= num_rocks:
                break

    def setup_enemy_slots(self, enemy_size):
        if not self.central_tree:
            return
        self.enemy_slots.clear()
        self.next_slot = 0

        cy = self.central_tree.y
        h = self.central_tree.size

        step = max(1, enemy_size - 6)
        top = cy
        bottom = cy + h - enemy_size

        ys = []
        y = top
        while y <= bottom:
            ys.append(y)
            y += step

        left_x = self.central_tree.x - enemy_size - 10
        right_x = self.central_tree.x + self.central_tree.size + 10

        toggle = True
        for yv in ys:
            if toggle:
                self.enemy_slots.append((left_x, yv))
                self.enemy_slots.append((right_x, yv))
            else:
                self.enemy_slots.append((right_x, yv))
                self.enemy_slots.append((left_x, yv))
            toggle = not toggle

    def get_next_enemy_slot(self):
        if not self.enemy_slots:
            return None
        slot = self.enemy_slots[self.next_slot % len(self.enemy_slots)]
        self.next_slot += 1
        return slot

    def draw(self, screen):
        for y in range(0, self.height, constants.GRASS):
            for x in range(0, self.width, constants.GRASS):
                screen.blit(self.grass_image, (x, y))

        for tree in self.trees:
            tree.draw(screen)
        for rock in self.rocks:
            rock.draw(screen)

