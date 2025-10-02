import pygame
import constants
import os

class Lumberjack:
    def __init__(self, x, y, target_pos):
        self.x = x
        self.y = y
        self.size = constants.LUMBERJACK_SIZE
        self.speed = constants.ENEMY_SPEED
        self.damage = constants.ENEMY_DAMAGE
        self.attack_cooldown = 60
        self.timer = 0
        self.target_pos = target_pos  # slot disperso alrededor del árbol

        image_path = os.path.join('assets', 'images', 'character', 'leñador.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def move_towards(self, tree):
        
        enemy_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        tree_rect = pygame.Rect(tree.x, tree.y, tree.size, tree.size)

        if enemy_rect.colliderect(tree_rect):
            return  # ya en contacto con el árbol

        tx, ty = self.target_pos

        if self.x < tx:
            self.x += self.speed
        elif self.x > tx:
            self.x -= self.speed

        if self.y < ty:
            self.y += self.speed
        elif self.y > ty:
            self.y -= self.speed

    def attack(self, tree):
        enemy_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        tree_rect = pygame.Rect(tree.x, tree.y, tree.size, tree.size)

        if enemy_rect.colliderect(tree_rect):
            if self.timer <= 0:
                tree.take_damage(self.damage)
                self.timer = self.attack_cooldown
            else:
                self.timer -= 1

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
