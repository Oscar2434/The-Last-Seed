import pygame
import sys
import os

# === CORRECCIÓN DE IMPORTS ===
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import constants
from character_nivel_2 import Character
from world_nivel_2 import World
from ambient_nivel_2 import CentralTree
from dialog_manager_nivel_2 import DialogManager
from pause_menu_nivel_2 import PauseMenu
# === FIN DE CORRECCIÓN ===

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("The last seed - Nivel 2")

victory_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'ganar.png')).convert_alpha()
defeat_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'perder.png')).convert_alpha()

victory_img = pygame.transform.scale(victory_img, (constants.WIDTH, constants.HEIGHT))
defeat_img = pygame.transform.scale(defeat_img, (constants.WIDTH, constants.HEIGHT))

def draw_dialog(screen, text):
    dialog_rect = pygame.Rect(40, constants.HEIGHT - 180, constants.WIDTH - 80, 160)
    
    pygame.draw.rect(screen, (255, 255, 255), dialog_rect)
    pygame.draw.rect(screen, (0, 100, 0), dialog_rect, 3)
    
    font = pygame.font.SysFont(None, 22)
    y_offset = dialog_rect.y + 15
    
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split(' ')
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < dialog_rect.width - 40:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
    
    for line in lines:
        if y_offset + 20 > dialog_rect.y + dialog_rect.height - 30:
            break
        text_surface = font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (dialog_rect.x + 20, y_offset))
        y_offset += 22
    
    continue_font = pygame.font.SysFont(None, 20)
    continue_text = continue_font.render("Presiona ESPACIO para continuar...", True, (100, 100, 100))
    screen.blit(continue_text, (dialog_rect.x + 20, dialog_rect.y + dialog_rect.height - 30))

def draw_inventory(screen, collected_resources):
    inventory_bg = pygame.Rect(constants.WIDTH - 150, 10, 140, 80)
    
    transparent_bg = pygame.Surface((inventory_bg.width, inventory_bg.height), pygame.SRCALPHA)
    pygame.draw.rect(transparent_bg, (0, 0, 0, 80), transparent_bg.get_rect())
    pygame.draw.rect(transparent_bg, (100, 100, 100, 100), transparent_bg.get_rect(), 1)
    
    screen.blit(transparent_bg, inventory_bg)
    
    font = pygame.font.SysFont(None, 20)
    
    title_shadow = font.render("Inventario:", True, (0, 0, 0, 100))
    screen.blit(title_shadow, (constants.WIDTH - 139, 16))
    
    title = font.render("Inventario:", True, (255, 255, 255))
    screen.blit(title, (constants.WIDTH - 140, 15))
    
    resource_display_names = {
        "composta": "Cáscara Plátano",
        "agua": "Agua",
        "semillas": "Cáscara Huevo"
    }
    
    y_offset = 35
    for resource_type in ["composta", "agua", "semillas"]:
        count = collected_resources.count(resource_type)
        display_name = resource_display_names.get(resource_type, resource_type)
        status = f"{display_name}: {count}" if count > 0 else f"{display_name}: 0"
        color = (200, 250, 200) if count > 0 else (180, 0, 0)
        text = font.render(status, True, color)
        screen.blit(text, (constants.WIDTH - 140, y_offset))
        y_offset += 20

def get_interaction_rect(central_tree):
    if hasattr(central_tree, 'image'):
        interaction_margin = 30
        
        return pygame.Rect(
            central_tree.x + central_tree.image.get_width() * constants.CENTRAL_TREE_HITBOX_X - interaction_margin,
            central_tree.y + central_tree.image.get_height() * constants.CENTRAL_TREE_HITBOX_Y - interaction_margin,
            central_tree.image.get_width() * constants.CENTRAL_TREE_HITBOX_WIDTH + (interaction_margin * 2),
            central_tree.image.get_height() * constants.CENTRAL_TREE_HITBOX_HEIGHT + (interaction_margin * 2)
        )
    return None

def check_interaction(character, central_tree):
    interaction_rect = get_interaction_rect(central_tree)
    if not interaction_rect:
        return False
    
    player_rect = pygame.Rect(
        character.x + character.gx,
        character.y + character.gy,
        constants.PERSONAJE * character.ry,
        constants.PERSONAJE * character.rx
    )
    
    return player_rect.colliderect(interaction_rect)

def show_defeat_screen(screen):
    screen.blit(defeat_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)

def show_victory_screen(screen):
    screen.blit(victory_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)

