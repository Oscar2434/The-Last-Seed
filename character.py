import pygame
import constants 
import os
import config
from constants import *
import desarrollador  # Nuevo import

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        if hasattr(config, "selected_character"):
            if config.selected_character == "niña":
                image_path = os.path.join('assets', 'images', 'character', 'eli agua.png')
            else:
                image_path = os.path.join('assets', 'images', 'character', 'dan agua.png')
        else:
            image_path = os.path.join('assets', 'images', 'character', 'dan agua.png')

        self.sprite = pygame.image.load(image_path).convert_alpha()
        self.frame_size = F_SIZE
        self.animation_frame = 0
        self.animation_timer = 0
        self.animatios_delay = DELAY_FPS

        self.current_state = DOWN
        self.moving = False
        self.animations = self.load_animatios()
        self.carrying_resource = None

        self.is_throwing = False
        self.throw_start = 0
        self.throw_frame = 0
        self.ultima_horizontal = "right"
        self.throw_direction = "right"

    def load_animatios(self):
        animations = {}
        for state in range(6):
            frames = []
            for frame in range(SPRITES1):
                surface = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
                surface.blit(self.sprite, (0, 0), (frame * self.frame_size, state * self.frame_size, self.frame_size, self.frame_size))
                if constants.PERSONAJE != self.frame_size:
                    surface = pygame.transform.scale(surface, (constants.PERSONAJE, constants.PERSONAJE))
                frames.append(surface)
            animations[state] = frames
        return animations

    def start_throw_animation(self):
        self.is_throwing = True
        self.throw_start = pygame.time.get_ticks()
        self.throw_frame = 0

        if self.current_state == 1:
            self.throw_direction = "left"
            self.ultima_horizontal = "left"

        elif self.current_state == 2:
            self.throw_direction = "right"
            self.ultima_horizontal = "right"

        elif self.current_state in (0, 3):
            self.throw_direction = self.ultima_horizontal

    def update_animation(self):
        current_time = pygame.time.get_ticks()

        if self.is_throwing:
            elapsed = current_time - self.throw_start
            frame_duration = THROW_ANIM_TIME // THROW_FRAMES
            self.throw_frame = min(THROW_FRAMES - 1, elapsed // frame_duration)
            if elapsed >= THROW_ANIM_TIME:
                self.is_throwing = False
                self.throw_frame = 0
            return

        if self.moving:
            if current_time - self.animation_timer > self.animatios_delay:
                self.animation_timer = current_time
                self.animation_frame = (self.animation_frame + 1) % SPRITES

    def draw(self, screen):
        if self.is_throwing:
            if self.throw_direction == "left":
                row = 4
            else:
                row = 5
            col = self.throw_frame
        else:
            row = self.current_state
            col = self.animation_frame

        current_image = self.animations[row][col]
        screen.blit(current_image, (self.x, self.y))
        
        # Dibujar hitbox de colisión si está activado el modo desarrollador
        if desarrollador.MOSTRAR_HITBOX:
            colision_rect = self.get_collision_rect()
            pygame.draw.rect(screen, desarrollador.COLOR_HITBOX_PERSONAJE, colision_rect, 1)

    def move(self, dx, dy, world):
        if self.is_throwing:
            self.moving = False
            self.update_animation()
            return

        self.moving = dx != 0 or dy != 0

        if self.moving:
            if dx > 0:
                self.current_state = 2
                self.ultima_horizontal = "right"
            elif dx < 0:
                self.current_state = 1
                self.ultima_horizontal = "left"
            elif dy > 0:
                self.current_state = 0
            elif dy < 0:
                self.current_state = 3
        else:
            pass

        new_x = self.x + dx
        new_y = self.y + dy

        for tree in world.trees:
            if self.check_collision(new_x, new_y, tree):
                self.moving = False
                return

        if hasattr(world, "central_tree") and world.central_tree:
            if self.check_collision(new_x, new_y, world.central_tree):
                self.moving = False
                return

        self.x = new_x
        self.y = new_y
        self.x = max(0, min(self.x, constants.WIDTH - constants.PERSONAJE))
        self.y = max(0, min(self.y, constants.HEIGHT - constants.PERSONAJE))

        self.update_animation()

    def get_collision_rect(self):
        """Devuelve el rectángulo de colisión del personaje"""
        return pygame.Rect(
            self.x + desarrollador.HITBOX_COLISION_PERSONAJE['offset_x'],
            self.y + desarrollador.HITBOX_COLISION_PERSONAJE['offset_y'],
            desarrollador.HITBOX_COLISION_PERSONAJE['width'],
            desarrollador.HITBOX_COLISION_PERSONAJE['height']
        )

    def check_collision(self, x, y, obj):
        # Crear un rectángulo de prueba para el personaje en la nueva posición
        test_rect = pygame.Rect(
            x + desarrollador.HITBOX_COLISION_PERSONAJE['offset_x'],
            y + desarrollador.HITBOX_COLISION_PERSONAJE['offset_y'],
            desarrollador.HITBOX_COLISION_PERSONAJE['width'],
            desarrollador.HITBOX_COLISION_PERSONAJE['height']
        )

        # Verificar colisión con la hitbox de colisión del objeto
        if hasattr(obj, 'get_collision_rect'):
            return test_rect.colliderect(obj.get_collision_rect())
        else:
            # Fallback: usar un rectángulo por defecto (por ejemplo, el rectángulo completo del objeto)
            return test_rect.colliderect(pygame.Rect(obj.x, obj.y, obj.size, obj.size))

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