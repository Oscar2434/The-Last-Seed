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
from config_nivel_2.dialog_texts import DialogManager
import pause_menu
import config
# === FIN DE CORRECCIÓN ===

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("The last seed - Nivel 2")

victory_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'ganar.png')).convert_alpha()
defeat_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'perder.png')).convert_alpha()

victory_img = pygame.transform.scale(victory_img, (constants.WIDTH, constants.HEIGHT))
defeat_img = pygame.transform.scale(defeat_img, (constants.WIDTH, constants.HEIGHT))

# === BOTÓN DE PAUSA PARA NIVEL 2 ===
pause_icon_raw = pygame.image.load("assets/images/effects/pausa.png").convert_alpha()
pause_icon = pygame.transform.scale(pause_icon_raw, (35, 35))
pause_rect = pause_icon.get_rect(center=(constants.WIDTH // 2, 20))

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
    
    # Texto "continuar" según idioma
    if config.lenguaje:
        continue_text = "Presiona ESPACIO para continuar..."
    else:
        continue_text = "Press SPACE to continue..."
        
    continue_surface = continue_font.render(continue_text, True, (100, 100, 100))
    screen.blit(continue_surface, (dialog_rect.x + 20, dialog_rect.y + dialog_rect.height - 30))

def draw_inventory(screen, collected_resources):
    inventory_bg = pygame.Rect(constants.WIDTH - 150, 10, 140, 80)
    
    transparent_bg = pygame.Surface((inventory_bg.width, inventory_bg.height), pygame.SRCALPHA)
    pygame.draw.rect(transparent_bg, (0, 0, 0, 80), transparent_bg.get_rect())
    pygame.draw.rect(transparent_bg, (100, 100, 100, 100), transparent_bg.get_rect(), 1)
    
    screen.blit(transparent_bg, inventory_bg)
    
    font = pygame.font.SysFont(None, 20)
    
    # Título del inventario según idioma
    if config.lenguaje:
        title_text = "Inventario:"
    else:
        title_text = "Inventory:"
    
    title_shadow = font.render(title_text, True, (0, 0, 0, 100))
    screen.blit(title_shadow, (constants.WIDTH - 139, 16))
    
    title = font.render(title_text, True, (255, 255, 255))
    screen.blit(title, (constants.WIDTH - 140, 15))
    
    # Nombres según el idioma
    if config.lenguaje:  # Español
        resource_display_names = {
            "composta": "Cáscara Plátano",
            "agua": "Agua",
            "semillas": "Cáscara Huevo"
        }
    else:  # Inglés
        resource_display_names = {
            "composta": "Banana Peel",
            "agua": "Water",
            "semillas": "Egg Shell"
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
    # Actualizar configuración al inicio
    config.update_global_config()
    
    # Control de música
    def start_level_music():
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.music.load('music/m1.mp3')
            pygame.mixer.music.set_volume(config.volume_master)
            pygame.mixer.music.play(-1)
    
    def stop_level_music():
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    
    # MOSTRAR TUTORIALES ANTES DE INICIAR EL NIVEL
    if not show_tutorial_screens(screen, 2):
        return "menu"  # Salir al menú si se cierra durante tutorial
    
    # Iniciar música al comenzar
    start_level_music()
    
    clock = pygame.time.Clock()
    game_world = World(constants.WIDTH, constants.HEIGHT)
    game_character = Character(5, 386)
    
    central_tree = CentralTree(350, 50)
    game_world.set_central_tree(central_tree)

    # INICIALIZAR DIÁLOGOS
    dialog_manager = DialogManager()

    start_ticks = pygame.time.get_ticks()
    pause_start_time = 0
    total_pause_time = 0
    game_paused = False
    
    collected_resources = []
    
    puede_entregar = False
    
    try:
        difficulty = getattr(config, 'difficulty', 'normal')
    except:
        difficulty = 'normal'
    
    game_world.create_enemies(difficulty)
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        # Calcular tiempo efectivo considerando pausas
        if game_paused:
            effective_time = (pause_start_time - start_ticks) - total_pause_time
        else:
            effective_time = (current_time - start_ticks) - total_pause_time
        
        # VERIFICAR ESTADOS DE PAUSA
        game_paused_by_dialog = dialog_manager.game_paused
        game_paused_total = game_paused_by_dialog or game_paused

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            elif event.type == pygame.KEYDOWN:
                # Tecla ESC para activar/desactivar pausa
                if event.key == pygame.K_ESCAPE and not game_paused_by_dialog:
                    if not game_paused:
                        # Iniciar pausa
                        game_paused = True
                        pause_start_time = current_time
                        # Mostrar menú de pausa y capturar resultado
                        result = pause_menu.show_pause_menu(screen, "level2")
                        # Finalizar pausa
                        game_paused = False
                        total_pause_time += (current_time - pause_start_time)
                        
                        # Manejar resultado del menú de pausa
                        if result == "restart":
                            return "restart"
                        elif result == "menu":
                            stop_level_music()
                            return "menu"
                        # Reanudar música si se detuvo por configuración
                        if config.music and not pygame.mixer.music.get_busy():
                            start_level_music()
                
                # Solo procesar otras teclas si no hay pausa activa
                if not game_paused_total:
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

            # CLICK EN BOTÓN DE PAUSA
            if event.type == pygame.MOUSEBUTTONDOWN and not game_paused_by_dialog:
                if pause_rect.collidepoint(event.pos):
                    if not game_paused:
                        # Iniciar pausa
                        game_paused = True
                        pause_start_time = current_time
                        # Mostrar menú de pausa y capturar resultado
                        result = pause_menu.show_pause_menu(screen, "level2")
                        # Finalizar pausa
                        game_paused = False
                        total_pause_time += (current_time - pause_start_time)
                        
                        # Manejar resultado del menú de pausa
                        if result == "restart":
                            return "restart"
                        elif result == "menu":
                            stop_level_music()
                            return "menu"
                        # Reanudar música si se detuvo por configuración
                        if config.music and not pygame.mixer.music.get_busy():
                            start_level_music()

        # Dibujar elementos del juego (siempre se dibujan, incluso en pausa)
        game_world.draw(screen)
        game_character.draw(screen)
        central_tree.draw(screen)

        for resource in game_world.resources:
            resource.draw(screen)
        
        for enemy in game_world.enemies:
            enemy.draw(screen)

        # Solo actualizar juego si no está en pausa
        if not game_paused_total:
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
        
        # Texto del tiempo según idioma
        if config.lenguaje:
            time_text = f"Tiempo: {remaining_time}s"
        else:
            time_text = f"Time: {remaining_time}s"
            
        text = font.render(time_text, True, constants.BLACK)
        screen.blit(text, (10, 10))

        draw_inventory(screen, collected_resources)
        
        # === MOSTRAR BOTÓN DE PAUSA ===
        screen.blit(pause_icon, pause_rect)

        # HOVER amarillo del botón de pausa
        if pause_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255, 255, 0), pause_rect, 2)

        # DIBUJAR DIÁLOGOS (si es necesario y no está en pausa por menú)
        if dialog_manager.game_paused and dialog_manager.has_dialogs() and not game_paused:
            dialog_text = dialog_manager.get_current_dialog_text()
            draw_dialog(screen, dialog_text)
            
            time_left = 10 - ((current_time - dialog_manager.dialog_timer) // 1000)
            if time_left < 11:
                time_font = pygame.font.SysFont(None, 20)
                
                # Texto del temporizador según idioma
                if config.lenguaje:
                    time_display = f"Desaparece en: {time_left}s"
                else:
                    time_display = f"Disappears in: {time_left}s"
                    
                time_text = time_font.render(time_display, True, (255, 220, 0))
                screen.blit(time_text, (constants.WIDTH - 150, constants.HEIGHT - 190))

        # VERIFICAR SI SE ACABÓ EL TIEMPO (solo si no está en pausa)
        if remaining_time == 0 and not game_paused_total:
            show_defeat_screen(screen)
            return "defeat"

        pygame.display.flip()
        clock.tick(60)

    return "quit"

def main():
    while True:
        result = run_level()
        
        # DETENER MÚSICA DEL NIVEL AL SALIR
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
        
        if result == "victory":
            # Enviar evento para reiniciar música del menú
            menu_event = pygame.event.Event(config.OPEN_MENU_EVENT)
            pygame.event.post(menu_event)
            return "menu"
        elif result == "defeat":
            continue
        elif result == "restart":
            continue
        elif result == "menu":
            # Enviar evento para reiniciar música del menú
            menu_event = pygame.event.Event(config.OPEN_MENU_EVENT)
            pygame.event.post(menu_event)
            return "menu"
        elif result == "quit":
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()