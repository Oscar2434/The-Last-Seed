import pygame
import sys
import constants
from character import Character
from world import World
from ambient import CentralTree
from enemy import Lumberjack
from resources import Resource
import random
import os
import config  # Importado para leer dificultad

pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("The Last Seed")

victory_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'ganar.png')).convert_alpha()
defeat_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'perder.png')).convert_alpha()
victory_img = pygame.transform.scale(victory_img, (constants.WIDTH, constants.HEIGHT))
defeat_img = pygame.transform.scale(defeat_img, (constants.WIDTH, constants.HEIGHT))

def main():
    clock = pygame.time.Clock()
    game_world = World(constants.WIDTH, constants.HEIGHT)
    game_character = Character(constants.WIDTH // 2, constants.HEIGHT - 100)
    central_tree = CentralTree(constants.WIDTH//2 - 40, constants.HEIGHT//2 - 40)
    game_world.central_tree = central_tree
    game_world.setup_enemy_slots(constants.LUMBERJACK_SIZE)

    # --- Configuración de dificultad dinámica ---
    dificultad = getattr(config, "difficulty", "normal")
    ajustes = constants.DIFFICULTY_SETTINGS.get(dificultad, constants.DIFFICULTY_SETTINGS["normal"])

    constants.ENEMY_SPEED = ajustes["ENEMY_SPEED"]
    constants.ENEMY_DAMAGE = ajustes["ENEMY_DAMAGE"]
    constants.LEVEL_TIME = ajustes["LEVEL_TIME"]
    max_enemies = ajustes["max_enemies"]
    spawn_delay = ajustes["spawn_delay"]

    lumberjacks = []
    resources = []
    spawn_timer = 0
    resource_timer = 0
    start_ticks = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game_character.move(dx=-5, dy=0, world=game_world)
        if keys[pygame.K_RIGHT]:
            game_character.move(dx=5, dy=0, world=game_world)
        if keys[pygame.K_UP]:
            game_character.move(dx=0, dy=-5, world=game_world)
        if keys[pygame.K_DOWN]:
            game_character.move(dx=0, dy=5, world=game_world)

        if keys[pygame.K_e]:
            all_trees = [central_tree] + game_world.trees
            closest_tree = min(all_trees, key=lambda t: ((t.x - game_character.x) ** 2 + (t.y - game_character.y) ** 2))
            distance = ((closest_tree.x - game_character.x) ** 2 + (closest_tree.y - game_character.y) ** 2) ** 0.5
            if distance <= 70:
                game_character.deliver_resource(closest_tree)

        if len(lumberjacks) < max_enemies:
            if spawn_timer <= 0:
                x = random.choice([0, constants.WIDTH-constants.LUMBERJACK_SIZE])
                y = random.choice([0, constants.HEIGHT-constants.LUMBERJACK_SIZE])
                lumberjacks.append(Lumberjack(x, y, game_world))
                spawn_timer = spawn_delay
            else:
                spawn_timer -= 1

        if resource_timer <= 0:
            rx = random.randint(0, constants.WIDTH-20)
            ry = random.randint(0, constants.HEIGHT-20)
            resources.append(Resource(rx, ry))
            resource_timer = 300
        else:
            resource_timer -= 1

        for enemy in lumberjacks:
            enemy.move_towards_target()
            enemy.attack()

        game_character.check_collect_resource(resources)
        game_world.draw(screen)
        for resource in resources:
            resource.draw(screen)
        for enemy in lumberjacks:
            enemy.draw(screen)
        central_tree.draw(screen)
        for tree in game_world.trees:
            tree.draw(screen)
        game_character.draw(screen)

        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(0, constants.LEVEL_TIME - seconds_passed)
        font = pygame.font.SysFont(None, 26)
        text = font.render(f"Tiempo: {remaining_time}", True, constants.BLACK)
        screen.blit(text, (10, 10))

        fade_duration = 1000
        elapsed_time = pygame.time.get_ticks() - start_ticks
        alpha_value = min(120, int((elapsed_time / fade_duration) * 120))

        panel_surface = pygame.Surface((250, 85), pygame.SRCALPHA)
        panel_surface.fill((255, 255, 255, alpha_value))
        panel_x = constants.WIDTH - 265
        panel_y = 15
        screen.blit(panel_surface, (panel_x, panel_y))

        font2 = pygame.font.SysFont(None, 18)
        objetivos = [
            "OBJETIVOS:",
            "- Salvar el árbol central",
            "- Mantener con vida al menos 3 árboles",
            "- Sobrevive hasta que termine el tiempo"
        ]

        y_offset = panel_y + 20
        for line in objetivos:
            t = font2.render(line, True, constants.BLACK)
            screen.blit(t, (panel_x + 15, y_offset))
            y_offset += 16

        vivos = sum(1 for t in game_world.trees if t.health > 0)
        if central_tree.health <= 0:
            screen.blit(defeat_img, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            return "defeat"

        if remaining_time == 0:
            if vivos >= 3 and central_tree.health > 0:
                screen.blit(victory_img, (0, 0))
            else:
                screen.blit(defeat_img, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            return "victory" if vivos >= 3 and central_tree.health > 0 else "defeat"

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
