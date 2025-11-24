import pygame
import constants

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


def show_pause_menu(screen, from_level, callback_restart=None):

    # === CARGA DE IMÁGENES ===
    titulo_raw = pygame.image.load("assets/images/effects/titulo1.png").convert_alpha()
    menu_raw = pygame.image.load("assets/images/effects/menu1.png").convert_alpha()
    config_raw = pygame.image.load("assets/images/effects/config1.png").convert_alpha()
    reanudar_raw = pygame.image.load("assets/images/effects/reanu1.png").convert_alpha()
    reiniciar_raw = pygame.image.load("assets/images/effects/reini1.png").convert_alpha()

    # === ESCALAS DEFINITIVAS ===
    titulo_img = pygame.transform.scale(titulo_raw, (int(titulo_raw.get_width() * 0.75),
                                                     int(titulo_raw.get_height() * 0.75)))

    menu_img = pygame.transform.scale(menu_raw, (int(menu_raw.get_width() * 0.60),
                                                 int(menu_raw.get_height() * 0.60)))

    config_img = pygame.transform.scale(config_raw, (int(config_raw.get_width() * 0.60),
                                                     int(config_raw.get_height() * 0.60)))

    reanudar_img = pygame.transform.scale(reanudar_raw, (int(reanudar_raw.get_width() * 0.60),
                                                         int(reanudar_raw.get_height() * 0.60)))

    reiniciar_img = pygame.transform.scale(reiniciar_raw, (int(reiniciar_raw.get_width() * 0.60),
                                                           int(reiniciar_raw.get_height() * 0.60)))

    clock = pygame.time.Clock()
    WIDTH = constants.WIDTH
    HEIGHT = constants.HEIGHT

    blurred = make_blur(screen, WIDTH, HEIGHT)

    # === POSICIONES CENTRADAS ===
    titulo_y = 70
    separation = 75
    first_button_y = titulo_y + 130
    center_x = WIDTH // 2

    btn_menu = PauseButton(menu_img, (center_x, first_button_y))
    btn_conf = PauseButton(config_img, (center_x, first_button_y + separation))
    btn_rean = PauseButton(reanudar_img, (center_x, first_button_y + separation * 2))
    btn_reini = PauseButton(reiniciar_img, (center_x, first_button_y + separation * 3))

    titulo_rect = titulo_img.get_rect(center=(center_x, titulo_y))

    pause_active = True

    while pause_active:
        clock.tick(60)

        screen.blit(blurred, (0, 0))
        screen.blit(titulo_img, titulo_rect)

        btn_menu.draw(screen)
        btn_conf.draw(screen)
        btn_rean.draw(screen)
        btn_reini.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_active = False

            if btn_menu.is_clicked(event):
                return "menu_principal"

            if btn_conf.is_clicked(event):
                return "config"

            if btn_rean.is_clicked(event):
                pause_active = False

            if btn_reini.is_clicked(event):
                return "reiniciar"

    return "reanudar"
