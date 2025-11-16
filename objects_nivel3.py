import pygame
import random

class Basura:
    def __init__(self, x, y, img):
        self.image = img
        self.rect = self.image.get_rect(topleft=(x, y))

    def dibujar(self, screen):
        screen.blit(self.image, self.rect)


def generar_basura(cantidad, img, width, height, world):
    basura = []
    min_dist = 60

    for _ in range(cantidad):
        placed = False
        intentos = 0

        while not placed and intentos < 300:
            intentos += 1
            x = random.randint(10, width - img.get_width() - 10)
            y = random.randint(10, height - img.get_height() - 10)

            rect = pygame.Rect(x, y, img.get_width(), img.get_height())

            if not world.zona_libre(rect):
                continue

            demasiado_cerca = False
            for b in basura:
                dx = rect.centerx - b.rect.centerx
                dy = rect.centery - b.rect.centery
                if abs(dx) < min_dist and abs(dy) < min_dist:
                    demasiado_cerca = True
                    break

            if demasiado_cerca:
                continue

            basura.append(Basura(x, y, img))
            placed = True

    return basura
