import pygame
import sys
import os
import config
import constants
import select_character

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

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

def load_image(name, scale=1.0):
    path = os.path.join("imagenes", name)
    image = pygame.image.load(path).convert_alpha()
    if scale != 1.0:
        w, h = int(image.get_width() * scale), int(image.get_height() * scale)
        image = pygame.transform.scale(image, (w, h))
    return image

# Cargar imagen de retorno y escalarla
return_scale = 0.5  # Variable para escalar el botón de retorno
return_img = load_image("retorno.png", return_scale)

class ReturnButton:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.last_click_time = 0  # Control de tiempo entre clics

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        surface.blit(self.image, self.rect)
        clicked = False
        
        current_time = pygame.time.get_ticks()
        if (self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] and 
            current_time - self.last_click_time > 300):  # 300ms entre clics
            clicked = True
            self.last_click_time = current_time
            
        return clicked

def load_level_buttons():
    """Carga los botones de niveles según el idioma actual"""
    config.update_global_config()
    
    if config.lenguaje:  # Español
        nivel1 = load_btn("nivel1")
        nivel1R = load_btn("nivel1R")
        nivel2 = load_btn("nivel2")
        nivel2R = load_btn("nivel2R")
        nivel3 = load_btn("nivel3")
        nivel3R = load_btn("nivel3R")
    else:  # Inglés
        nivel1 = load_btn("level1")
        nivel1R = load_btn("level1R")
        nivel2 = load_btn("level2")
        nivel2R = load_btn("level2R")
        nivel3 = load_btn("level3")
        nivel3R = load_btn("level3R")
    
    return nivel1, nivel1R, nivel2, nivel2R, nivel3, nivel3R

def create_buttons():
    """Crea y escala los botones según el idioma actual"""
    nivel1, nivel1R, nivel2, nivel2R, nivel3, nivel3R = load_level_buttons()
    
    target_width = 200
    def scale(img):
        h = int(img.get_height() * (target_width / img.get_width()))
        return pygame.transform.scale(img, (target_width, h))

    nivel1 = scale(nivel1)
    nivel1R = scale(nivel1R)
    nivel2 = scale(nivel2)
    nivel2R = scale(nivel2R)
    nivel3 = scale(nivel3)
    nivel3R = scale(nivel3R)

    spacing = 70
    total_width = target_width * 3 + spacing * 2
    start_x = (constants.WIDTH - total_width) // 2
    y_pos = constants.HEIGHT // 2

    buttons = [
        {"normal": nivel1, "hover": nivel1R, "rect": pygame.Rect(start_x, y_pos, target_width, nivel1.get_height()), "lvl": 1},
        {"normal": nivel2, "hover": nivel2R, "rect": pygame.Rect(start_x + target_width + spacing, y_pos, target_width, nivel2.get_height()), "lvl": 2},
        {"normal": nivel3, "hover": nivel3R, "rect": pygame.Rect(start_x + (target_width + spacing) * 2, y_pos, target_width, nivel3.get_height()), "lvl": 3},
    ]
    
    return buttons

def niveles():
    run = True
    needs_reload = True  # Bandera para recargar botones cuando cambie el idioma
    ignore_first_click = True  # Nueva bandera para ignorar el primer clic
    
    # Botón de retorno
    return_btn = ReturnButton(50, 430, return_img)
    
    while run:
        # ACTUALIZAR CONFIGURACIÓN
        config.update_global_config()
        
        # Actualizar título de ventana según idioma
        if config.lenguaje:
            pygame.display.set_caption("Niveles")
        else:
            pygame.display.set_caption("Levels")
        
        # Recargar botones si es necesario (después de cambiar idioma)
        if needs_reload:
            buttons = create_buttons()
            needs_reload = False
        
        screen.blit(Fondo, (0, 0))
        screen.blit(title_img, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        
        # Si es el primer clic después de entrar, ignorarlo
        if ignore_first_click:
            click = False
            # Solo ignorar el primer clic que ocurra después de un breve período
            if pygame.time.get_ticks() > 300:  # 300ms después de entrar
                ignore_first_click = False

        # Dibujar y verificar botón de retorno
        return_clicked = return_btn.draw(screen)
        if return_clicked and not ignore_first_click:
            pygame.time.delay(150)
            # LIMPIAR EVENTOS DE MOUSE ANTES DE CAMBIAR DE PANTALLA
            pygame.event.clear(pygame.MOUSEBUTTONDOWN)
            pygame.event.clear(pygame.MOUSEBUTTONUP)
            return "menu"

        for b in buttons:
            hovered = b["rect"].collidepoint(mouse_pos)
            img = b["hover"] if hovered else b["normal"]
            screen.blit(img, b["rect"])

            if hovered and click and not ignore_first_click:
                pygame.time.delay(150)
                # LIMPIAR EVENTOS DE MOUSE ANTES DE CAMBIAR DE PANTALLA
                pygame.event.clear(pygame.MOUSEBUTTONDOWN)
                pygame.event.clear(pygame.MOUSEBUTTONUP)
                resultado = select_character.show(level=b["lvl"])

                if resultado == "menu":
                    return "menu"
                if resultado == "config":
                    config_result = config.open_config_menu(from_menu="niveles")
                    if config_result == "menu":
                        return "menu"
                    # Marcar para recargar botones después de cambiar idioma en configuración
                    needs_reload = True
                    # Reactivar la bandera de ignorar primer clic al regresar
                    ignore_first_click = True
                    continue
                elif resultado == "reiniciar":
                    return "reiniciar"
                elif resultado == "quit":
                    config.save_current_config()  # GUARDAR ANTES DE SALIR
                    pygame.quit()
                    sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.save_current_config()  # GUARDAR ANTES DE SALIR
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        pygame.display.update()