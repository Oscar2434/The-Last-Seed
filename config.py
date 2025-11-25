import pygame
import constants

pygame.init()

# EVENTOS PERSONALIZADOS
OPEN_MENU_EVENT = pygame.USEREVENT + 1
OPEN_CONFIG_EVENT = pygame.USEREVENT + 2
OPEN_LEVEL_EVENT = pygame.USEREVENT + 3

lenguaje = True
music = True
volume_master = 0.5
selected_character = None
difficulty = None

BACKGROUND_CONFIG = "assets/images/effects/portada.png"
TITLE_IMAGE       = "assets/images/effects/titulo1.png"
CONFIG_ICON       = "assets/images/effects/config1.png"
MUSIC_ICON        = "assets/images/effects/musicaL.png"
FLAG_ES           = "assets/images/effects/españa.png"
FLAG_EN           = "assets/images/effects/inglaterra .png"   
EXIT_BUTTON       = "assets/images/effects/salida.png"

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

    running = True
    while running:
        screen.blit(bg, (0, 0))
        screen.blit(title_img, title_rect)
        screen.blit(config_icon, config_rect)
        screen.blit(flag_es, flag_es_rect)
        screen.blit(flag_en, flag_en_rect)

        mx, my = pygame.mouse.get_pos()
        if flag_es_rect.collidepoint(mx, my):
            draw_hover(screen, flag_es_rect)
        if flag_en_rect.collidepoint(mx, my):
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

        screen.blit(exit_img, exit_rect)

        if exit_rect.collidepoint(mx, my):
            draw_hover(screen, exit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == OPEN_MENU_EVENT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if flag_es_rect.collidepoint(mx, my):
                    lenguaje = True
                if flag_en_rect.collidepoint(mx, my):
                    lenguaje = False

                if bar_x <= mx <= bar_x + bar_width and bar_y <= my <= bar_y + bar_height:
                    volume_master = (mx - bar_x) / bar_width
                    volume_master = max(0, min(volume_master, 1))

                if exit_rect.collidepoint(mx, my):
                    pygame.time.delay(100)
                    return

        pygame.display.update()

    return