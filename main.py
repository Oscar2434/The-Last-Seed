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
import config
import pause_menu
import desarrollador

pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("The Last Seed")

pause_icon_raw = pygame.image.load("assets/images/effects/pausa.png").convert_alpha()
pause_icon = pygame.transform.scale(pause_icon_raw, (35, 35))
pause_rect = pause_icon.get_rect(center=(constants.WIDTH // 2, 20))

game_paused = False

def get_localized_texts():
    if config.lenguaje:
        return {
            "objectives_title": "OBJETIVOS:",
            "objective1": "- Salvar el árbol central",
            "objective2": "- Mantener con vida al menos 3 árboles",
            "objective3": "- Sobrevive hasta que termine el tiempo"
        }
    else:
        return {
            "objectives_title": "OBJECTIVES:",
            "objective1": "- Save the central tree",
            "objective2": "- Keep at least 3 trees alive", 
            "objective3": "- Survive until time runs out"
        }

def draw_timer(screen, remaining_time, total_time, x, y):
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    time_text = f"{minutes:02d}:{seconds:02d}"
    
    font = pygame.font.Font(None, 40)
    
    if remaining_time > total_time * 0.6:
        color = constants.GREEN
    elif remaining_time > total_time * 0.3:
        color = constants.YELLOW
    else:
        color = constants.RED
    
    text_surface = font.render(time_text, True, color)
    
    bg_rect = text_surface.get_rect()
    bg_rect.x = x - 10
    bg_rect.y = y - 5
    bg_rect.width += 20
    bg_rect.height += 10
    
    pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect, border_radius=8)
    pygame.draw.rect(screen, (255, 255, 255, 100), bg_rect, 2, border_radius=8)
    
    screen.blit(text_surface, (x, y))
    
    if remaining_time < 10:
        pulse = (pygame.time.get_ticks() // 200) % 2
        if pulse == 0:
            glow_rect = bg_rect.copy()
            glow_rect.x -= 2
            glow_rect.y -= 2
            glow_rect.width += 4
            glow_rect.height += 4
            pygame.draw.rect(screen, (255, 50, 50, 100), glow_rect, 3, border_radius=10)

def show_tutorial_screens(screen, level_number):
    if config.lenguaje:
        tutorial_path = "assets/images/turorial en español"
    else:
        tutorial_path = "assets/images/tutorial en ingles"
    
    try:
        universal_img = pygame.image.load(os.path.join(tutorial_path, "universal.png")).convert_alpha()
        level_img = pygame.image.load(os.path.join(tutorial_path, f"N{level_number}.png")).convert_alpha()
        continue_img = pygame.image.load("assets/images/Buttons/continuar.png").convert_alpha()
        continue_img = pygame.transform.scale(continue_img, (int(continue_img.get_width() * 0.5), int(continue_img.get_height() * 0.5)))
    except pygame.error as e:
        print(f"Error cargando imágenes de tutorial: {e}")
        return False
    
    universal_img = pygame.transform.scale(universal_img, (constants.WIDTH, constants.HEIGHT))
    level_img = pygame.transform.scale(level_img, (constants.WIDTH, constants.HEIGHT))
    continue_rect = continue_img.get_rect(center=(750, 450))
    
    current_screen = 0
    screens = [universal_img, level_img]
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    current_screen += 1
                    if current_screen >= len(screens):
                        return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_rect.collidepoint(event.pos):
                    current_screen += 1
                    if current_screen >= len(screens):
                        return True
        
        screen.blit(screens[current_screen], (0, 0))
        screen.blit(continue_img, continue_rect)
        pygame.display.flip()
        clock.tick(60)
    
    return True

def show_victory_screen(screen):
    if config.lenguaje:
        victory_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'ganar.png')).convert_alpha()
    else:
        victory_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'ganarI.png')).convert_alpha()
    
    victory_img = pygame.transform.scale(victory_img, (constants.WIDTH, constants.HEIGHT))
    screen.blit(victory_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)

def show_defeat_screen(screen):
    if config.lenguaje:
        defeat_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'perder.png')).convert_alpha()
    else:
        defeat_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'perderI.png')).convert_alpha()
    
    defeat_img = pygame.transform.scale(defeat_img, (constants.WIDTH, constants.HEIGHT))
    screen.blit(defeat_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)

