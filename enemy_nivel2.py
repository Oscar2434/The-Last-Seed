import pygame
import constants
import os
from constants import *

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1  # Velocidad del enemigo (puedes ajustarla)
        
        # Variables de hitbox similares al personaje
        self.gy = 18
        self.gx = 12
        self.ry = 0.6
        self.rx = 0.55
        
        # Intentar cargar sprite del enemigo, si no existe usar placeholder
        try:
            image_path = os.path.join('assets', 'images', 'character', 'enemy.png')
            self.sprite = pygame.image.load(image_path).convert_alpha()
            self.has_sprite = True
            self.frame_size = F_SIZE
            self.animation_frame = 0
            self.animation_timer = 0
            self.animations_delay = DELAY_FPS
            self.current_state = DOWN
            self.moving = False
            self.facing_left = False
            self.animations = self.load_animations()
        except:
            # Si no hay imagen, usar un cuadrado azul
            self.has_sprite = False
            self.placeholder = pygame.Surface((constants.PERSONAJE, constants.PERSONAJE))
            self.placeholder.fill((0, 0, 255))  # Azul

    def load_animations(self):
        """Cargar animaciones similares al personaje"""
        animations = {}
        for state in range(4):
            frames = []
            for frame in range(SPRITES):
                surface = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
                surface.blit(self.sprite, (0, 0), (frame * self.frame_size, state * self.frame_size, self.frame_size, self.frame_size))
                if constants.PERSONAJE != self.frame_size:
                    surface = pygame.transform.scale(surface, (constants.PERSONAJE, constants.PERSONAJE))
                frames.append(surface)
            animations[state] = frames
        return animations

    def update_animation(self):
        """Actualizar animación si tiene sprite"""
        if not self.has_sprite:
            return
            
        current_time = pygame.time.get_ticks()
        if self.moving:
            if current_time - self.animation_timer > self.animations_delay:
                self.animation_timer = current_time
                self.animation_frame = (self.animation_frame + 1) % SPRITES

    def draw(self, screen):
        """Dibujar al enemigo"""
        if self.has_sprite:
            if self.current_state not in self.animations:
                self.current_state = DOWN
            current_image = self.animations[self.current_state][self.animation_frame]
            if self.facing_left:
                current_image = pygame.transform.flip(current_image, True, False)
            screen.blit(current_image, (self.x, self.y))
        else:
            # Dibujar placeholder azul
            screen.blit(self.placeholder, (self.x, self.y))
        
        # DEBUG: Dibujar rectángulo de colisión del ENEMIGO en ROJO
        debug_rect = pygame.Rect(
            self.x + self.gx,
            self.y + self.gy,
            constants.PERSONAJE * self.ry,
            constants.PERSONAJE * self.rx
        )
        pygame.draw.rect(screen, (255, 0, 0), debug_rect, 2)  # Rojo, línea de 2px

    def move_towards_player(self, player_x, player_y, world):
        """Moverse hacia el jugador evitando obstáculos"""
        # Calcular dirección hacia el jugador
        dx = player_x - self.x
        dy = player_y - self.y
        
        # Normalizar dirección
        distance = max(1, (dx**2 + dy**2)**0.5)  # Evitar división por cero
        dx = dx / distance * self.speed
        dy = dy / distance * self.speed
        
        # Actualizar animación si tiene sprite
        if self.has_sprite:
            self.moving = True
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.current_state = RIGHT
                    self.facing_left = False
                else:
                    self.current_state = RIGHT
                    self.facing_left = True
            else:
                if dy > 0:
                    self.current_state = DOWN
                    self.facing_left = False
                else:
                    self.current_state = UP
                    self.facing_left = False
        
        # Intentar mover en X
        new_x = self.x + dx
        if not self.check_collision(new_x, self.y, world):
            self.x = new_x
        else:
            # Si hay colisión en X, intentar moverse solo en Y
            new_y = self.y + dy
            if not self.check_collision(self.x, new_y, world):
                self.y = new_y
        
        # Intentar mover en Y
        new_y = self.y + dy
        if not self.check_collision(self.x, new_y, world):
            self.y = new_y
        else:
            # Si hay colisión en Y, intentar moverse solo en X
            new_x = self.x + dx
            if not self.check_collision(new_x, self.y, world):
                self.x = new_x
        
        # Mantener dentro de los límites
        self.x = max(0, min(self.x, constants.WIDTH - constants.PERSONAJE))
        self.y = max(0, min(self.y, constants.HEIGHT - constants.PERSONAJE))
        
        self.update_animation()

    def check_collision(self, x, y, world):
        """Verificar colisiones con obstáculos (similar al personaje)"""
        # Hitbox del enemigo
        enemy_rect = pygame.Rect(
            x + self.gx,
            y + self.gy,
            constants.PERSONAJE * self.ry,
            constants.PERSONAJE * self.rx
        )
        
        # Colisión con muros
        for wall in world.walls:
            if hasattr(wall, 'get_rect'):
                wall_rect = wall.get_rect()
                if enemy_rect.colliderect(wall_rect):
                    return True
        
        # Colisión con árbol central
        if hasattr(world, "central_tree") and world.central_tree:
            if hasattr(world.central_tree, 'image'):
                # Usar las mismas proporciones que el personaje
                x_offset = world.central_tree.image.get_width() * constants.CENTRAL_TREE_HITBOX_X
                y_offset = world.central_tree.image.get_height() * constants.CENTRAL_TREE_HITBOX_Y
                width = world.central_tree.image.get_width() * constants.CENTRAL_TREE_HITBOX_WIDTH
                height = world.central_tree.image.get_height() * constants.CENTRAL_TREE_HITBOX_HEIGHT

                tree_rect = pygame.Rect(
                    world.central_tree.x + x_offset, 
                    world.central_tree.y + y_offset, 
                    width, 
                    height
                )
                if enemy_rect.colliderect(tree_rect):
                    return True
        
        return False

    def check_capture(self, character):
        """Verificar si capturó al jugador"""
        enemy_rect = pygame.Rect(
            self.x + self.gx,
            self.y + self.gy,
            constants.PERSONAJE * self.ry,
            constants.PERSONAJE * self.rx
        )
        
        player_rect = pygame.Rect(
            character.x + character.gx,
            character.y + character.gy,
            constants.PERSONAJE * character.ry,
            constants.PERSONAJE * character.rx
        )
        
        return enemy_rect.colliderect(player_rect)