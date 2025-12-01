import pygame
import constants
import os
from fire import Fire
import desarrollador

class CentralTree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = constants.TREE_SIZE
        self.health = constants.TREE_HEALTH
        self.max_health = constants.TREE_HEALTH  # Agregado para la barra de salud
        self.fires = []

        image_path = os.path.join('assets', 'images', 'objects', 'treeC.png')
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        self.glow = False
        self.glow_start = 0

    def get_collision_rect(self):
        """Hitbox de colisión del árbol central (usa configuración personalizada)"""
        return pygame.Rect(
            self.x + desarrollador.HITBOX_COLISION_ARBOL_CENTRAL['offset_x'],
            self.y + desarrollador.HITBOX_COLISION_ARBOL_CENTRAL['offset_y'],
            desarrollador.HITBOX_COLISION_ARBOL_CENTRAL['width'],
            desarrollador.HITBOX_COLISION_ARBOL_CENTRAL['height']
        )

    def get_attack_rect(self):
        """Hitbox de ataque del árbol central (usa configuración personalizada)"""
        return pygame.Rect(
            self.x + desarrollador.HITBOX_ATAQUE_ARBOL_CENTRAL['offset_x'],
            self.y + desarrollador.HITBOX_ATAQUE_ARBOL_CENTRAL['offset_y'],
            desarrollador.HITBOX_ATAQUE_ARBOL_CENTRAL['width'],
            desarrollador.HITBOX_ATAQUE_ARBOL_CENTRAL['height']
        )

    def start_glow(self):
        self.glow = True
        self.glow_start = pygame.time.get_ticks()

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > constants.TREE_HEALTH:
            self.health = constants.TREE_HEALTH
        self.fires.clear()
        self.start_glow()

    def add_fire(self, big=False):
        fx = self.x + self.size // 2 - constants.FIRE_SIZE // 2 - 5
        fy = self.y + self.size - int(constants.FIRE_SIZE * 0.85)
        self.fires.append(Fire(fx, fy, big))

    def draw(self, screen):
        if self.glow:
            elapsed = pygame.time.get_ticks() - self.glow_start
            alpha = 150 + 80 * pygame.math.sin(elapsed / 100)
            temp = self.image.copy()
            temp.set_alpha(max(0, min(255, int(alpha))))
            screen.blit(temp, (self.x, self.y))
            if elapsed >= constants.THROW_ANIM_TIME:
                self.glow = False
        else:
            screen.blit(self.image, (self.x, self.y))

        if desarrollador.MOSTRAR_HITBOX:
            bar_width = self.size
            bar_height = 8
            fill = (self.health / self.max_health) * bar_width if self.max_health > 0 else 0
            outline_rect = pygame.Rect(self.x, self.y - 12, bar_width, bar_height)
            fill_rect = pygame.Rect(self.x, self.y - 12, fill, bar_height)
            pygame.draw.rect(screen, constants.RED, outline_rect)
            pygame.draw.rect(screen, constants.GREEN, fill_rect)

        for fire in self.fires:
            fire.draw(screen)

        # Dibujar hitboxes si está activado el modo desarrollador
        if desarrollador.MOSTRAR_HITBOX:
            # Hitbox de colisión (usando configuración de árbol central)
            colision_rect = self.get_collision_rect()
            pygame.draw.rect(screen, desarrollador.COLOR_HITBOX_COLISION, colision_rect, 1)
            
            # Hitbox de ataque (usando configuración de árbol central)
            ataque_rect = self.get_attack_rect()
            pygame.draw.rect(screen, desarrollador.COLOR_HITBOX_ATAQUE, ataque_rect, 1)