def main():
    global game_paused
    
    while True:
        config.update_global_config()
        music_playing = False
        
        def start_level_music():
            nonlocal music_playing
            if config.music and not music_playing:
                if pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                pygame.mixer.music.load('music/m2.mp3')
                pygame.mixer.music.set_volume(config.volume_master)
                pygame.mixer.music.play(-1)
                music_playing = True
        
        def stop_level_music():
            nonlocal music_playing
            if music_playing:
                pygame.mixer.music.stop()
                music_playing = False
        
        if not show_tutorial_screens(screen, 1):
            return "menu"
        
        start_level_music()

        clock = pygame.time.Clock()
        game_world = World(constants.WIDTH, constants.HEIGHT)
        game_character = Character(constants.WIDTH // 2, constants.HEIGHT - 100)
        central_tree = CentralTree(constants.WIDTH//2 - 40, constants.HEIGHT//2 - 40)
        game_world.central_tree = central_tree
        game_world.setup_enemy_slots(constants.LUMBERJACK_SIZE)

        dificultad = getattr(config, "difficulty", "normal")
        ajustes = constants.DIFFICULTY_SETTINGS.get(dificultad, constants.DIFFICULTY_SETTINGS["normal"])

        constants.ENEMY_SPEED = ajustes["ENEMY_SPEED"]
        constants.ENEMY_DAMAGE = ajustes["ENEMY_DAMAGE"]
        constants.LEVEL_TIME = ajustes["LEVEL_TIME"]
        max_enemies = ajustes["max_enemies"]
        spawn_delay = ajustes["spawn_delay"]
        total_time = ajustes["LEVEL_TIME"]

        lumberjacks = []
        resources = []
        spawn_timer = 0
        resource_timer = 0
        start_ticks = pygame.time.get_ticks()
        restart_requested = False
        player_resource = None

        while True:
            for event in pygame.event.get(pump=False):
                if event.type == config.OPEN_MENU_EVENT:
                    stop_level_music()
                    return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_level_music()
                    pygame.quit()
                    sys.exit()

                if event.type == config.OPEN_MENU_EVENT:
                    stop_level_music()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = True
                        result = pause_menu.show_pause_menu(screen, "level1")
                        game_paused = False
                        
                        if result == "restart":
                            restart_requested = True
                        elif result == "menu":
                            stop_level_music()
                            return
                        
                        if config.music and not pygame.mixer.music.get_busy():
                            start_level_music()

                    if event.key == pygame.K_e:
                        if player_resource is not None:
                            all_trees = [central_tree] + game_world.trees
                            
                            player_interact_rect = pygame.Rect(
                                game_character.x + desarrollador.HITBOX_ENTREGA_RECURSO['offset_x'],
                                game_character.y + desarrollador.HITBOX_ENTREGA_RECURSO['offset_y'],
                                desarrollador.HITBOX_ENTREGA_RECURSO['width'],
                                desarrollador.HITBOX_ENTREGA_RECURSO['height']
                            )
                            
                            closest_tree = min(all_trees, key=lambda t: ((t.x - game_character.x) ** 2 + (t.y - game_character.y) ** 2))
                            
                            if player_interact_rect.colliderect(closest_tree.get_attack_rect()):
                                game_character.start_throw_animation()
                                game_character.deliver_resource(closest_tree)
                                closest_tree.activate_protection()
                                player_resource = None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_rect.collidepoint(event.pos):
                        game_paused = True
                        result = pause_menu.show_pause_menu(screen, "level1")
                        game_paused = False
                        
                        if result == "restart":
                            restart_requested = True
                        elif result == "menu":
                            stop_level_music()
                            return
                        
                        if config.music and not pygame.mixer.music.get_busy():
                            start_level_music()

            if restart_requested:
                break

            if game_paused:
                continue

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                game_character.move(dx=-5, dy=0, world=game_world)
            if keys[pygame.K_RIGHT]:
                game_character.move(dx=5, dy=0, world=game_world)
            if keys[pygame.K_UP]:
                game_character.move(dx=0, dy=-5, world=game_world)
            if keys[pygame.K_DOWN]:
                game_character.move(dx=0, dy=5, world=game_world)

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
            
            if player_resource is None:
                for resource in resources[:]:
                    distance = ((resource.x - game_character.x) ** 2 + (resource.y - game_character.y) ** 2) ** 0.5
                    if distance <= 30:
                        player_resource = resource
                        resources.remove(resource)
                        break

            game_world.draw(screen)
            for resource in resources:
                resource.draw(screen)
            for enemy in lumberjacks:
                enemy.draw(screen)
            game_character.draw(screen)
            central_tree.draw(screen)
            for tree in game_world.trees:
                tree.draw(screen)
            
            if desarrollador.MOSTRAR_HITBOX:
                interact_rect = pygame.Rect(
                    game_character.x + desarrollador.HITBOX_ENTREGA_RECURSO['offset_x'],
                    game_character.y + desarrollador.HITBOX_ENTREGA_RECURSO['offset_y'],
                    desarrollador.HITBOX_ENTREGA_RECURSO['width'],
                    desarrollador.HITBOX_ENTREGA_RECURSO['height']
                )
                pygame.draw.rect(screen, desarrollador.COLOR_HITBOX_ENTREGA, interact_rect, 2)

            seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
            remaining_time = max(0, total_time - seconds_passed)
            
            draw_timer(screen, remaining_time, total_time, 10, 10)

            texts = get_localized_texts()
            
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
                texts["objectives_title"],
                texts["objective1"],
                texts["objective2"],
                texts["objective3"]
            ]

            y_offset = panel_y + 20
            for line in objetivos:
                t = font2.render(line, True, constants.BLACK)
                screen.blit(t, (panel_x + 15, y_offset))
                y_offset += 16

            vivos = sum(1 for t in game_world.trees if t.health > 0)

            if central_tree.health <= 0:
                show_defeat_screen(screen)
                game_paused = True
                result = pause_menu.show_pause_menu(screen, "level1")
                game_paused = False
                if result == "restart":
                    restart_requested = True
                elif result == "menu":
                    stop_level_music()
                    return
                else:
                    restart_requested = True

            if remaining_time == 0:
                if vivos >= 3 and central_tree.health > 0:
                    show_victory_screen(screen)
                else:
                    show_defeat_screen(screen)
                game_paused = True
                result = pause_menu.show_pause_menu(screen, "level1")
                game_paused = False
                if result == "restart":
                    restart_requested = True
                elif result == "menu":
                    stop_level_music()
                    return
                else:
                    restart_requested = True

            if vivos < 3 and central_tree.health > 0:
                show_defeat_screen(screen)
                game_paused = True
                result = pause_menu.show_pause_menu(screen, "level1")
                game_paused = False
                if result == "restart":
                    restart_requested = True
                elif result == "menu":
                    stop_level_music()
                    return
                else:
                    restart_requested = True

            screen.blit(pause_icon, pause_rect)

            if pause_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 255, 0), pause_rect, 2)

            pygame.display.flip()
            clock.tick(60)

        if restart_requested:
            continue

if __name__ == "__main__":
    main()