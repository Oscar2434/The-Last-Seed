import pygame
import constants
import os
import random

class Lumberjack:
    def __init__(self, x, y, target_pos):
        self.x = x
        self.y = y
        self.size = constants.LUMBERJACK_SIZE
        self.speed = constants.ENEMY_SPEED
        self.damage = constants.ENEMY_DAMAGE
        self.attack_cooldown = 60
        self.timer = 0
        self.target_pos = target_pos  

        # Animación
        self.frame_size = constants.LUMBERJACK_F_SIZE  
        self.animation_frame = 0
        self.animation_timer = 0
        self.animatios_delay = constants.LUMBERJACK_DELAY_FPS
        self.current_state = constants.LUMBERJACK_DOWN
        self.moving = False
        self.attacking = False

        # Cargar spritesheet del enemigo
        image_path = os.path.join('assets', 'images', 'character', 'antagonista.png')
        self.sprite = pygame.image.load(image_path).convert_alpha()

        # Animaciones
        self.animations = self.load_animations()

    def load_animations(self):
        animations = {}
        # OJO: este valor depende de tu spritesheet original
        # → 4 direcciones (up, down, left, right) + 2 ataques (left y right)
        total_states = 6  
        for state in range(total_states):
            frames = []
            for frame in range(constants.SPRITES):
                rect = pygame.Rect(
                    frame * constants.LUMBERJACK_F_SIZE,
                    state * constants.LUMBERJACK_F_SIZE,
                    constants.LUMBERJACK_F_SIZE,
                    constants.LUMBERJACK_F_SIZE
                )
                surface = pygame.Surface((constants.LUMBERJACK_F_SIZE, constants.LUMBERJACK_F_SIZE), pygame.SRCALPHA)
                surface.blit(self.sprite, (0, 0), rect)

                if constants.LUMBERJACK_SIZE != constants.LUMBERJACK_F_SIZE:
                    surface = pygame.transform.scale(surface,
                                                     (constants.LUMBERJACK_SIZE, constants.LUMBERJACK_SIZE))
                frames.append(surface)
            animations[state] = frames
        return animations

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if self.moving or self.attacking:
            if current_time - self.animation_timer > self.animatios_delay:
                self.animation_timer = current_time
                self.animation_frame = (self.animation_frame + 1) % constants.SPRITES

    def move_towards(self, tree):
        if self.attacking:
            return  

        # 🔧 Recalcular siempre la posición objetivo hacia el árbol
        self.target_pos = (tree.x, tree.y)

        enemy_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        tree_rect = pygame.Rect(tree.x, tree.y, tree.size, tree.size)

        if enemy_rect.colliderect(tree_rect):
            self.moving = False
            return  

        tx, ty = self.target_pos
        dx = tx - self.x
        dy = ty - self.y

        step_x, step_y = 0, 0
        if dx > 0:
            step_x = self.speed
        elif dx < 0:
            step_x = -self.speed
        if dy > 0:
            step_y = self.speed
        elif dy < 0:
            step_y = -self.speed

        self.moving = (step_x != 0 or step_y != 0)

        if self.moving:
            if step_x > 0:
                self.current_state = constants.LUMBERJACK_RIGHT
            elif step_x < 0:
                self.current_state = constants.LUMBERJACK_LEFT
            elif step_y > 0:
                self.current_state = constants.LUMBERJACK_DOWN
            elif step_y < 0:
                self.current_state = constants.LUMBERJACK_UP

        self.x += step_x
        self.y += step_y
        self.update_animation()

    def attack(self, tree):
        enemy_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        tree_rect = pygame.Rect(tree.x, tree.y, tree.size, tree.size)

        if enemy_rect.colliderect(tree_rect):
            self.attacking = True
            if self.timer <= 0:
                # Animación de ataque
                if self.x < tree.x:
                    self.current_state = constants.LUMBERJACK_ATTACK_RIGHT
                else:
                    self.current_state = constants.LUMBERJACK_ATTACK_LEFT

                self.animation_frame = 0  # reiniciar animación de ataque

                # 🔥 Daño y añadir fuego (árbol central siempre fila 1 → big=True)
                tree.take_damage(self.damage)
                tree.add_fire(big=True)

                self.timer = self.attack_cooldown
            else:
                self.timer -= 1
        else:
            self.attacking = False

        self.update_animation()

    def draw(self, screen):
        current_image = self.animations[self.current_state][self.animation_frame]
        screen.blit(current_image, (self.x, self.y))
