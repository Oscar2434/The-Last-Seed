import constants
import pygame
import os
import math
from fire import Fire
import desarrollador

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
        self.glow = False
        self.glow_start = 0
        self.protected_until = 0  # NUEVA VARIABLE: tiempo hasta que termina protección

    def get_collision_rect(self):
        """Hitbox de colisión usando el sistema centralizado"""
        return pygame.Rect(
            self.x + desarrollador.HITBOX_COLISION_ARBOL['offset_x'],
            self.y + desarrollador.HITBOX_COLISION_ARBOL['offset_y'],
            desarrollador.HITBOX_COLISION_ARBOL['width'],
            desarrollador.HITBOX_COLISION_ARBOL['height']
        )

    def get_attack_rect(self):
        """Hitbox de ataque usando el sistema centralizado"""
        return pygame.Rect(
            self.x + desarrollador.HITBOX_ATAQUE_ARBOL['offset_x'],
            self.y + desarrollador.HITBOX_ATAQUE_ARBOL['offset_y'],
            desarrollador.HITBOX_ATAQUE_ARBOL['width'],
            desarrollador.HITBOX_ATAQUE_ARBOL['height']
        )

    def start_glow(self):
        self.glow = True
        self.glow_start = pygame.time.get_ticks()

    def is_protected(self):
        """Verifica si el árbol está protegido"""
        return pygame.time.get_ticks() < self.protected_until

    def activate_protection(self):
        """Activa la protección por 5 segundos después de riego"""
        self.protected_until = pygame.time.get_ticks() + desarrollador.TREE_PROTECTION_TIME
        # eliminar fuegos actuales inmediatamente para que no vuelvan a mostrarse
        self.fires.clear()

    def take_damage(self, amount):
        """Solo recibe daño si NO está protegido"""
        if not self.is_protected():
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
        self.start_glow()

    def add_fire(self, big=False):
        """Agrega fuego solo si el árbol NO está protegido"""
        # Mantener protección fuerte: si está protegido no agregar fuego
        if self.is_protected():
            return
        fire = Fire(
            self.x + self.size // 2 + desarrollador.FIRE_OFFSET_X,
            self.y + self.size // 2 + desarrollador.FIRE_OFFSET_Y,
            big
        )
        self.fires.append(fire)

    def draw(self, screen):
        # Si está protegido, asegurarse de que no haya fuegos visibles
        if self.is_protected():
            # limpiar la lista cada frame para evitar que un enemy reañada fuegos
            if self.fires:
                self.fires.clear()
        # Dibujo del árbol
        if self.glow:
            elapsed = pygame.time.get_ticks() - self.glow_start
            alpha = 150 + 80 * math.sin(elapsed / 100)
            temp = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
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
            rect = pygame.Rect(self.current_frame * self.frame_size, row * self.frame_size, self.frame_size, self.frame_size)
            temp.blit(self.sprite, (0, 0), rect)
            temp = pygame.transform.scale(temp, (self.size, self.size))
            temp.set_alpha(max(0, min(255, int(alpha))))
            screen.blit(temp, (self.x, self.y))
            if elapsed >= constants.THROW_ANIM_TIME:
                self.glow = False
        else:
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

        # Dibujar fuegos (si quedan)
        for fire in self.fires:
            fire.draw(screen)

        # DIBUJAR HITBOXES DEL ÁRBOL (modo desarrollador)
        if desarrollador.MOSTRAR_HITBOX:
            # Hitbox de colisión
            col_rect = self.get_collision_rect()
            pygame.draw.rect(screen, desarrollador.COLOR_HITBOX_COLISION, col_rect, 1)
            # Hitbox de ataque
            atk_rect = self.get_attack_rect()
            pygame.draw.rect(screen, desarrollador.COLOR_HITBOX_ATAQUE, atk_rect, 1)

            # DIBUJAR BARRA DE VIDA (solo en modo desarrollador)
            bar_width = self.size
            bar_height = 8
            fill = (self.health / self.max_health) * bar_width if self.max_health > 0 else 0
            outline_rect = pygame.Rect(self.x, self.y - 12, bar_width, bar_height)
            fill_rect = pygame.Rect(self.x, self.y - 12, fill, bar_height)
            pygame.draw.rect(screen, constants.RED, outline_rect)
            pygame.draw.rect(screen, constants.GREEN, fill_rect)

# En ambient.py, modifica la clase CentralTree:
class CentralTree(Tree):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = constants.TREE_HEALTH
        self.max_health = constants.TREE_HEALTH
        self.size = constants.TREE_SIZE
        self.sprite = pygame.image.load(os.path.join('assets', 'images', 'objects', 'arbolquemado.png')).convert_alpha()

    def get_collision_rect(self):
        """Hitbox de colisión del árbol central (configuración personalizada)"""
        return pygame.Rect(
            self.x + desarrollador.HITBOX_COLISION_ARBOL_CENTRAL['offset_x'],
            self.y + desarrollador.HITBOX_COLISION_ARBOL_CENTRAL['offset_y'],
            desarrollador.HITBOX_COLISION_ARBOL_CENTRAL['width'],
            desarrollador.HITBOX_COLISION_ARBOL_CENTRAL['height']
        )

    def get_attack_rect(self):
        """Hitbox de ataque del árbol central (configuración personalizada)"""
        return pygame.Rect(
            self.x + desarrollador.HITBOX_ATAQUE_ARBOL_CENTRAL['offset_x'],
            self.y + desarrollador.HITBOX_ATAQUE_ARBOL_CENTRAL['offset_y'],
            desarrollador.HITBOX_ATAQUE_ARBOL_CENTRAL['width'],
            desarrollador.HITBOX_ATAQUE_ARBOL_CENTRAL['height']
        )

class Rock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        rock_path = os.path.join('assets', 'images', 'objects', 'rock.png')
        self.image = pygame.image.load(rock_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.ROCK, constants.ROCK))
        self.size = constants.ROCK

    def get_collision_rect(self):
        """Hitbox de colisión de la roca usando el sistema centralizado"""
        return pygame.Rect(
            self.x + desarrollador.HITBOX_COLISION_ROCA['offset_x'],
            self.y + desarrollador.HITBOX_COLISION_ROCA['offset_y'],
            desarrollador.HITBOX_COLISION_ROCA['width'],
            desarrollador.HITBOX_COLISION_ROCA['height']
        )

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
        # Dibujar hitbox si está activado el modo desarrollador
        if desarrollador.MOSTRAR_HITBOX:
            colision_rect = self.get_collision_rect()
            pygame.draw.rect(screen, desarrollador.COLOR_HITBOX_ROCA, colision_rect, 1)