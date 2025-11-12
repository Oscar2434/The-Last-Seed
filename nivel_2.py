import pygame
import sys
import constants
from character_nivel_2 import Character
from world_nivel2 import World
import os

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("The last seed - Nivel 2")

# Cargar imágenes de victoria/derrota
victory_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'victoria.png')).convert_alpha()
defeat_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'derrota.png')).convert_alpha()

# Escalarlas al tamaño de la ventana
victory_img = pygame.transform.scale(victory_img, (constants.WIDTH, constants.HEIGHT))
defeat_img = pygame.transform.scale(defeat_img, (constants.WIDTH, constants.HEIGHT))

def main():
    clock = pygame.time.Clock()
    game_world = World(constants.WIDTH, constants.HEIGHT)

    # DEBUG: Verificar que se crearon muros
    print(f"Número de muros creados: {len(game_world.walls)}")

    # Personaje principal - posicionarlo en un área libre del laberinto
    # Personaje principal - volver a la posición original
    game_character = Character(constants.WIDTH // 2, constants.HEIGHT - 140)

    start_ticks = pygame.time.get_ticks()
    
    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"

        # Movimiento personaje
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game_character.move(dx=-5, dy=0, world=game_world)
        if keys[pygame.K_RIGHT]:
            game_character.move(dx=5, dy=0, world=game_world)
        if keys[pygame.K_UP]:
            game_character.move(dx=0, dy=-5, world=game_world)
        if keys[pygame.K_DOWN]:
            game_character.move(dx=0, dy=5, world=game_world)

        # Dibujar mundo y personaje
        game_world.draw(screen)
        game_character.draw(screen)

        # Tiempo restante
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(0, constants.LEVEL_TIME - seconds_passed)
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Tiempo: {remaining_time}", True, constants.BLACK)
        screen.blit(text, (10, 10))

        # Condición de victoria por tiempo
        if remaining_time == 0:
            screen.blit(victory_img, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            return "victory"

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()