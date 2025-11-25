import pygame
import constants
import os
import random
import math

class Lumberjack:
    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world

        self.size = constants.LUMBERJACK_SIZE
        self.speed = constants.ENEMY_SPEED
        self.damage = constants.ENEMY_DAMAGE
        self.attack_cooldown = 60
        self.cooldown_timer = 0

        self.frame_size = constants.LUMBERJACK_F_SIZE
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = constants.LUMBERJACK_DELAY_FPS

        self.current_state = constants.LUMBERJACK_DOWN
        self.attacking = False

        image_path = os.path.join('assets', 'images', 'character', 'antagonista.png')
        self.sprite = pygame.image.load(image_path).convert_alpha()
        self.animations = self.load_animations()

        self.target_tree = self.choose_target()
        
        # Sistema de navegación mejorado
        self.stuck_timer = 0
        self.last_positions = []
        self.path_attempts = 0
        self.max_path_attempts = 5

    def load_animations(self):
        animations = {}
        total_states = 6
        for state in range(total_states):
            frames = []
            for frame in range(constants.SPRITES):
                rect = pygame.Rect(
                    frame * self.frame_size,
                    state * self.frame_size,
                    self.frame_size,
                    self.frame_size
                )
                surf = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
                surf.blit(self.sprite, (0, 0), rect)
                if self.size != self.frame_size:
                    surf = pygame.transform.scale(surf, (self.size, self.size))
                frames.append(surf)
            animations[state] = frames
        return animations

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.animation_timer >= self.animation_delay:
            self.animation_timer = now
            self.animation_frame = (self.animation_frame + 1) % constants.SPRITES

    def choose_target(self):
        """Selección de objetivos mejorada"""
        available_trees = []
        
        for t in self.world.trees:
            if t.health > 0:
                available_trees.append(t)
        
        if self.world.central_tree and self.world.central_tree.health > 0:
            available_trees.append(self.world.central_tree)
        
        if not available_trees:
            return None

        def distance_to_tree(tree):
            cx = tree.x + tree.size * 0.5
            cy = tree.y + tree.size * 0.5
            ex = self.x + self.size * 0.5
            ey = self.y + self.size * 0.5
            return (cx - ex)**2 + (cy - ey)**2

        available_trees.sort(key=distance_to_tree)

        # Distribuir enemigos entre árboles
        if hasattr(self.world, "enemies"):
            target_count = {}
            for enemy in self.world.enemies:
                if hasattr(enemy, "target_tree") and enemy.target_tree:
                    target_count[enemy.target_tree] = target_count.get(enemy.target_tree, 0) + 1
            
            for tree in available_trees:
                if target_count.get(tree, 0) < 2:
                    return tree
        
        return available_trees[0]

    def refresh_target_if_needed(self):
        if not self.target_tree or self.target_tree.health <= 0:
            self.attacking = False
            self.target_tree = self.choose_target()
            self.path_attempts = 0  # Resetear intentos al cambiar objetivo
            return True
        return False

    def desired_step(self, target_x, target_y):
        """Calcular dirección hacia el objetivo"""
        dx = target_x - (self.x + self.size/2)
        dy = target_y - (self.y + self.size/2)
        distance = math.hypot(dx, dy)
        
        if distance < 1e-6:
            return 0, 0
            
        dx_normalized = dx / distance
        dy_normalized = dy / distance
        
        return dx_normalized * self.speed, dy_normalized * self.speed

    def is_position_blocked(self, x, y, ignore_tree=None):
        """Verificar si una posición está bloqueada por hitboxes de colisión"""
        test_rect = pygame.Rect(x, y, self.size, self.size)
        
        # Verificar colisión con otros árboles
        for tree in self.world.trees:
            if tree.health > 0 and tree != ignore_tree:
                if test_rect.colliderect(tree.get_collision_rect()):
                    return True
        
        # Verificar colisión con árbol central
        if self.world.central_tree and self.world.central_tree.health > 0 and self.world.central_tree != ignore_tree:
            if test_rect.colliderect(self.world.central_tree.get_collision_rect()):
                return True
                
        return False

    def find_path_around_obstacle(self, target_x, target_y, obstacle_tree):
        """Encontrar camino alrededor de un obstáculo específico"""
        enemy_center_x = self.x + self.size/2
        enemy_center_y = self.y + self.size/2
        
        # Calcular ángulo hacia el objetivo
        dx = target_x - enemy_center_x
        dy = target_y - enemy_center_y
        target_angle = math.atan2(dy, dx)
        
        # Probar ángulos alternativos alrededor del obstáculo
        angles_to_try = [
            target_angle,  # Dirección original
            target_angle + math.pi/4,    # 45° derecha
            target_angle - math.pi/4,    # 45° izquierda
            target_angle + math.pi/2,    # 90° derecha  
            target_angle - math.pi/2,    # 90° izquierda
            target_angle + math.pi*0.75, # 135° derecha
            target_angle - math.pi*0.75, # 135° izquierda
        ]
        
        # Radio para evitar el obstáculo (tamaño del árbol + margen)
        avoid_radius = obstacle_tree.size * 0.8
        
        for angle in angles_to_try:
            # Calcular posición de prueba
            test_x = enemy_center_x + math.cos(angle) * avoid_radius
            test_y = enemy_center_y + math.sin(angle) * avoid_radius
            
            # Ajustar a la posición del enemigo (esquina)
            test_x -= self.size/2
            test_y -= self.size/2
            
            # Verificar si esta posición está libre
            if not self.is_position_blocked(test_x, test_y, obstacle_tree):
                return self.desired_step(test_x + self.size/2, test_y + self.size/2)
        
        return 0, 0  # No se encontró camino

    def move_towards_target(self):
        """Sistema de movimiento completamente nuevo con dos hitboxes"""
        if self.refresh_target_if_needed():
            return
            
        if not self.target_tree or self.attacking:
            return

        t = self.target_tree
        if t.health <= 0:
            self.attacking = False
            self.target_tree = self.choose_target()
            self.path_attempts = 0
            return

        # Calcular posición objetivo (hitbox de ataque del árbol)
        attack_rect = t.get_attack_rect()
        target_x = attack_rect.x + attack_rect.width/2
        target_y = attack_rect.y + attack_rect.height/2

        # Verificar si ya estamos en posición de ataque
        enemy_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        if enemy_rect.colliderect(attack_rect):
            self.attacking = True
            return

        # Calcular movimiento hacia el objetivo
        dx, dy = self.desired_step(target_x, target_y)
        
        # Verificar si el camino está bloqueado
        new_x = self.x + dx
        new_y = self.y + dy
        
        if self.is_position_blocked(new_x, new_y, t):
            # Camino bloqueado, buscar ruta alternativa
            self.path_attempts += 1
            
            if self.path_attempts <= self.max_path_attempts:
                # Encontrar el árbol que está bloqueando
                blocking_tree = None
                test_rect = pygame.Rect(new_x, new_y, self.size, self.size)
                
                for tree in self.world.trees + ([self.world.central_tree] if self.world.central_tree else []):
                    if tree != t and tree.health > 0:
                        if test_rect.colliderect(tree.get_collision_rect()):
                            blocking_tree = tree
                            break
                
                if blocking_tree:
                    # Intentar rodear el obstáculo
                    alt_dx, alt_dy = self.find_path_around_obstacle(target_x, target_y, blocking_tree)
                    if alt_dx != 0 or alt_dy != 0:
                        new_x = self.x + alt_dx
                        new_y = self.y + alt_dy
            else:
                # Demasiados intentos, cambiar objetivo
                self.target_tree = self.choose_target()
                self.path_attempts = 0
                return
        else:
            # Camino libre, resetear contador
            self.path_attempts = 0

        # Aplicar movimiento si la nueva posición es válida
        if not self.is_position_blocked(new_x, new_y, t):
            self.x = new_x
            self.y = new_y
            
            # Actualizar animación de movimiento
            if abs(dy) > abs(dx):
                self.current_state = constants.LUMBERJACK_UP if dy < 0 else constants.LUMBERJACK_DOWN
            else:
                self.current_state = constants.LUMBERJACK_LEFT if dx < 0 else constants.LUMBERJACK_RIGHT
        else:
            # Si aún está bloqueado después de todo, cambiar objetivo
            self.target_tree = self.choose_target()
            self.path_attempts = 0

        self.update_animation()

    def attack(self):
        """Sistema de ataque usando hitbox de ataque"""
        self.refresh_target_if_needed()
        if not self.target_tree:
            self.attacking = False
            return

        t = self.target_tree
        if t.health <= 0:
            self.attacking = False
            self.target_tree = self.choose_target()
            return

        # Verificar si estamos en la hitbox de ataque
        enemy_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        attack_rect = t.get_attack_rect()
        
        in_range = enemy_rect.colliderect(attack_rect)
        
        if in_range:
            self.attacking = True
            
            if self.cooldown_timer <= 0:
                t.take_damage(self.damage)
                if hasattr(t, 'add_fire'):
                    t.add_fire(big=True)
                self.cooldown_timer = self.attack_cooldown
            
            # Animación de ataque basada en posición relativa
            enemy_center_x = self.x + self.size/2
            enemy_center_y = self.y + self.size/2
            tree_center_x = t.x + t.size/2
            tree_center_y = t.y + t.size/2
            
            dx = tree_center_x - enemy_center_x
            self.current_state = (constants.LUMBERJACK_ATTACK_LEFT 
                                if dx < 0 else constants.LUMBERJACK_ATTACK_RIGHT)
        else:
            self.attacking = False
        
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
        
        self.update_animation()

    def draw(self, screen):
        img = self.animations[self.current_state][self.animation_frame]
        screen.blit(img, (self.x, self.y))
        
        # NOTA: Se eliminó el código de dibujo de hitboxes de debug