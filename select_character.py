import pygame
import sys
import os
import config
import constants
import main
import nivel_2

pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Selección de personaje y dificultad")

def load_image(name, scale=1.0):
    path = os.path.join("imagenes", name)
    image = pygame.image.load(path).convert_alpha()
    if scale != 1.0:
        w, h = int(image.get_width() * scale), int(image.get_height() * scale)
        image = pygame.transform.scale(image, (w, h))
    return image

background = load_image("portada.png")
background = pygame.transform.scale(background, (constants.WIDTH, constants.HEIGHT))

title_img = load_image("seleccionPj.png")

boy_normal = load_image("seleccionNiño.png")
boy_hover = load_image("seleccionNiño2.png")
girl_normal = load_image("seleccionNiña.png")
girl_hover = load_image("seleccionNiña2.png")

normal_img = load_image("principiante.png", 0.45)
normal_hover = load_image("principianteR.png", 0.45)

hard_img = load_image("avanzado.png", 0.45)
hard_hover = load_image("avanzadoR.png", 0.45)

class HoverButton:
    def __init__(self, x, y, normal_img, hover_img, name):
        self.normal = normal_img
        self.hover = hover_img
        self.rect = self.normal.get_rect(center=(x, y))
        self.name = name
        self.hovered = False
        self.selected = False

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(pos)
        img = self.hover if (self.hovered or self.selected) else self.normal
        surface.blit(img, self.rect)

        clicked = False
        if self.hovered and pygame.mouse.get_pressed()[0]:
            self.selected = True
            clicked = True

        return clicked

class Button:
    def __init__(self, x, y, image, name):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.name = name
        self.selected = False

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        surface.blit(self.image, self.rect)
        clicked = False
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            self.selected = True
            clicked = True
        return clicked

def show(level=1):
    clock = pygame.time.Clock()
    selected_character = None
    selected_difficulty = None

    center_x = constants.WIDTH // 2

    title_rect = title_img.get_rect(midtop=(center_x, int(constants.HEIGHT * 0.001)))

    character_y = constants.HEIGHT // 2 + 60

    spacing_x = 230
    boy_x = center_x - spacing_x
    girl_x = center_x + spacing_x

    boy_btn = HoverButton(boy_x, character_y, boy_normal, boy_hover, "niño")
    girl_btn = HoverButton(girl_x, character_y, girl_normal, girl_hover, "niña")

    gap_center_x = center_x
    diff_top_y = character_y - int(constants.HEIGHT * 0.05)

    normal_btn = HoverButton(gap_center_x, diff_top_y, normal_img, normal_hover, "normal")

    hard_btn = HoverButton(
        gap_center_x,
        diff_top_y + normal_img.get_height() + int(constants.HEIGHT * 0.03),
        hard_img,
        hard_hover,
        "avanzado"
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))
        screen.blit(title_img, title_rect)

        if boy_btn.draw(screen):
            selected_character = "niño"
            boy_btn.selected = True
            girl_btn.selected = False

        if girl_btn.draw(screen):
            selected_character = "niña"
            girl_btn.selected = True
            boy_btn.selected = False

        if normal_btn.draw(screen):
            selected_difficulty = "normal"
            normal_btn.selected = True
            hard_btn.selected = False

        if hard_btn.draw(screen):
            selected_difficulty = "avanzado"
            hard_btn.selected = True
            normal_btn.selected = False

        if selected_character and selected_difficulty:
            config.selected_character = selected_character
            config.difficulty = selected_difficulty
            pygame.time.delay(250)

            # 🟥 DETENER música del menú antes de cambiar
            pygame.mixer.music.stop()

            # ------------------------------------------------
            # NIVEL 1 — música /m2.mp3
            # ------------------------------------------------
            if level == 1:
                pygame.mixer.music.load("music/m2.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                main.main()

            # ------------------------------------------------
            # NIVEL 2 — música /m1.mp3
            # ------------------------------------------------
            elif level == 2:
                pygame.mixer.music.load("music/m1.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                nivel_2.main()

            # ------------------------------------------------
            # NIVEL 3 — música /m3.mp3
            # ------------------------------------------------
            elif level == 3:
                pygame.mixer.music.load("music/m3.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)

                import nivel_3
                nivel_3.main()

            return

        pygame.display.update()
        clock.tick(60)
