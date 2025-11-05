import pygame
import constants 
import os
from constants import *

gy=18 # Ajuste horizontal de la hitbox
gx=12 # Ajuste vertical de la hitbox
ry=0.6 # escalar hitbox y
rx=0.55 # escalar hitbox x

#Clase del personaje
class Character:
    def __init__(self, x, y):
         self.x = x
         self.y = y
         image_path = os.path.join('assets', 'images', 'character', 'nino.png')
         self.sprite = pygame.image.load(image_path).convert_alpha()
         self.frame_size = F_SIZE
         self.animation_frame = 0
         self.animation_timer = 0
         self.animatios_delay = DELAY_FPS
         self.current_state = DOWN
         self.moving = False 
         self.facing_left = False
         self.animations = self.load_animatios()
         self.carrying_resource = None   

    def load_animatios(self):
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
        current_time = pygame.time.get_ticks()
        if self.moving:
            if current_time - self.animation_timer > self.animatios_delay:
                self.animation_timer = current_time
                self.animation_frame = (self.animation_frame + 1) % SPRITES
        
    def draw(self, screen):
        if self.current_state not in self.animations:
            self.current_state = DOWN
        current_image = self.animations[self.current_state][self.animation_frame]
        if self.facing_left:
            current_image = pygame.transform.flip(current_image, True, False)
        screen.blit(current_image, (self.x, self.y))
        
        # ⬇️ DEBUG: Dibujar rectángulo de colisión del PERSONAJE en AZUL ⬇️
        debug_rect = pygame.Rect(
            self.x + gx,  # ⬅️ AJUSTAR: Mover hitbox 10px a la DERECHA
            self.y + gy,  # ⬅️ AJUSTAR: Mover hitbox 20px hacia ABAJO
            constants.PERSONAJE * ry,  # 60% del ancho
            constants.PERSONAJE * rx   # 60% del alto
        )
        pygame.draw.rect(screen, (0, 0, 255), debug_rect, 2)  # Azul, línea de 2px

    def move(self, dx, dy, world):
         self.moving = dx != 0 or dy != 0
         if self.moving:
            if dx > 0:  
                self.current_state = RIGHT
                self.facing_left = False
            elif dx < 0:  
                self.current_state = RIGHT
                self.facing_left = True
            elif dy > 0:  
                self.current_state = DOWN
                self.facing_left = False
            elif dy < 0:  
                self.current_state = UP
                self.facing_left = False
         else :
            if self.current_state in [MOVE_DOWN, DOWN]:
                self.current_state = DOWN
            elif self.current_state in [MOVE_UP, UP]:
                self.current_state = UP
            elif self.current_state in [MOVE_RIGHT, RIGHT]:
                self.current_state = RIGHT

         new_x = self.x + dx
         new_y = self.y + dy

         #Colisiones con los árboles normales
         for tree in world.trees:
             if self.check_collision(new_x, new_y, tree):
                 self.moving = False
                 return

         # COLISIÓN CON MUROS - AGREGADA
         for wall in world.walls:
             if self.check_collision(new_x, new_y, wall):
                 self.moving = False
                 return

         # ✅ AGREGADO: Colisión con el árbol central del nivel 2
         if hasattr(world, "central_tree") and world.central_tree:
             if self.check_collision(new_x, new_y, world.central_tree):
                 self.moving = False
                 return

         self.x = new_x
         self.y = new_y
         self.x = max(0, min(self.x, constants.WIDTH - constants.PERSONAJE))
         self.y = max(0, min(self.y, constants.HEIGHT - constants.PERSONAJE))
         self.update_animation()
         
         # ACTUALIZAR: Verificar colisión con recursos (pero no recolectar automáticamente)
         self.near_resource = self.check_near_resource(world.resources)

    def check_collision(self, x, y, obj):
        # MODIFICADO: Usar Rect para que la hitbox del personaje coincida con el cuadro rojo del árbol
        if hasattr(obj, 'get_rect'):
            obj_rect = obj.get_rect()
            player_rect = pygame.Rect(
                x + gx,
                y + gy,
                constants.PERSONAJE * ry,  # ancho usado en el debug_rect
                constants.PERSONAJE * rx   # alto usado en el debug_rect
            )
            return player_rect.colliderect(obj_rect)
        
        if hasattr(obj, 'image'):
            # Usar las mismas proporciones que se dibujan en nivel_2.py para central_tree
            if hasattr(obj, 'type') and obj.type == "central_tree":
                width = obj.image.get_width() * 0.9
                height = obj.image.get_height() * 0.8
            else:
                width = obj.image.get_width() * 0.9
                height = obj.image.get_height() * 0.7

            tree_rect = pygame.Rect(obj.x, obj.y, width, height)

            player_rect = pygame.Rect(
                x + gx,
                y + gy,
                constants.PERSONAJE * ry,
                constants.PERSONAJE * rx
            )

            return player_rect.colliderect(tree_rect)
        
        return False

    def check_collect_resource(self, resources):
        for resource in resources:
            if not resource.collected and self.check_collision(self.x, self.y, resource):
                if self.carrying_resource is None:
                    resource.collected = True
                    self.carrying_resource = resource
                    return

    def deliver_resource(self, tree):
        if self.carrying_resource:
            tree.heal(constants.RESOURCE_HEAL)
            self.carrying_resource = None

    def check_near_resource(self, resources):
        """Verificar si está cerca de un recurso para recoger"""
        for resource in resources:
            if not resource.collected and self.check_collision(self.x, self.y, resource):
                return resource
        return None