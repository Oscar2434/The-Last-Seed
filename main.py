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

# === IMPORTACIÓN DEL MENÚ DE PAUSA ===
import pause_menu

pygame.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("The Last Seed")

victory_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'ganar.png')).convert_alpha()
defeat_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'perder.png')).convert_alpha()
victory_img = pygame.transform.scale(victory_img, (constants.WIDTH, constants.HEIGHT))
defeat_img = pygame.transform.scale(defeat_img, (constants.WIDTH, constants.HEIGHT))

# === BOTÓN DE PAUSA (ahora reducido) ===
pause_icon_raw = pygame.image.load("assets/images/effects/pausa.png").convert_alpha()
pause_icon = pygame.transform.scale(pause_icon_raw, (35, 35))
pause_rect = pause_icon.get_rect(center=(constants.WIDTH // 2, 20))

# Variable para controlar si estamos en pausa
game_paused = False

def get_localized_texts():
    """Retorna los textos traducidos según el idioma configurado"""
    if config.lenguaje:  # Español
        return {
            "time": "Tiempo: {}",
            "objectives_title": "OBJETIVOS:",
            "objective1": "- Salvar el árbol central",
            "objective2": "- Mantener con vida al menos 3 árboles",
            "objective3": "- Sobrevive hasta que termine el tiempo"
        }
    else:  # Inglés
        return {
            "time": "Time: {}",
            "objectives_title": "OBJECTIVES:",
            "objective1": "- Save the central tree",
            "objective2": "- Keep at least 3 trees alive", 
            "objective3": "- Survive until time runs out"
        }

def show_tutorial_screens(screen, level_number):
    """Muestra las pantallas de tutorial para el nivel especificado"""
    # Cargar imágenes según idioma
    if config.lenguaje:  # Español
        tutorial_path = "assets/images/turorial en español"
    else:  # Inglés
        tutorial_path = "assets/images/tutorial en ingles"
    
    # Cargar imágenes
    try:
        universal_img = pygame.image.load(os.path.join(tutorial_path, "universal.png")).convert_alpha()
        level_img = pygame.image.load(os.path.join(tutorial_path, f"N{level_number}.png")).convert_alpha()
        continue_img = pygame.image.load("assets/images/Buttons/continuar.png").convert_alpha()
        continue_img = pygame.transform.scale(continue_img, (int(continue_img.get_width() * 0.5), int(continue_img.get_height() * 0.5)))

    except pygame.error as e:
        print(f"Error cargando imágenes de tutorial: {e}")
        return False
    
    # Escalar imágenes al tamaño de la pantalla
    universal_img = pygame.transform.scale(universal_img, (constants.WIDTH, constants.HEIGHT))
    level_img = pygame.transform.scale(level_img, (constants.WIDTH, constants.HEIGHT))
    
    # Posición del botón continuar
    continue_rect = continue_img.get_rect(center=(750, 450))
    
    # Mostrar pantalla universal primero
    current_screen = 0  # 0 = universal, 1 = nivel específico
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
        
        # Dibujar pantalla actual
        screen.blit(screens[current_screen], (0, 0))
        screen.blit(continue_img, continue_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return True

def main():
    global game_paused
    
    # Bucle principal del juego que permite reinicios
    while True:
        # Actualizar configuración al inicio
        config.update_global_config()
        
        # Variables para control de música
        music_playing = False
        
        # Iniciar música del nivel
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
        
        # MOSTRAR TUTORIALES ANTES DE INICIAR EL NIVEL
        if not show_tutorial_screens(screen, 1):
            return "menu"  # Salir al menú si se cierra durante tutorial
        
        # Iniciar música al comenzar
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

        lumberjacks = []
        resources = []
        spawn_timer = 0
        resource_timer = 0
        start_ticks = pygame.time.get_ticks()
        
        # Variable para controlar si debemos reiniciar
        restart_requested = False

        while True:
            # VERIFICAR EVENTOS DE NAVEGACIÓN
            for event in pygame.event.get(pump=False):
                if event.type == config.OPEN_MENU_EVENT:
                    stop_level_music()
                    return  # Salir al menú principal

            # === EVENTOS ORIGINALES DEL NIVEL ===
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_level_music()
                    pygame.quit()
                    sys.exit()

                if event.type == config.OPEN_MENU_EVENT:
                    stop_level_music()
                    return  # Salir al menú principal

                if event.type == pygame.KEYDOWN:
                    # TECLA ESC → ABRE MENÚ DE PAUSA
                    if event.key == pygame.K_ESCAPE:
                        game_paused = True
                        result = pause_menu.show_pause_menu(screen, "level1")
                        game_paused = False
                        
                        # Manejar resultado del menú de pausa
                        if result == "restart":
                            restart_requested = True
                        elif result == "menu":
                            stop_level_music()
                            return
                        
                        # Reanudar música si se detuvo por configuración
                        if config.music and not pygame.mixer.music.get_busy():
                            start_level_music()

                    # Lógica original sin tocar:
                    if event.key == pygame.K_e:
                        all_trees = [central_tree] + game_world.trees
                        closest_tree = min(all_trees, key=lambda t: ((t.x - game_character.x) ** 2 + (t.y - game_character.y) ** 2))
                        distance = ((closest_tree.x - game_character.x) ** 2 + (closest_tree.y - game_character.y) ** 2) ** 0.5
                        if distance <= 70:
                            game_character.start_throw_animation()
                            game_character.deliver_resource(closest_tree)

                # CLICK EN BOTÓN DE PAUSA
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_rect.collidepoint(event.pos):
                        game_paused = True
                        result = pause_menu.show_pause_menu(screen, "level1")
                        game_paused = False
                        
                        # Manejar resultado del menú de pausa
                        if result == "restart":
                            restart_requested = True
                        elif result == "menu":
                            stop_level_music()
                            return
                        
                        # Reanudar música si se detuvo por configuración
                        if config.music and not pygame.mixer.music.get_busy():
                            start_level_music()

            # Verificar si se solicitó reinicio
            if restart_requested:
                break  # Romper el bucle interno y reiniciar

            # Si el juego está en pausa, saltar el resto de la lógica
            if game_paused:
                continue

            # === MOVIMIENTO ORIGINAL ===
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                game_character.move(dx=-5, dy=0, world=game_world)
            if keys[pygame.K_RIGHT]:
                game_character.move(dx=5, dy=0, world=game_world)
            if keys[pygame.K_UP]:
                game_character.move(dx=0, dy=-5, world=game_world)
            if keys[pygame.K_DOWN]:
                game_character.move(dx=0, dy=5, world=game_world)

            # === SPAWNS ORIGINALES ===
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

            # === DIBUJO ORIGINAL SIN CAMBIOS ===
            game_world.draw(screen)
            for resource in resources:
                resource.draw(screen)
            for enemy in lumberjacks:
                enemy.draw(screen)
            central_tree.draw(screen)
            for tree in game_world.trees:
                tree.draw(screen)
            game_character.draw(screen)

            # === HUD CON TEXTO TRADUCIDO ===
            seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
            remaining_time = max(0, constants.LEVEL_TIME - seconds_passed)
            
            # Obtener textos traducidos
            texts = get_localized_texts()
            
            font = pygame.font.SysFont(None, 26)
            text = font.render(texts["time"].format(remaining_time), True, constants.BLACK)
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

            # === DERROTA: ahora abre menú de pausa ===
            if central_tree.health <= 0:
                screen.blit(defeat_img, (0, 0))
                pygame.display.flip()
                pygame.time.delay(2000)
                game_paused = True
                result = pause_menu.show_pause_menu(screen, "level1")
                game_paused = False
                if result == "restart":
                    restart_requested = True
                elif result == "menu":
                    stop_level_music()
                    return
                # Si se cierra el menú de pausa sin reiniciar, continuamos el bucle interno
                # pero en este caso, el árbol central está destruido, por lo que probablemente queremos reiniciar o salir.
                # Vamos a forzar reinicio si no se elige menú.
                else:
                    restart_requested = True

            # === VICTORIA / DERROTA FINAL ===
            if remaining_time == 0:
                if vivos >= 3 and central_tree.health > 0:
                    screen.blit(victory_img, (0, 0))
                else:
                    screen.blit(defeat_img, (0, 0))
                pygame.display.flip()
                pygame.time.delay(3000)
                game_paused = True
                result = pause_menu.show_pause_menu(screen, "level1")
                game_paused = False
                if result == "restart":
                    restart_requested = True
                elif result == "menu":
                    stop_level_music()
                    return
                else:
                    # Por defecto, reiniciar si no se elige menú
                    restart_requested = True

            # === MOSTRAR BOTÓN DE PAUSA ===
            screen.blit(pause_icon, pause_rect)

            # HOVER amarillo del botón de pausa
            if pause_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 255, 0), pause_rect, 2)

            pygame.display.flip()
            clock.tick(60)

        # Si salimos del bucle interno por reinicio, continuamos el bucle externo
        if restart_requested:
            continue

if __name__ == "__main__":
    main()