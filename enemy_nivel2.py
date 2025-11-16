import pygame
import pygame
import constants
import os
from constants import *

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1  
        
        # Variables de hitbox similares al personaje
        self.gy = 18
        self.gx = 12
        self.ry = 0.6
        self.rx = 0.55
        
        # Cargar sprites del fantasma
        try:
            # Cargar ambas direcciones del fantasma
            image_path_i = os.path.join('assets', 'images', 'fantasma', 'fantasma_i.png')
            image_path_d = os.path.join('assets', 'images', 'fantasma', 'fantasma_d.png')
            
            self.sprite_i = pygame.image.load(image_path_i).convert_alpha()
            self.sprite_d = pygame.image.load(image_path_d).convert_alpha()
            
            self.has_sprite = True
            
            # Escalar los sprites al tamaño del personaje
            self.sprite_i = pygame.transform.scale(self.sprite_i, (constants.PERSONAJE, constants.PERSONAJE))
            self.sprite_d = pygame.transform.scale(self.sprite_d, (constants.PERSONAJE, constants.PERSONAJE))
            
            self.facing_left = False  
            self.moving = False
           
            self.animation_timer = 0
            self.animations_delay = 500  
            self.current_image = self.sprite_d  
            
        except Exception as e:
            print(f"Error cargando sprites del fantasma: {e}")
          
            self.has_sprite = False
            self.placeholder = pygame.Surface((constants.PERSONAJE, constants.PERSONAJE))
            self.placeholder.fill((0, 0, 255)) 

    def update_animation(self):
        
        if not self.has_sprite:
            return
            
        current_time = pygame.time.get_ticks()
        
       
        if self.moving:
            
            if self.facing_left:
                self.current_image = self.sprite_i
            else:
                self.current_image = self.sprite_d

    def draw(self, screen):
       
        if self.has_sprite:
            screen.blit(self.current_image, (self.x, self.y))
        else:
            # Dibujar placeholder azul
            screen.blit(self.placeholder, (self.x, self.y))
        
       
    def move_towards_player(self, player_x, player_y, world):
       
        dx = player_x - self.x
        dy = player_y - self.y
        
     
        distance = max(1, (dx**2 + dy**2)**0.5)  
        dx = dx / distance * self.speed
        dy = dy / distance * self.speed
        
       
        self.moving = True
        
        # Solo cambiamos dirección cuando hay movimiento horizontal significativo
        if abs(dx) > 0.1: 
            if dx > 0:
                self.facing_left = False  
            else:
                self.facing_left = True   
        
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