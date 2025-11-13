import pygame
import constants

pygame.font.init()
fuente = pygame.font.SysFont(None, 28)
fuente_grande = pygame.font.SysFont(None, 60)

def dibujar_hud(screen, tiempo, recogidas, objetivo):
    texto1 = fuente.render(f"Tiempo: {tiempo}s", True, constants.WHITE)
    texto2 = fuente.render(f"Basura: {recogidas}/{objetivo}", True, constants.WHITE)
    screen.blit(texto1, (20, 20))
    screen.blit(texto2, (20, 55))

def mensaje_final(screen, texto):
    msg = fuente_grande.render(texto, True, constants.WHITE)
    rect = msg.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2))
    screen.blit(msg, rect)
    pygame.display.update()
    pygame.time.delay(2000)
