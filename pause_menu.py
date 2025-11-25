import pygame
import constants
import config

pygame.init()

def make_blur(screen, width, height):
    snapshot = screen.copy()
    small = pygame.transform.smoothscale(snapshot, (width // 6, height // 6))
    blurred = pygame.transform.smoothscale(small, (width, height))
    return blurred

class PauseButton:
    def __init__(self, image, center_pos):
        self.image = image
        self.rect = self.image.get_rect(center=center_pos)
        self.hover_color = (255, 255, 0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect, 3)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

def load_pause_images():
    """Carga las imágenes según el idioma actual"""
    # ACTUALIZAR CONFIGURACIÓN ANTES DE CARGAR IMÁGENES
    config.update_global_config()
    
    # Cargar imágenes según idioma
    if config.lenguaje:  # Español
        menu_img = pygame.image.load("assets/images/effects/menu1.png").convert_alpha()
        reanudar_img = pygame.image.load("assets/images/effects/reanu1.png").convert_alpha()
        reiniciar_img = pygame.image.load("assets/images/effects/reini1.png").convert_alpha()
    else:  # Inglés
        # NOTA: Necesitarás crear estas imágenes o usar las existentes
        menu_img = pygame.image.load("assets/images/effects/menu1.png").convert_alpha()  # Cambiar por imagen en inglés
        reanudar_img = pygame.image.load("assets/images/effects/reanu1.png").convert_alpha()  # Cambiar por imagen en inglés
        reiniciar_img = pygame.image.load("assets/images/effects/reini1.png").convert_alpha()  # Cambiar por imagen en inglés

    # Imágenes que no cambian con idioma
    titulo_img = pygame.image.load("assets/images/effects/titulo1.png").convert_alpha()
    config_img = pygame.image.load("assets/images/effects/config1.png").convert_alpha()

    return {
        "titulo": titulo_img,
        "menu": menu_img,
        "config": config_img,
        "reanudar": reanudar_img,
        "reiniciar": reiniciar_img
    }

def scale_images(images):
    """Escala las imágenes a los tamaños deseados"""
    scaled = {}
    
    scaled["titulo"] = pygame.transform.scale(
        images["titulo"], 
        (int(images["titulo"].get_width() * 0.75),
         int(images["titulo"].get_height() * 0.75))
    )
    
    scaled["menu"] = pygame.transform.scale(
        images["menu"],
        (int(images["menu"].get_width() * 0.60),
         int(images["menu"].get_height() * 0.60))
    )
    
    scaled["config"] = pygame.transform.scale(
        images["config"],
        (int(images["config"].get_width() * 0.60),
         int(images["config"].get_height() * 0.60))
    )
    
    scaled["reanudar"] = pygame.transform.scale(
        images["reanudar"],
        (int(images["reanudar"].get_width() * 0.60),
         int(images["reanudar"].get_height() * 0.60))
    )
    
    scaled["reiniciar"] = pygame.transform.scale(
        images["reiniciar"],
        (int(images["reiniciar"].get_width() * 0.60),
         int(images["reiniciar"].get_height() * 0.60))
    )
    
    return scaled

def show_pause_menu(screen, from_level, callback_restart=None):
    # Cargar y escalar imágenes iniciales
    raw_images = load_pause_images()
    images = scale_images(raw_images)
    
    clock = pygame.time.Clock()
    WIDTH = constants.WIDTH
    HEIGHT = constants.HEIGHT

    blurred = make_blur(screen, WIDTH, HEIGHT)

    # === POSICIONES CENTRADAS ===
    titulo_y = 70
    separation = 75
    first_button_y = titulo_y + 130
    center_x = WIDTH // 2

    # Crear botones con imágenes escaladas
    btn_menu = PauseButton(images["menu"], (center_x, first_button_y))
    btn_conf = PauseButton(images["config"], (center_x, first_button_y + separation))
    btn_rean = PauseButton(images["reanudar"], (center_x, first_button_y + separation * 2))
    btn_reini = PauseButton(images["reiniciar"], (center_x, first_button_y + separation * 3))

    titulo_rect = images["titulo"].get_rect(center=(center_x, titulo_y))

    pause_active = True
    needs_reload = False  # Bandera para recargar imágenes

    while pause_active:
        clock.tick(60)

        # RECARGAR IMÁGENES SI ES NECESARIO (después de cambiar idioma)
        if needs_reload:
            raw_images = load_pause_images()
            images = scale_images(raw_images)
            
            # Actualizar botones con nuevas imágenes
            btn_menu.image = images["menu"]
            btn_conf.image = images["config"] 
            btn_rean.image = images["reanudar"]
            btn_reini.image = images["reiniciar"]
            
            needs_reload = False

        screen.blit(blurred, (0, 0))
        screen.blit(images["titulo"], titulo_rect)

        btn_menu.draw(screen)
        btn_conf.draw(screen)
        btn_rean.draw(screen)
        btn_reini.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.save_current_config()  # GUARDAR ANTES DE SALIR
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_active = False
    
            if btn_menu.is_clicked(event):
                # ENVIAR EVENTO PARA VOLVER AL MENÚ PRINCIPAL
                config.save_current_config()  # GUARDAR CONFIGURACIÓN
                menu_event = pygame.event.Event(config.OPEN_MENU_EVENT)
                pygame.time.delay(100)
                pygame.event.post(menu_event)
                return

            if btn_conf.is_clicked(event):
                # Abrir configuración y marcar para recargar imágenes al regresar
                config.open_config_menu(from_menu="pause")
                needs_reload = True  # Recargar imágenes después de config
                continue

            if btn_rean.is_clicked(event):
                pause_active = False

            if btn_reini.is_clicked(event):
                if callback_restart:
                    callback_restart()
                return

        # Verificar si llegó un evento para abrir el menú principal
        for ev in pygame.event.get(pump=False):
            if ev.type == config.OPEN_MENU_EVENT:
                config.save_current_config()  # GUARDAR ANTES DE SALIR
                return

    return