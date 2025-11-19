import pygame
import sys
import config
import constants
from button import Button
import select_character

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("niveles")

Fondo = pygame.image.load("imagenes/portada.png")
Fondo = pygame.transform.scale(Fondo, (constants.WIDTH, constants.HEIGHT))

title_img = pygame.image.load("imagenes/titulo1.png").convert_alpha()
title_img = pygame.transform.scale(
    title_img,
    (
        int(title_img.get_width() * 0.90),
        int(title_img.get_height() * 0.90)
    )
)
title_rect = title_img.get_rect(center=(constants.WIDTH // 2, 250))

def load_btn(name):
    return pygame.image.load(f"assets/images/effects/{name}.png").convert_alpha()

nivel1     = load_btn("nivel1")
nivel1R    = load_btn("nivel1R")
nivel2     = load_btn("nivel2")
nivel2R    = load_btn("nivel2R")
nivel3     = load_btn("nivel3")
nivel3R    = load_btn("nivel3R")

target_width = 200
def scale(img):
    h = int(img.get_height() * (target_width / img.get_width()))
    return pygame.transform.scale(img, (target_width, h))

nivel1  = scale(nivel1)
nivel1R = scale(nivel1R)
nivel2  = scale(nivel2)
nivel2R = scale(nivel2R)
nivel3  = scale(nivel3)
nivel3R = scale(nivel3R)

spacing = 70
total_width = target_width * 3 + spacing * 2
start_x = (constants.WIDTH - total_width) // 2
y_pos = constants.HEIGHT // 2 + 80

buttons = [
    {"normal": nivel1, "hover": nivel1R, "rect": pygame.Rect(start_x, y_pos, target_width, nivel1.get_height()), "lvl": 1},
    {"normal": nivel2, "hover": nivel2R, "rect": pygame.Rect(start_x + target_width + spacing, y_pos, target_width, nivel2.get_height()), "lvl": 2},
    {"normal": nivel3, "hover": nivel3R, "rect": pygame.Rect(start_x + (target_width + spacing) * 2, y_pos, target_width, nivel3.get_height()), "lvl": 3},
]

def niveles():
    # Reiniciar música del menú
    if pygame.mixer.get_init():
        pygame.mixer.music.load('music/m4.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    
    run = True
    while run:
        screen.blit(Fondo, (0, 0))
        screen.blit(title_img, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        for b in buttons:
            hovered = b["rect"].collidepoint(mouse_pos)
            img = b["hover"] if hovered else b["normal"]
            screen.blit(img, b["rect"])
            if hovered and click:
                pygame.time.delay(150)
                select_character.show(level=b["lvl"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()

if __name__ == "__main__":
    niveles()