def run_level():
    clock = pygame.time.Clock()
    game_world = World(constants.WIDTH, constants.HEIGHT)
    game_character = Character(5, 386)
    
    central_tree = CentralTree(350, 50)
    game_world.set_central_tree(central_tree)

    # INICIALIZAR DIÁLOGOS
    dialog_manager = DialogManager()
    
    # INICIALIZAR MENÚ DE PAUSA
    pause_menu = PauseMenu(constants.WIDTH, constants.HEIGHT)

    start_ticks = pygame.time.get_ticks()
    
    collected_resources = []
    
    # SE ELIMINÓ LA LLAMADA A DIÁLOGOS INICIALES
    
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
        
        # OBTENER TIEMPO EFECTIVO DESDE EL MENÚ DE PAUSA
        effective_time = pause_menu.get_effective_time(current_time, start_ticks)
        
        # VERIFICAR ESTADOS DE PAUSA
        game_paused_by_dialog = dialog_manager.game_paused
        game_paused_by_menu = pause_menu.is_active()
        game_paused = game_paused_by_dialog or game_paused_by_menu
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            elif event.type == pygame.KEYDOWN:
                # Tecla P para activar/desactivar pausa
                if event.key == pygame.K_p:
                    pause_menu.toggle(current_time)
                
                # Solo procesar otras teclas si no hay pausa activa
                if not game_paused:
                    if event.key == pygame.K_e:
                        if check_interaction(game_character, central_tree):
                            if puede_entregar:
                                show_victory_screen(screen)
                                return "victory"
                            else:
                                dialog_manager.add_tree_dialog("need_resources")
                
                # Manejar ESPACIO para diálogos (solo si hay diálogos activos)
                elif event.key == pygame.K_SPACE and game_paused_by_dialog:
                    dialog_manager.next_dialog()
            
            # Manejar eventos del menú de pausa
            if pause_menu.is_active():
                menu_action = pause_menu.handle_event(event, current_time)
                if menu_action == "continue":
                    pause_menu.toggle(current_time)
                elif menu_action == "restart":  # NUEVO: Manejar reinicio
                    return "restart"
                elif menu_action == "menu":
                    return "menu"

        # Dibujar elementos del juego (siempre se dibujan, incluso en pausa)
        game_world.draw(screen)
        game_character.draw(screen)
        central_tree.draw(screen)

        for resource in game_world.resources:
            resource.draw(screen)
        
        for enemy in game_world.enemies:
            enemy.draw(screen)

        # Solo actualizar juego si no está en pausa
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
                    
                    break

        # ACTUALIZAR DIÁLOGOS (para cierre automático)
        dialog_manager.update(current_time)

        # CALCULAR Y MOSTRAR TIEMPO RESTANTE
        seconds_passed = effective_time // 1000
        remaining_time = max(0, constants.LEVEL_TIME - seconds_passed)
        
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Tiempo: {remaining_time}s", True, constants.BLACK)
        screen.blit(text, (10, 10))

        draw_inventory(screen, collected_resources)

        # DIBUJAR DIÁLOGOS (si es necesario y no está en pausa por menú)
        if dialog_manager.game_paused and dialog_manager.has_dialogs() and not pause_menu.is_active():
            dialog_text = dialog_manager.get_current_dialog_text()
            draw_dialog(screen, dialog_text)
            
            time_left = 10 - ((current_time - dialog_manager.dialog_timer) // 1000)
            if time_left < 11:
                time_font = pygame.font.SysFont(None, 20)
                time_text = time_font.render(f"Desaparece en: {time_left}s", True, (255, 220, 0))
                screen.blit(time_text, (constants.WIDTH - 150, constants.HEIGHT - 190))

        # DIBUJAR MENÚ DE PAUSA (encima de todo)
        if pause_menu.is_active():
            pause_menu.draw(screen)

        # VERIFICAR SI SE ACABÓ EL TIEMPO (solo si no está en pausa)
        if remaining_time == 0 and not game_paused:
            show_defeat_screen(screen)
            return "defeat"

        pygame.display.flip()
        clock.tick(60)

    return "quit"

def main():
    while True:
        result = run_level()
        
        if result == "victory":
            import nivels
            nivels.niveles()
            break
        elif result == "defeat":
            continue
        elif result == "restart":  # NUEVO: Reiniciar nivel
            continue  # Simplemente continuar el bucle para reiniciar
        elif result == "menu":  # Volver al menú principal
            import menu
            menu.menu()
            break
        elif result == "quit":
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()