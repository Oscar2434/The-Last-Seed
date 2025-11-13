import pygame
import os
import constants
import config

class SnakePlayer:
    def __init__(self, x, y, velocidad):
        self.x = x
        self.y = y
        self.speed = velocidad

        self.dir_x = 0
        self.dir_y = 0
        self.movement_enabled = False

        self.positions = [(self.x, self.y)]
        self.segment_steps = 8
        self.cola_length = 0
        self.cola = []

        if config.selected_character == "niño":
            personaje = "nino.png"
        else:
            personaje = "Eli.png"

        path = os.path.join("assets", "images", "character", personaje)
        self.sprite_sheet = pygame.image.load(path).convert_alpha()
        self.sprite_sheet = pygame.transform.scale(
            self.sprite_sheet,
            (constants.F_SIZE * 4, constants.F_SIZE * 4)
        )

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.anim_row = 0

    def get_head_rect(self):
        return pygame.Rect(self.x, self.y, constants.PERSONAJE, constants.PERSONAJE)

    def _set_direction_from_keys(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.dir_x, self.dir_y = 0, -1
            self.anim_row = 3
            return True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.dir_x, self.dir_y = 0, 1
            self.anim_row = 0
            return True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.dir_x, self.dir_y = -1, 0
            self.anim_row = 1
            return True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.dir_x, self.dir_y = 1, 0
            self.anim_row = 2
            return True
        return False

    def mover_perpetuo(self, keys):
        if not self.movement_enabled:
            if self._set_direction_from_keys(keys):
                self.movement_enabled = True
            return

        self._set_direction_from_keys(keys)

        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

        self.positions.insert(0, (self.x, self.y))
        max_len = (self.cola_length + 1) * self.segment_steps + 1
        if len(self.positions) > max_len:
            self.positions.pop()

    def crecer(self):
        self.cola_length += 1

    def dibujar(self, screen, bolsa_img):
        now = pygame.time.get_ticks()
        if now - self.last_update > constants.DELAY_FPS:
            self.frame = (self.frame + 1) % 4
            self.last_update = now

        frame_rect = pygame.Rect(
            self.frame * constants.F_SIZE,
            self.anim_row * constants.F_SIZE,
            constants.F_SIZE,
            constants.F_SIZE
        )

        img = self.sprite_sheet.subsurface(frame_rect)
        img = pygame.transform.scale(img, (constants.PERSONAJE, constants.PERSONAJE))
        screen.blit(img, (self.x, self.y))

        self.cola = []
        for i in range(self.cola_length):
            idx = (i + 1) * self.segment_steps
            if idx < len(self.positions):
                sx, sy = self.positions[idx]
                cx = sx + constants.PERSONAJE // 2
                cy = sy + constants.PERSONAJE // 2 + 4
                rect = bolsa_img.get_rect(center=(cx, cy))
                screen.blit(bolsa_img, rect)
                self.cola.append(rect)
