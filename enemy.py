import pygame
import constants
import os
import random
import math
import desarrollador

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
        self.stuck_timer = 0
        self.last_x = x
        self.last_y = y
        self.stuck_threshold = 30
        self.avoidance_angle = 0

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
            return True
        return False

    def desired_step(self, target_x, target_y):
        dx = target_x - (self.x + self.size/2)
        dy = target_y - (self.y + self.size/2)
        distance = math.hypot(dx, dy)
        
        if distance < 1e-6:
            return 0, 0
            
        dx_normalized = dx / distance
        dy_normalized = dy / distance
        
        return dx_normalized * self.speed, dy_normalized * self.speed

    def get_collision_rect(self):
        return pygame.Rect(
            self.x + desarrollador.HITBOX_COLISION_ENEMIGO['offset_x'],
            self.y + desarrollador.HITBOX_COLISION_ENEMIGO['offset_y'],
            desarrollador.HITBOX_COLISION_ENEMIGO['width'],
            desarrollador.HITBOX_COLISION_ENEMIGO['height']
        )

    def get_attack_rect(self):
        return pygame.Rect(
            self.x + desarrollador.HITBOX_ATAQUE_ENEMIGO['offset_x'],
            self.y + desarrollador.HITBOX_ATAQUE_ENEMIGO['offset_y'],
            desarrollador.HITBOX_ATAQUE_ENEMIGO['width'],
            desarrollador.HITBOX_ATAQUE_ENEMIGO['height']
        )

    def is_position_blocked(self, x, y, ignore_tree=None):
        test_rect = pygame.Rect(
            x + desarrollador.HITBOX_COLISION_ENEMIGO['offset_x'],
            y + desarrollador.HITBOX_COLISION_ENEMIGO['offset_y'],
            desarrollador.HITBOX_COLISION_ENEMIGO['width'],
            desarrollador.HITBOX_COLISION_ENEMIGO['height']
        )
        
        for tree in self.world.trees:
            if tree != ignore_tree:
                if test_rect.colliderect(tree.get_collision_rect()):
                    return True
        
        if self.world.central_tree and self.world.central_tree != ignore_tree:
            if test_rect.colliderect(self.world.central_tree.get_collision_rect()):
                return True
                
        return False

    def try_alternative_directions(self, target_x, target_y, ignore_tree=None):
        enemy_center_x = self.x + self.size/2
        enemy_center_y = self.y + self.size/2
        
        dx = target_x - enemy_center_x
        dy = target_y - enemy_center_y
        base_angle = math.atan2(dy, dx)
        
        angles = [
            base_angle,
            base_angle + math.pi/6,
            base_angle - math.pi/6,
            base_angle + math.pi/3,
            base_angle - math.pi/3,
            base_angle + math.pi/2,
            base_angle - math.pi/2,
            base_angle + 2*math.pi/3,
            base_angle - 2*math.pi/3,
        ]
        
        for angle in angles:
            move_x = math.cos(angle) * self.speed
            move_y = math.sin(angle) * self.speed
            
            new_x = self.x + move_x
            new_y = self.y + move_y
            
            if not self.is_position_blocked(new_x, new_y, ignore_tree):
                return move_x, move_y
        
        return 0, 0

    def move_towards_target(self):
        if self.refresh_target_if_needed():
            return
            
        if not self.target_tree or self.attacking:
            return

        t = self.target_tree
        if t.health <= 0:
            self.attacking = False
            self.target_tree = self.choose_target()
            return

        attack_rect = t.get_attack_rect()
        target_x = attack_rect.x + attack_rect.width/2
        target_y = attack_rect.y + attack_rect.height/2

        enemy_attack_rect = self.get_attack_rect()
        if enemy_attack_rect.colliderect(attack_rect):
            self.attacking = True
            return

        dx, dy = self.desired_step(target_x, target_y)
        new_x = self.x + dx
        new_y = self.y + dy
        
        if self.is_position_blocked(new_x, new_y, t):
            dx, dy = self.try_alternative_directions(target_x, target_y, t)
            new_x = self.x + dx
            new_y = self.y + dy
        
        distance_moved = math.hypot(self.x - self.last_x, self.y - self.last_y)
        if distance_moved < 2:
            self.stuck_timer += 1
        else:
            self.stuck_timer = 0
        
        if self.stuck_timer > self.stuck_threshold:
            dx, dy = self.try_alternative_directions(target_x, target_y, t)
            new_x = self.x + dx
            new_y = self.y + dy
            self.stuck_timer = 0
        
        if not self.is_position_blocked(new_x, new_y, t):
            self.x = new_x
            self.y = new_y
            self.last_x = self.x
            self.last_y = self.y
            
            if abs(dy) > abs(dx):
                self.current_state = constants.LUMBERJACK_UP if dy < 0 else constants.LUMBERJACK_DOWN
            else:
                self.current_state = constants.LUMBERJACK_LEFT if dx < 0 else constants.LUMBERJACK_RIGHT

        self.update_animation()

    def attack(self):
        self.refresh_target_if_needed()
        if not self.target_tree:
            self.attacking = False
            return

        t = self.target_tree
        if t.health <= 0:
            self.attacking = False
            self.target_tree = self.choose_target()
            return

        enemy_attack_rect = self.get_attack_rect()
        attack_rect = t.get_attack_rect()
        
        in_range = enemy_attack_rect.colliderect(attack_rect)
        
        if in_range:
            self.attacking = True
            
            if self.cooldown_timer <= 0:
                t.take_damage(self.damage)
                if hasattr(t, 'add_fire'):
                    t.add_fire(big=True)
                self.cooldown_timer = self.attack_cooldown
            
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
        
        if desarrollador.MOSTRAR_HITBOX:
            colision_rect = self.get_collision_rect()
            pygame.draw.rect(screen, desarrollador.COLOR_HITBOX_COLISION, colision_rect, 1)
            
            ataque_rect = self.get_attack_rect()
            pygame.draw.rect(screen, desarrollador.COLOR_HITBOX_ATAQUE, ataque_rect, 1)
            
            center_x = self.x + self.size/2
            center_y = self.y + self.size/2
            pygame.draw.circle(screen, desarrollador.COLOR_HITBOX_CENTRAL, (int(center_x), int(center_y)), 3)