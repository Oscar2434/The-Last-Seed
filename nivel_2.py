import pygame
import sys
import os

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

pygame.init()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("The last seed - Nivel 2")

pause_icon_raw = pygame.image.load("assets/images/effects/pausa.png").convert_alpha()
pause_icon = pygame.transform.scale(pause_icon_raw, (35, 35))
pause_rect = pause_icon.get_rect(center=(constants.WIDTH // 2, 20))

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

def draw_dialog(screen, text):
    dialog_rect = pygame.Rect(40, constants.HEIGHT - 180, constants.WIDTH - 80, 160)
    
    # Fondo color madera (café)
    wood_color = (101, 67, 33)  # Color madera oscura
    pygame.draw.rect(screen, wood_color, dialog_rect)
    
    # Borde más oscuro para simular madera
    border_color = (76, 47, 19)
    pygame.draw.rect(screen, border_color, dialog_rect, 4)
    
    # Texto color piel
    skin_color = (255, 218, 185)  # Color piel
    
    font = pygame.font.SysFont(None, 22)
    y_offset = dialog_rect.y + 20
    
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
        if y_offset + 20 > dialog_rect.y + dialog_rect.height - 40:
            break
        text_surface = font.render(line, True, skin_color)
        screen.blit(text_surface, (dialog_rect.x + 20, y_offset))
        y_offset += 24
    
    continue_font = pygame.font.SysFont(None, 20)
    
    if config.lenguaje:
        continue_text = "Presiona ESPACIO para continuar..."
    else:
        continue_text = "Press SPACE to continue..."
    
    # Texto de continuar en color piel claro
    continue_color = (255, 228, 196)
    continue_surface = continue_font.render(continue_text, True, continue_color)
    continue_rect = continue_surface.get_rect()
    continue_rect.x = dialog_rect.x + 20
    continue_rect.y = dialog_rect.y + dialog_rect.height - 35
    screen.blit(continue_surface, continue_rect)

def draw_inventory(screen, collected_resources):
    font = pygame.font.SysFont(None, 20)
    
    if config.lenguaje:
        title_text = "Inventario:"
        resource_display_names = {
            "composta": "Cáscara Plátano",
            "agua": "Agua",
            "semillas": "Cáscara Huevo"
        }
    else:
        title_text = "Inventory:"
        resource_display_names = {
            "composta": "Banana Peel",
            "agua": "Water",
            "semillas": "Egg Shell"
        }
    
    resource_texts = []
    for resource_type in ["composta", "agua", "semillas"]:
        count = collected_resources.count(resource_type)
        display_name = resource_display_names.get(resource_type, resource_type)
        status = f"{display_name}: {count}"
        resource_texts.append(status)
    
    title_size = font.size(title_text)
    max_width = max(title_size[0], max(font.size(text)[0] for text in resource_texts))
    
    padding = 15
    bg_width = max_width + padding * 2
    bg_height = padding * 2 + title_size[1] + len(resource_texts) * (font.get_height() + 2)
    
    bg_x = constants.WIDTH - bg_width - 20
    bg_y = 15
    
    bg_rect = pygame.Rect(bg_x, bg_y, bg_width, bg_height)
    
    # Crear superficie con canal alpha para transparencia real (fondo totalmente transparente)
    panel_surf = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
    panel_surf.fill((0, 0, 0, 0))  # transparente total inicialmente

    # Dibujar un rectángulo redondeado semitransparente (solo el negro) para que las esquinas queden transparentes
    pygame.draw.rect(panel_surf, (0, 0, 0, 110), panel_surf.get_rect(), border_radius=8)
    # Borde semitransparente
    pygame.draw.rect(panel_surf, (255, 255, 255, 100), panel_surf.get_rect(), 2, border_radius=8)
    # Dibujar la superficie transparente en la pantalla
    screen.blit(panel_surf, (bg_x, bg_y))
    
    title = font.render(title_text, True, (255, 255, 255))
    screen.blit(title, (bg_x + padding, bg_y + padding))
    
    y_offset = bg_y + padding + title_size[1] + 4
    for i, resource_type in enumerate(["composta", "agua", "semillas"]):
        count = collected_resources.count(resource_type)
        display_name = resource_display_names.get(resource_type, resource_type)
        status = f"{display_name}: {count}"
        color = (200, 250, 200) if count > 0 else (255, 150, 150)
        text = font.render(status, True, color)
        screen.blit(text, (bg_x + padding, y_offset))
        y_offset += font.get_height() + 2

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
    if config.lenguaje:
        defeat_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'perder.png')).convert_alpha()
    else:
        defeat_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'perderI.png')).convert_alpha()
    
    defeat_img = pygame.transform.scale(defeat_img, (constants.WIDTH, constants.HEIGHT))
    screen.blit(defeat_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)

