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
    """Carga imágenes desde assets/images con manejo de errores"""
    # Primero intentar en assets/images
    path = os.path.join("assets", "images", name)
    if not os.path.exists(path):
        # Si no existe, intentar en la carpeta raíz de imágenes
        path = os.path.join("imagenes", name)
        if not os.path.exists(path):
            # Si tampoco existe, mostrar error pero continuar
            print(f"Advertencia: No se pudo encontrar la imagen: {name}")
            # Crear una imagen de placeholder
            surf = pygame.Surface((100, 100))
            surf.fill((255, 0, 255))  # Color magenta para indicar error
            return surf
    
    image = pygame.image.load(path).convert_alpha()
    if scale != 1.0:
        w, h = int(image.get_width() * scale), int(image.get_height() * scale)
        image = pygame.transform.scale(image, (w, h))
    return image

def load_localized_images():
    """Carga las imágenes según el idioma actual"""
    config.update_global_config()  # Actualizar configuración primero
    
    if config.lenguaje:  # Español
        title_img = load_image("seleccionPj.png")
        normal_img = load_image("principiante.png", 0.45)
        normal_hover = load_image("principianteR.png", 0.45)
        hard_img = load_image("avanzado.png", 0.45)
        hard_hover = load_image("avanzadoR.png", 0.45)
    else:  # Inglés
        # Cargar imágenes en inglés desde la subcarpeta Selec
        title_img = load_image(os.path.join("Selec", "selección de personaje INGLES.png"))
        normal_img = load_image(os.path.join("Selec", "principiante INGLES.png"), 0.45)
        normal_hover = load_image(os.path.join("Selec", "principiante INGLES ELEGIR.png"), 0.45)
        hard_img = load_image(os.path.join("Selec", "avanzado INGLES.png"), 0.45)
        hard_hover = load_image(os.path.join("Selec", "avanzado INGLES ELEGIR.png"), 0.45)
    
    return title_img, normal_img, normal_hover, hard_img, hard_hover

# Cargar imágenes que no cambian con el idioma
background = load_image("portada.png")
background = pygame.transform.scale(background, (constants.WIDTH, constants.HEIGHT))

boy_normal = load_image("Dan sin flor.png")
boy_hover = load_image("Dan con flor.png")
girl_normal = load_image("Eli sin flor.png")
girl_hover = load_image("Eli con flor.png")

# Cargar imagen de retorno y escalarla
return_scale = 0.50  # Variable para escalar el botón de retorno
return_img = load_image("retorno.png", return_scale)

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
        self.last_click_time = 0  # Control de tiempo entre clics

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        surface.blit(self.image, self.rect)
        clicked = False
        
        current_time = pygame.time.get_ticks()
        if (self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] and 
            current_time - self.last_click_time > 300):  # 300ms entre clics
            self.selected = True
            clicked = True
            self.last_click_time = current_time
            
        return clicked

def show(level=1):
    clock = pygame.time.Clock()
    selected_character = None
    selected_difficulty = None
    ignore_first_click = True  # Bandera para ignorar clics al entrar

    center_x = constants.WIDTH // 2

    # Cargar imágenes localizadas
    title_img, normal_img, normal_hover, hard_img, hard_hover = load_localized_images()
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

    # Botón de retorno
    return_btn = Button(50, 430, return_img, "retorno")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))
        screen.blit(title_img, title_rect)

        # Si es el primer clic después de entrar, ignorarlo
        if ignore_first_click:
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
            return "nivels"  # CORRECCIÓN: Regresar a niveles en lugar de menú

        # Verificar clics en botones de personaje y dificultad
        character_clicked = False
        difficulty_clicked = False
        
        if boy_btn.draw(screen) and not ignore_first_click:
            selected_character = "niño"
            boy_btn.selected = True
            girl_btn.selected = False
            character_clicked = True

        if girl_btn.draw(screen) and not ignore_first_click:
            selected_character = "niña"
            girl_btn.selected = True
            boy_btn.selected = False
            character_clicked = True

        if normal_btn.draw(screen) and not ignore_first_click:
            selected_difficulty = "normal"
            normal_btn.selected = True
            hard_btn.selected = False
            difficulty_clicked = True

        if hard_btn.draw(screen) and not ignore_first_click:
            selected_difficulty = "avanzado"
            hard_btn.selected = True
            normal_btn.selected = False
            difficulty_clicked = True

        # Si se hizo clic en algún botón, limpiar eventos
        if (character_clicked or difficulty_clicked) and not ignore_first_click:
            pygame.event.clear(pygame.MOUSEBUTTONDOWN)
            pygame.event.clear(pygame.MOUSEBUTTONUP)

        if selected_character and selected_difficulty:
            config.selected_character = selected_character
            config.difficulty = selected_difficulty
            # GUARDAR CONFIGURACIÓN INMEDIATAMENTE
            config.save_current_config()
            pygame.time.delay(250)

            # 🟥 DETENER música del menú antes de cambiar
            pygame.mixer.music.stop()

            # ------------------------------------------------
            # NIVEL 1 — música /m2.mp3
            # ------------------------------------------------
            if level == 1:
                pygame.mixer.music.load("music/m2.mp3")
                pygame.mixer.music.set_volume(config.volume_master)
                pygame.mixer.music.play(-1)
                result = main.main()  # CAPTURAR EL RETORNO
                if result == "menu" or result == "to_menu":
                    # Enviar evento para reiniciar música del menú
                    menu_event = pygame.event.Event(config.OPEN_MENU_EVENT)
                    pygame.event.post(menu_event)
                    return "menu"  # PROPAGAR EL RETORNO

            # ------------------------------------------------
            # NIVEL 2 — música /m1.mp3
            # ------------------------------------------------
            elif level == 2:
                pygame.mixer.music.load("music/m1.mp3")
                pygame.mixer.music.set_volume(config.volume_master)
                pygame.mixer.music.play(-1)
                result = nivel_2.main()  # CAPTURAR EL RETORNO
                if result == "menu" or result == "to_menu":
                    # Enviar evento para reiniciar música del menú
                    menu_event = pygame.event.Event(config.OPEN_MENU_EVENT)
                    pygame.event.post(menu_event)
                    return "menu"  # PROPAGAR EL RETORNO

            # ------------------------------------------------
            # NIVEL 3 — música /m3.mp3
            # ------------------------------------------------
            elif level == 3:
                pygame.mixer.music.load("music/m3.mp3")
                pygame.mixer.music.set_volume(config.volume_master)
                pygame.mixer.music.play(-1)

                import nivel_3
                result = nivel_3.main()  # CAPTURAR EL RETORNO
                if result == "menu" or result == "to_menu":
                    # Enviar evento para reiniciar música del menú
                    menu_event = pygame.event.Event(config.OPEN_MENU_EVENT)
                    pygame.event.post(menu_event)
                    return "menu"  # PROPAGAR EL RETORNO

            # Si llegamos aquí, el nivel terminó pero no retornó "menu"
            # En ese caso, volvemos al menú principal
            # Enviar evento para reiniciar música del menú
            menu_event = pygame.event.Event(config.OPEN_MENU_EVENT)
            pygame.event.post(menu_event)
            return "menu"

        pygame.display.update()
        clock.tick(60)