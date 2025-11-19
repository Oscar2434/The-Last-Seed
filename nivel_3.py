import pygame
import sys
import os
import random
import constants
import config
import world_nivel3
import player_nivel3
import objects_nivel3
import snake_logic
import ui_nivel3

pygame.init()

def cargar_imagen_bolsa():
    base_path = os.path.join("assets", "images", "effects")
    try:
        img = pygame.image.load(os.path.join(base_path, "bolsa.png")).convert_alpha()
    except:
        img = pygame.image.load(os.path.join(base_path, "basura.png")).convert_alpha()
    return img

def main():
    # --- DETENER MÚSICA DEL MENÚ ---
    try:
        pygame.mixer.music.fadeout(800)
    except:
        pass

    # --- INICIAR MÚSICA DEL NIVEL 3 ---
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load("music/m3.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    except Exception as e:
        print("Error cargando música nivel 3:", e)

    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    clock = pygame.time.Clock()

    # Imágenes de victoria y derrota a pantalla completa
    victory_img = pygame.image.load(
        os.path.join("assets", "images", "effects", "ganar.png")
    ).convert_alpha()

    lose_img = pygame.image.load(
        os.path.join("assets", "images", "effects", "perder.png")
    ).convert_alpha()

    victory_img = pygame.transform.scale(victory_img, (constants.WIDTH, constants.HEIGHT))
    lose_img = pygame.transform.scale(lose_img, (constants.WIDTH, constants.HEIGHT))

    world = world_nivel3.World(constants.WIDTH, constants.HEIGHT)

    if getattr(config, "difficulty", "normal") == "avanzado":
        velocidad = 5
        objetivo = 20
    else:
        velocidad = 4
        objetivo = 12

    start_x = constants.WIDTH // 2 - constants.PERSONAJE // 2
    start_y = constants.HEIGHT - constants.PERSONAJE - 20
    jugador = player_nivel3.SnakePlayer(start_x, start_y, velocidad)

    bolsa_img = cargar_imagen_bolsa()
    bolsa_img = pygame.transform.scale(bolsa_img, (40, 40))

    basura = objects_nivel3.generar_basura(
        objetivo, bolsa_img, constants.WIDTH, constants.HEIGHT, world
    )

    inicio = pygame.time.get_ticks()
    recogidas = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        keys = pygame.key.get_pressed()
        jugador.mover_perpetuo(keys)

        cabeza = jugador.get_head_rect()

        nuevas_basuras = []
        for b in basura:
            if cabeza.colliderect(b.rect):
                recogidas += 1
                jugador.crecer()
            else:
                nuevas_basuras.append(b)
        basura = nuevas_basuras

        if snake_logic.fuera_de_limites(jugador, constants.WIDTH, constants.HEIGHT):
            screen.blit(lose_img, (0, 0))
            pygame.display.update()
            pygame.time.delay(2000)
            return "defeat"

        if snake_logic.colision_obstaculos(jugador, world.obstacles):
            screen.blit(lose_img, (0, 0))
            pygame.display.update()
            pygame.time.delay(2000)
            return "defeat"

        if recogidas >= objetivo and len(jugador.cola) > 0:
            cola_rect = jugador.cola[-1]
            if cola_rect.colliderect(world.bote.rect):
                screen.blit(victory_img, (0, 0))
                pygame.display.update()
                pygame.time.delay(2000)
                return "victory"

        tiempo = (pygame.time.get_ticks() - inicio) // 1000

        world.draw(screen)
        for b in basura:
            b.dibujar(screen)
        jugador.dibujar(screen, bolsa_img)
        ui_nivel3.dibujar_hud(screen, tiempo, recogidas, objetivo)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