def show_victory_screen(screen):
    if config.lenguaje:
        victory_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'ganar.png')).convert_alpha()
    else:
        victory_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'ganarI.png')).convert_alpha()
    
    victory_img = pygame.transform.scale(victory_img, (constants.WIDTH, constants.HEIGHT))
    screen.blit(victory_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)

def run_level():
    config.update_global_config()
    
    def start_level_music():
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.music.load('music/m1.mp3')
            pygame.mixer.music.set_volume(config.volume_master)
            pygame.mixer.music.play(-1)
    
    def stop_level_music():
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    
    if not show_tutorial_screens(screen, 2):
        return "menu"
    
    start_level_music()
    
    clock = pygame.time.Clock()
    game_world = World(constants.WIDTH, constants.HEIGHT)
    game_character = Character(5, 386)
    
    central_tree = CentralTree(350, 50)
    game_world.set_central_tree(central_tree)

    dialog_manager = DialogManager()

    start_ticks = pygame.time.get_ticks()
    pause_start_time = 0
    total_pause_time = 0
    game_paused = False
    dialog_pause_start_time = 0
    total_dialog_time = 0
    last_dialog_state = False
    
    collected_resources = []
    
    puede_entregar = False
    
    try:
        difficulty = getattr(config, 'difficulty', 'normal')
    except:
        difficulty = 'normal'
    
    level_settings = constants.LEVEL_2_SETTINGS.get(difficulty, constants.LEVEL_2_SETTINGS["normal"])
    level_time = level_settings["LEVEL_TIME"]
    
    game_world.create_enemies(difficulty)
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        current_dialog_paused = dialog_manager.game_paused
        
        if current_dialog_paused and not last_dialog_state:
            dialog_pause_start_time = current_time
        elif not current_dialog_paused and last_dialog_state:
            total_dialog_time += (current_time - dialog_pause_start_time)
        
        last_dialog_state = current_dialog_paused
        
        if game_paused:
            effective_time = (pause_start_time - start_ticks) - total_pause_time
        else:
            effective_time = (current_time - start_ticks) - total_pause_time - total_dialog_time
        
        game_paused_by_dialog = dialog_manager.game_paused
        game_paused_total = game_paused_by_dialog or game_paused

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not game_paused_by_dialog:
                    if not game_paused:
                        game_paused = True
                        pause_start_time = current_time
                        result = pause_menu.show_pause_menu(screen, "level2")
                        game_paused = False
                        total_pause_time += (current_time - pause_start_time)
                        
                        if result == "restart":
                            return "restart"
                        elif result == "menu":
                            stop_level_music()
                            return "menu"
                        if config.music and not pygame.mixer.music.get_busy():
                            start_level_music()
                
                if not game_paused_total:
                    if event.key == pygame.K_e:
                        if check_interaction(game_character, central_tree):
                            if puede_entregar:
                                show_victory_screen(screen)
                                game_paused = True
                                result = pause_menu.show_pause_menu(screen, "level2")
                                game_paused = False
                                
                                if result == "restart":
                                    return "restart"
                                elif result == "menu":
                                    stop_level_music()
                                    return "menu"
                                else:
                                    return "restart"
                            else:
                                dialog_manager.add_tree_dialog("need_resources")
                
                elif event.key == pygame.K_SPACE and game_paused_by_dialog:
                    dialog_manager.next_dialog()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_paused_by_dialog:
                if pause_rect.collidepoint(event.pos):
                    if not game_paused:
                        game_paused = True
                        pause_start_time = current_time
                        result = pause_menu.show_pause_menu(screen, "level2")
                        game_paused = False
                        total_pause_time += (current_time - pause_start_time)
                        
                        if result == "restart":
                            return "restart"
                        elif result == "menu":
                            stop_level_music()
                            return "menu"
                        if config.music and not pygame.mixer.music.get_busy():
                            start_level_music()

        game_world.draw(screen)
        game_character.draw(screen)
        central_tree.draw(screen)

        for resource in game_world.resources:
            resource.draw(screen)
        
        for enemy in game_world.enemies:
            enemy.draw(screen)

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
                    game_paused = True
                    result = pause_menu.show_pause_menu(screen, "level2")
                    game_paused = False
                    
                    if result == "restart":
                        return "restart"
                    elif result == "menu":
                        stop_level_music()
                        return "menu"
                    else:
                        return "restart"

            for resource in game_world.resources:
                if not resource.collected and game_character.check_collision(game_character.x, game_character.y, resource):
                    resource.collected = True
                    temp_resource_type = resource.type
                    
                    dialog_manager.add_resource_dialog(temp_resource_type)
                    
                    collected_resources.append(temp_resource_type)
                    
                    if len(collected_resources) >= 3:
                        dialog_manager.add_tree_dialog("all_collected")
                        puede_entregar = True
                    
                    break

        dialog_manager.update(current_time)

        seconds_passed = effective_time // 1000
        remaining_time = max(0, level_time - seconds_passed)
        
        draw_timer(screen, remaining_time, level_time, 10, 10)

        draw_inventory(screen, collected_resources)
        
        screen.blit(pause_icon, pause_rect)

        if pause_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255, 255, 0), pause_rect, 2)

        if dialog_manager.game_paused and dialog_manager.has_dialogs() and not game_paused:
            dialog_text = dialog_manager.get_current_dialog_text()
            draw_dialog(screen, dialog_text)
            
            time_left = 10 - ((current_time - dialog_manager.dialog_timer) // 1000)
            if time_left < 11:
                time_font = pygame.font.SysFont(None, 20)
                
                if config.lenguaje:
                    time_display = f"Desaparece en: {time_left}s"
                else:
                    time_display = f"Disappears in: {time_left}s"
                    
                time_text = time_font.render(time_display, True, (255, 220, 0))
                # Posicionar el texto dentro del cuadro de diálogo (alineado a la derecha, encima de la línea de "continuar")
                dialog_x = 40
                dialog_y = constants.HEIGHT - 180
                dialog_width = constants.WIDTH - 80
                dialog_height = 160
                time_x = dialog_x + dialog_width - time_text.get_width() - 20
                time_y = dialog_y + dialog_height - 35
                screen.blit(time_text, (time_x, time_y))

        if remaining_time == 0 and not game_paused_total:
            show_defeat_screen(screen)
            game_paused = True
            result = pause_menu.show_pause_menu(screen, "level2")
            game_paused = False
            
            if result == "restart":
                return "restart"
            elif result == "menu":
                stop_level_music()
                return "menu"
            else:
                return "restart"

        pygame.display.flip()
        clock.tick(60)

    return "quit"

def main():
    while True:
        result = run_level()
        
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
        
        if result == "restart":
            continue
        elif result == "menu":
            menu_event = pygame.event.Event(config.OPEN_MENU_EVENT)
            pygame.event.post(menu_event)
            return "menu"
        elif result == "quit":
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()