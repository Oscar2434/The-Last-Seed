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

    def trunk_rect(self, tree):
        h = int(tree.size * 0.45)
        y0 = int(tree.y + tree.size - h)
        return pygame.Rect(tree.x, y0, tree.size, h)

    def choose_target(self):
        trees = [t for t in self.world.trees if t.health > 0]
        if self.world.central_tree and self.world.central_tree.health > 0:
            trees.append(self.world.central_tree)
        if not trees:
            return None

        def dist2(t):
            cx = t.x + t.size * 0.5
            cy = t.y + t.size * 0.5
            return (cx - (self.x + self.size * 0.5))**2 + (cy - (self.y + self.size * 0.5))**2

        trees.sort(key=dist2)

        if hasattr(self.world, "enemies"):
            engaged = [e.target_tree for e in self.world.enemies if getattr(e, "target_tree", None)]
            for t in trees:
                if t not in engaged:
                    return t
        return trees[0]

    def refresh_target_if_needed(self):
        if not self.target_tree or self.target_tree.health <= 0:
            self.attacking = False
            self.target_tree = self.choose_target()

    def desired_step(self, tx, ty):
        dx = tx - self.x
        dy = ty - self.y
        d = (dx*dx + dy*dy) ** 0.5
        if d < 1e-6:
            return 0.0, 0.0
        return (self.speed * dx / d, self.speed * dy / d)

    def collide_any_tree(self, rect, target):
        for t in self.world.trees:
            if t is target:
                if rect.colliderect(self.trunk_rect(t)):
                    return t
            else:
                if rect.colliderect(pygame.Rect(t.x, t.y, t.size, t.size)):
                    return t
        ct = self.world.central_tree
        if ct:
            if ct is target:
                if rect.colliderect(self.trunk_rect(ct)):
                    return ct
            else:
                if rect.colliderect(pygame.Rect(ct.x, ct.y, ct.size, ct.size)):
                    return ct
        return None

    def move_towards_target(self):
        self.refresh_target_if_needed()
        if not self.target_tree or self.attacking:
            return

        t = self.target_tree
        tx = t.x + t.size * 0.5 - self.size * 0.5
        ty = t.y + t.size * 0.5 - self.size * 0.5
        sx, sy = self.desired_step(tx, ty)

        enemy_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        try_rect = enemy_rect.move(sx, 0)
        hit = self.collide_any_tree(try_rect, t)
        moved_x, moved_y = 0.0, 0.0

        if hit is None:
            self.x += sx
            moved_x = sx
        else:
            if hit is t:
                self.attacking = True
            else:
                detour = self.speed
                left_try = enemy_rect.move(-detour, 0)
                right_try = enemy_rect.move(detour, 0)
                if self.collide_any_tree(left_try, t) is None:
                    self.x -= detour
                    moved_x = -detour
                elif self.collide_any_tree(right_try, t) is None:
                    self.x += detour
                    moved_x = detour

        if not self.attacking:
            enemy_rect = pygame.Rect(self.x, self.y, self.size, self.size)
            try_rect = enemy_rect.move(0, sy)
            hit = self.collide_any_tree(try_rect, t)
            if hit is None:
                self.y += sy
                moved_y = sy
            else:
                if hit is t:
                    self.attacking = True
                else:
                    detour = self.speed
                    up_try = enemy_rect.move(0, -detour)
                    down_try = enemy_rect.move(0, detour)
                    if self.collide_any_tree(up_try, t) is None:
                        self.y -= detour
                        moved_y = -detour
                    elif self.collide_any_tree(down_try, t) is None:
                        self.y += detour
                        moved_y = detour

        if not self.attacking:
            if abs(moved_y) > abs(moved_x):
                self.current_state = constants.LUMBERJACK_UP if moved_y < 0 else constants.LUMBERJACK_DOWN
            elif abs(moved_x) > 0:
                self.current_state = constants.LUMBERJACK_LEFT if moved_x < 0 else constants.LUMBERJACK_RIGHT

        self.update_animation()

    def attack(self):
        self.refresh_target_if_needed()
        if not self.target_tree:
            self.attacking = False
            return

        t = self.target_tree
        enemy_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        tronco = self.trunk_rect(t)
        tronco.inflate_ip(25, 25)

        dx = (t.x + t.size / 2) - (self.x + self.size / 2)
        dy = (t.y + t.size / 2) - (self.y + self.size / 2)
        dist = math.hypot(dx, dy)
        rango_ataque = (t.size + self.size) * 0.45

        in_range = enemy_rect.colliderect(tronco) or dist < rango_ataque

        if in_range and t.health > 0:
            self.attacking = True
            if self.cooldown_timer <= 0:
                t.take_damage(self.damage)
                t.add_fire(big=True)
                self.cooldown_timer = self.attack_cooldown
            else:
                self.cooldown_timer -= 1

            self.current_state = (
                constants.LUMBERJACK_ATTACK_LEFT if dx < 0 else constants.LUMBERJACK_ATTACK_RIGHT
            )
        else:
            self.attacking = False

        self.update_animation()

    def draw(self, screen):
        img = self.animations[self.current_state][self.animation_frame]
        screen.blit(img, (self.x, self.y))
