import pygame
import constants
from ambient import Tree
import random

class World:
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.trees = [Tree(random.randint(0, width-40), 
                           random.randint(0, width-40)) for _ in range(10)]

    def draw(self, screen):
        screen.fill(constants.GREEN)
        for tree in self.trees:
            tree.draw(screen)