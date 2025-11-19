import pygame
import sys
import os

# === CORRECCIÓN DE IMPORTS ===
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import constants
from nivel_2.character import Character
from nivel_2.world import World
from nivel_2.ambient import CentralTree
from nivel_2.dialog_manager import DialogManager
from nivel_2.config.ui_config import draw_dialog, draw_inventory, draw_timer, draw_dialog_timer
from nivel_2.config.interaction import check_interaction
from nivel_2.config.screen_manager import show_defeat_screen, show_victory_screen, scale_screen_images
# === FIN DE CORRECCIÓN ===

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("The last seed - Nivel 2")

# Escalar imágenes de pantalla
scale_screen_images(constants.WIDTH, constants.HEIGHT)

def run_level():
    # CARGAR MÚSICA DEL NIVEL AL INICIAR
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.music.load('music/m1.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    
    clock = pygame.time.Clock()
    game_world = World(constants.WIDTH, constants.HEIGHT)
    game_character = Character(5, 386)
    
    central_tree = CentralTree(350, 50)
    game_world.set_central_tree(central_tree)

    # INICIALIZAR DIÁLOGOS
    dialog_manager = DialogManager()

    start_ticks = pygame.time.get_ticks()
    paused_time = 0
    last_pause_start = 0
    
    collected_resources = []
    
    # INICIAR DIÁLOGOS INICIALES
    dialog_manager.start_initial_dialog()

    puede_entregar = False
    
    try:
        import config
        difficulty = getattr(config, 'difficulty', 'normal')
    except:
        difficulty = 'normal'
    
    game_world.create_enemies(difficulty)
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        # ACTUALIZAR ESTADO DE PAUSA BASADO EN DIÁLOGOS
        game_paused = dialog_manager.game_paused
        
        if game_paused:
            if last_pause_start == 0:
                last_pause_start = current_time
        else:
            if last_pause_start > 0:
                paused_time += current_time - last_pause_start
                last_pause_start = 0
        
        effective_time = current_time - start_ticks - paused_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not game_paused:
                    if check_interaction(game_character, central_tree):
                        if puede_entregar:
                            show_victory_screen(screen)
                            return "victory"
                        else:
                            dialog_manager.add_tree_dialog("need_resources")
                            if not game_paused:
                                dialog_manager.game_paused = True
                                dialog_manager.dialog_timer = current_time
                
                elif event.key == pygame.K_SPACE and game_paused:
                    dialog_manager.next_dialog()

        game_world.draw(screen)
        game_character.draw(screen)
        central_tree.draw(screen)

        for resource in game_world.resources:
            resource.draw(screen)
        
        for enemy in game_world.enemies:
            enemy.draw(screen)

        if not game_paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                game_character.move(dx=-5, dy=0, world=game_world)
            if keys[pygame.K_RIGHT]:
                game_character.move(dx=5, dy=0, world=game_world)
            if keys[pygame.K_UP]:
                game_character.move(dx=0, dy=-5, world=game_world)
            if keys[pygame.K_DOWN]:
                game_character.move(dx=0, dy=5, world=game_world)

            for enemy in game_world.enemies:
                enemy.move_towards_player(game_character.x, game_character.y, game_world)
                
                if enemy.check_capture(game_character):
                    show_defeat_screen(screen)
                    return "defeat"

            for resource in game_world.resources:
                if not resource.collected and game_character.check_collision(game_character.x, game_character.y, resource):
                    resource.collected = True
                    temp_resource_type = resource.type
                    
                    # AÑADIR DIÁLOGO DEL RECURSO
                    dialog_manager.add_resource_dialog(temp_resource_type)
                    
                    collected_resources.append(temp_resource_type)
                    
                    # VERIFICAR SI SE RECOLECTARON TODOS
                    if len(collected_resources) >= 3:
                        dialog_manager.add_tree_dialog("all_collected")
                        puede_entregar = True
                    
                    if not game_paused:
                        dialog_manager.game_paused = True
                        dialog_manager.dialog_timer = current_time
                    
                    break

        # ACTUALIZAR DIÁLOGOS (para cierre automático)
        dialog_manager.update(current_time)

        seconds_passed = effective_time // 1000
        remaining_time = max(0, constants.LEVEL_TIME - seconds_passed)
        draw_timer(screen, remaining_time, constants)

        draw_inventory(screen, collected_resources, constants)

        # DIBUJAR DIÁLOGOS (si es necesario)
        if dialog_manager.game_paused and dialog_manager.has_dialogs():
            dialog_text = dialog_manager.get_current_dialog_text()
            draw_dialog(screen, dialog_text, constants)
            draw_dialog_timer(screen, current_time, dialog_manager.dialog_timer, constants)

        if remaining_time == 0:
            show_defeat_screen(screen)
            return "defeat"

        pygame.display.flip()
        clock.tick(60)

    return "quit"

def main():
    while True:
        result = run_level()
        
        if result == "victory":
            pygame.mixer.music.stop()
            import nivels
            nivels.niveles()
            break
        elif result == "defeat":
            continue
        elif result == "quit":
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()