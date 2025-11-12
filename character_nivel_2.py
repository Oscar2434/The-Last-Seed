import pygame
import constants 
import os
from constants import *

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

         #Colisión con el árbol central
         if hasattr(world, "central_tree") and world.central_tree:
             if self.check_collision(new_x, new_y, world.central_tree):
                 self.moving = False
                 return

         self.x = new_x
         self.y = new_y
         self.x = max(0, min(self.x, constants.WIDTH - constants.PERSONAJE))
         self.y = max(0, min(self.y, constants.HEIGHT - constants.PERSONAJE))
         self.update_animation()

    def check_collision(self, x, y, obj):  # ⬅️ ESTE MÉTODO DEBE ESTAR DENTRO DE LA CLASE
        # Si el objeto tiene ancho y alto diferentes
        if hasattr(obj, 'image'):
            width = obj.image.get_width() * 0.8  # 80% del ancho visual
            height = obj.image.get_height() * 0.8  # 80% del alto visual
            return (x < obj.x + width and x + constants.PERSONAJE * 0.8 > obj.x and 
                    y < obj.y + height and y + constants.PERSONAJE * 0.8 > obj.y)
        else:
            # Fallback al método original
            return (x < obj.x + obj.size * 0.3 and x + constants.PERSONAJE * 0.3 > obj.x and 
                    y < obj.y + obj.size * 0.1 and y + constants.PERSONAJE * 0.1 > obj.y)
    
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