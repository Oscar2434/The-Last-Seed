import constants
import pygame
import os
from fire import Fire

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = constants.TREE_HEALTH
        self.max_health = constants.TREE_HEALTH
        self.fires = []
        self.frame_size = 64
        self.current_frame = 0
        self.animation_timer = 0
        self.total_frames = 5
        self.size = constants.TREE_MEDIUM
        self.sprite = pygame.image.load(os.path.join('assets', 'images', 'objects', 'arbolquemado.png')).convert_alpha()

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        if self.health == 0:
            self.add_fire(big=True)

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        self.fires.clear()

    def add_fire(self, big=False):
        fx = self.x + self.size // 2 - constants.FIRE_SIZE // 2 - 3
        fy = self.y + self.size - int(constants.FIRE_SIZE * 0.75)
        self.fires.append(Fire(fx, fy, big))

    def draw(self, screen):
        ratio = self.health / self.max_health if self.max_health > 0 else 0
        if ratio > 0.95:
            row = 0
        elif ratio > 0.75:
            row = 1
        elif ratio > 0.55:
            row = 2
        elif ratio > 0.35:
            row = 3
        else:
            row = 4
        current_time = pygame.time.get_ticks()
        if self.health > 0 and current_time - self.animation_timer > constants.WATER_ANIM_DELAY:
            self.animation_timer = current_time
            self.current_frame = (self.current_frame + 1) % self.total_frames
        rect = pygame.Rect(self.current_frame * self.frame_size, row * self.frame_size, self.frame_size, self.frame_size)
        surface = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
        surface.blit(self.sprite, (0, 0), rect)
        surface = pygame.transform.scale(surface, (self.size, self.size))
        screen.blit(surface, (self.x, self.y))
        for fire in self.fires:
            fire.draw(screen)

class CentralTree(Tree):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = constants.TREE_HEALTH
        self.max_health = constants.TREE_HEALTH
        self.size = constants.TREE_SIZE
        self.sprite = pygame.image.load(os.path.join('assets', 'images', 'objects', 'arbolquemado.png')).convert_alpha()

class Rock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        rock_path = os.path.join('assets', 'images', 'objects', 'rock.png')
        self.image = pygame.image.load(rock_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.ROCK, constants.ROCK))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
