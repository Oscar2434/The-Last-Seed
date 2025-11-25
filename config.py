import pygame
import constants
import config_manager

pygame.init()

# EVENTOS PERSONALIZADOS
OPEN_MENU_EVENT = pygame.USEREVENT + 1
OPEN_CONFIG_EVENT = pygame.USEREVENT + 2
OPEN_LEVEL_EVENT = pygame.USEREVENT + 3

# Cargar configuración al inicio
config_data = config_manager.load_config()

# Variables globales actualizadas automáticamente
lenguaje = config_data["lenguaje"]
music = config_data["music"]
volume_master = config_data["volume_master"]
selected_character = config_data["selected_character"]
difficulty = config_data["difficulty"]

BACKGROUND_CONFIG = "assets/images/effects/portada.png"
TITLE_IMAGE       = "assets/images/effects/titulo1.png"
CONFIG_ICON       = "assets/images/effects/config1.png"
MUSIC_ICON        = "assets/images/effects/musicaL.png"
FLAG_ES           = "assets/images/effects/españa.png"
FLAG_EN           = "assets/images/effects/inglaterra .png"   
EXIT_BUTTON       = "assets/images/effects/salida.png"

def update_global_config():
    """Actualiza las variables globales con la configuración actual"""
    global lenguaje, music, volume_master, selected_character, difficulty
    current_config = config_manager.load_config()
    lenguaje = current_config["lenguaje"]
    music = current_config["music"]
    volume_master = current_config["volume_master"]
    selected_character = current_config["selected_character"]
    difficulty = current_config["difficulty"]

def save_current_config():
    """Guarda la configuración actual"""
    config_data = {
        "lenguaje": lenguaje,
        "music": music,
        "volume_master": volume_master,
        "selected_character": selected_character,
        "difficulty": difficulty
    }
    return config_manager.save_config(config_data)

def update_music_volume():
    """Actualiza el volumen de la música en tiempo real"""
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.set_volume(volume_master)

def load_image(path, scale=1.0):
    img = pygame.image.load(path).convert_alpha()
    if scale != 1.0:
        w, h = img.get_width(), img.get_height()
        img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
    return img

def draw_hover(screen, rect):
    pygame.draw.rect(screen, (255, 255, 0), rect.inflate(10, 10), 3)

def open_config_menu(from_menu="main"):
    global lenguaje, music, volume_master
    
    # Actualizar configuración global al abrir
    update_global_config()
    
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

    # Cargar imágenes escaladas
    bg          = load_image(BACKGROUND_CONFIG)
    title_img   = load_image(TITLE_IMAGE, 0.85)
    config_icon = load_image(CONFIG_ICON, 0.70)
    exit_img    = load_image(EXIT_BUTTON, 0.30)
    music_icon  = load_image(MUSIC_ICON, 0.75)
    flag_es     = load_image(FLAG_ES, 0.65)
    flag_en     = load_image(FLAG_EN, 0.65)

    # Posiciones generales
    title_rect  = title_img.get_rect(center=(constants.WIDTH // 2, 75))
    config_rect = config_icon.get_rect(center=(constants.WIDTH // 2, 150))

    flag_es_rect = flag_es.get_rect(center=(constants.WIDTH // 2 - 70, 245))
    flag_en_rect = flag_en.get_rect(center=(constants.WIDTH // 2 + 70, 245))

    bar_width  = 220
    bar_height = 32
    bar_y = 300

    icon_w = music_icon.get_width()
    separation = 7

    block_width = icon_w + separation + bar_width
    start_x = (constants.WIDTH - block_width) // 2 - 15

    music_rect = music_icon.get_rect(center=(
        start_x + icon_w // 2,
        bar_y + bar_height // 2
    ))

    bar_x = start_x + icon_w + separation
    exit_rect = exit_img.get_rect(center=(constants.WIDTH // 2, 395))

    # Variables para arrastre de barra
    dragging_volume = False

    running = True
    while running:
        screen.blit(bg, (0, 0))
        screen.blit(title_img, title_rect)
        screen.blit(config_icon, config_rect)
        screen.blit(flag_es, flag_es_rect)
        screen.blit(flag_en, flag_en_rect)

        mx, my = pygame.mouse.get_pos()
        
        # Resaltar bandera seleccionada
        if lenguaje:  # Español seleccionado
            draw_hover(screen, flag_es_rect)
        else:  # Inglés seleccionado
            draw_hover(screen, flag_en_rect)
            
        # Resaltar al hover
        if flag_es_rect.collidepoint(mx, my) and not lenguaje:
            draw_hover(screen, flag_es_rect)
        if flag_en_rect.collidepoint(mx, my) and lenguaje:
            draw_hover(screen, flag_en_rect)

        screen.blit(music_icon, music_rect)

        # Barra de volumen (fondo)
        pygame.draw.rect(screen, (60, 60, 60),
                         (bar_x, bar_y, bar_width, bar_height),
                         border_radius=5)

        # Barra activa
        current_width = int(bar_width * volume_master)
        pygame.draw.rect(screen, (0, 180, 0),
                         (bar_x, bar_y, current_width, bar_height),
                         border_radius=5)

        # Indicador de volumen actual
        font = pygame.font.Font(None, 24)
        volume_text = f"{int(volume_master * 100)}%"
        text_surf = font.render(volume_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(bar_x + bar_width // 2, bar_y - 20))
        screen.blit(text_surf, text_rect)

        screen.blit(exit_img, exit_rect)

        if exit_rect.collidepoint(mx, my):
            draw_hover(screen, exit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_current_config()  # Guardar antes de salir
                pygame.quit()
                exit()

            if event.type == OPEN_MENU_EVENT:
                save_current_config()  # Guardar al salir del menú
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if flag_es_rect.collidepoint(mx, my):
                    lenguaje = True
                    save_current_config()  # Guardar inmediatamente
                    
                if flag_en_rect.collidepoint(mx, my):
                    lenguaje = False
                    save_current_config()  # Guardar inmediatamente

                if bar_x <= mx <= bar_x + bar_width and bar_y <= my <= bar_y + bar_height:
                    dragging_volume = True
                    volume_master = (mx - bar_x) / bar_width
                    volume_master = max(0, min(volume_master, 1))
                    save_current_config()  # Guardar inmediatamente
                    update_music_volume()  # Actualizar volumen en tiempo real

                if exit_rect.collidepoint(mx, my):
                    pygame.time.delay(150)
                    save_current_config()  # Guardar al salir
                    return

            if event.type == pygame.MOUSEBUTTONUP:
                dragging_volume = False

            if event.type == pygame.MOUSEMOTION:
                if dragging_volume:
                    volume_master = (mx - bar_x) / bar_width
                    volume_master = max(0, min(volume_master, 1))
                    save_current_config()  # Guardar inmediatamente
                    update_music_volume()  # Actualizar volumen en tiempo real

        pygame.display.update()

    save_current_config()  # Guardar por si acaso
    return