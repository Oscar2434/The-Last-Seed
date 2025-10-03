import pygame
import sys
import constants
from character import Character
from world import World
from central_tree import CentralTree
from enemy import Lumberjack
from resources import Resource
import random
import math

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("The last seed")

def get_enemy_slot(tree, enemy_size):
    
    angle = random.uniform(0, 360)   # ángulo aleatorio
    radius = random.randint(20, 40)  # radio aleatorio
    rad = math.radians(angle)

    cx = tree.x + tree.size // 2
    cy = tree.y + tree.size // 2

    tx = cx + int(math.cos(rad) * (tree.size // 2 + radius)) - enemy_size // 2
    ty = cy + int(math.sin(rad) * (tree.size // 2 + radius)) - enemy_size // 2

    return tx, ty

def main():
    clock = pygame.time.Clock()
    game_world = World(constants.WIDTH, constants.HEIGHT)

    # Personaje
    game_character = Character(constants.WIDTH // 2, constants.HEIGHT - 100)

    # Árbol central
    central_tree = CentralTree(constants.WIDTH//2 - 40, constants.HEIGHT//2 - 40)
    game_world.central_tree = central_tree

    # Configuración Nivel 1
    difficulty = "easy"
    config = constants.LEVEL1_CONFIG[difficulty]
    max_enemies = config["max_enemies"]
    spawn_delay = config["spawn_delay"]

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
            game_character.deliver_resource(central_tree)

        # Spawn enemigos
        if len(lumberjacks) < max_enemies:
            if spawn_timer <= 0:
                x = random.choice([0, constants.WIDTH-constants.LUMBERJACK_SIZE])
                y = random.choice([0, constants.HEIGHT-constants.LUMBERJACK_SIZE])
                target_pos = get_enemy_slot(central_tree, constants.LUMBERJACK_SIZE)
                lumberjacks.append(Lumberjack(x, y, target_pos))
                spawn_timer = spawn_delay
            else:
                spawn_timer -= 1

        # Spawn recursos
        if resource_timer <= 0:
            rx = random.randint(0, constants.WIDTH-20)
            ry = random.randint(0, constants.HEIGHT-20)
            resources.append(Resource(rx, ry))
            resource_timer = 300
        else:
            resource_timer -= 1

        # Movimiento enemigos y ataque
        for enemy in lumberjacks:
            enemy.move_towards(central_tree)
            enemy.attack(central_tree)

        # Recolección recursos
        game_character.check_collect_resource(resources)

        # Dibujar
        game_world.draw(screen)
        for resource in resources:
            resource.draw(screen)
        for enemy in lumberjacks:
            enemy.draw(screen)
        central_tree.draw(screen)
        game_character.draw(screen)

        # Tiempo restante
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(0, constants.LEVEL_TIME - seconds_passed)
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Tiempo: {remaining_time}", True, constants.BLACK)
        screen.blit(text, (10, 10))

        # Condiciones de fin
        if central_tree.health <= 0:
            return "defeat"
        elif remaining_time == 0:
            return "victory"

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
