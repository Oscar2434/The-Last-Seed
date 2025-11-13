import pygame
import sys
import constants
from character_nivel_2 import Character
from world_nivel2 import World
from ambient_nivel2 import CentralTree
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

def draw_dialog(screen, text):
    """Dibujar cuadro de diálogo en pantalla"""
    
    dialog_rect = pygame.Rect(40, constants.HEIGHT - 180, constants.WIDTH - 80, 160)
    
    # Fondo del diálogo
    pygame.draw.rect(screen, (255, 255, 255), dialog_rect)
    pygame.draw.rect(screen, (0, 100, 0), dialog_rect, 3)  
    
    # Texto del diálogo
    font = pygame.font.SysFont(None, 22)  
    y_offset = dialog_rect.y + 15
    
   
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split(' ')
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            # Verificar si la línea excede el ancho del diálogo
            if font.size(test_line)[0] < dialog_rect.width - 40:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
    
    # Dibujar cada línea
    for line in lines:
        if y_offset + 20 > dialog_rect.y + dialog_rect.height - 30:
            break  # No dibujar más líneas si no caben
        text_surface = font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (dialog_rect.x + 20, y_offset))
        y_offset += 22  # ✅ MODIFICADO: Espaciado entre líneas
    
    # Instrucción para continuar
    continue_font = pygame.font.SysFont(None, 20)
    continue_text = continue_font.render("Presiona ESPACIO para continuar...", True, (100, 100, 100))
    screen.blit(continue_text, (dialog_rect.x + 20, dialog_rect.y + dialog_rect.height - 30))

def draw_inventory(screen, collected_resources):
    """Inventario minimalista y muy transparente"""
    inventory_bg = pygame.Rect(constants.WIDTH - 150, 10, 140, 80)
    
    transparent_bg = pygame.Surface((inventory_bg.width, inventory_bg.height), pygame.SRCALPHA)
    # Muy poca opacidad
    pygame.draw.rect(transparent_bg, (0, 0, 0, 80), transparent_bg.get_rect())
    pygame.draw.rect(transparent_bg, (100, 100, 100, 100), transparent_bg.get_rect(), 1)
    
    screen.blit(transparent_bg, inventory_bg)
    
    # Texto con sombra para mejor legibilidad
    font = pygame.font.SysFont(None, 20)
    
    # Sombra del título
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
        color = (200, 250, 200) if count > 0 else (180, 0, 0)  # Colores claros
        text = font.render(status, True, color)
        screen.blit(text, (constants.WIDTH - 140, y_offset))
        y_offset += 20


def get_interaction_rect(central_tree):
    """Obtener hitbox de interacción más grande que la de colisión"""
    if hasattr(central_tree, 'image'):
        # Hacer la hitbox de interacción más grande que la de colisión
        interaction_margin = 30  # píxeles adicionales en cada dirección
        
        return pygame.Rect(
            central_tree.x + central_tree.image.get_width() * constants.CENTRAL_TREE_HITBOX_X - interaction_margin,
            central_tree.y + central_tree.image.get_height() * constants.CENTRAL_TREE_HITBOX_Y - interaction_margin,
            central_tree.image.get_width() * constants.CENTRAL_TREE_HITBOX_WIDTH + (interaction_margin * 2),
            central_tree.image.get_height() * constants.CENTRAL_TREE_HITBOX_HEIGHT + (interaction_margin * 2)
        )
    return None

def check_interaction(character, central_tree):
    """Verificar si el personaje está lo suficientemente cerca para interactuar"""
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
    """Mostrar pantalla de derrota y esperar"""
    screen.blit(defeat_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)  

def show_victory_screen(screen):
    """Mostrar pantalla de victoria y esperar"""
    screen.blit(victory_img, (0, 0))
    pygame.display.flip()
    pygame.time.delay(3000)  

def run_level():
    """Ejecutar un nivel completo y retornar el resultado"""
    clock = pygame.time.Clock()
    game_world = World(constants.WIDTH, constants.HEIGHT)
    game_character = Character(5, 386)
    
    # CREAR ÁRBOL CENTRAL
    central_tree = CentralTree(350, 50)
    game_world.set_central_tree(central_tree)

    start_ticks = pygame.time.get_ticks()
    paused_time = 0 
    last_pause_start = 0  
    
    collected_resources = []
    dialog_queue = []
    
    
    initial_dialog = [
        "EL LABERINTO DE LA NATURALEZA",
        " ",
        "OBJETIVO: Recolecta 3 recursos para",
        "ayudar al árbol central:",
        "• Cáscara de plátano (composta)",
        "• Agua",
        "• Cáscara de huevo",
        " ",
        "¡Cuidado! Los fantasmas te persiguen",
        "por el laberinto. No dejes que te atrapen.",
        
        "CONTROLES:",
        "• Flechas: Mover personaje",
        "• E: Interactuar con árbol central", 
        "• ESPACIO: Continuar diálogos",
        " ",
        "Tienes un límite de tiempo.",
        "¡Buena suerte!"
    ]
    
    # Añadir todos los diálogos iniciales a la cola
    dialog_queue.extend(initial_dialog)
    game_paused = True  
    dialog_timer = pygame.time.get_ticks()  
    
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
        
       
        if game_paused:
            if last_pause_start == 0:
                last_pause_start = current_time
        else:
            if last_pause_start > 0:
                # Al despausar, sumar el tiempo que estuvo pausado
                paused_time += current_time - last_pause_start
                last_pause_start = 0
        
        # Tiempo real de juego (excluyendo pausas)
        effective_time = current_time - start_ticks - paused_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not game_paused:
                    if check_interaction(game_character, central_tree):
                        if puede_entregar:
                            show_victory_screen(screen)
                            return "victory"
                        else:
                            dialog_queue.append("El árbol central necesita todos los")
                            dialog_queue.append("recursos para crecer fuerte.")
                            dialog_queue.append("Recolecta composta, agua y semillas primero.")
                            if not game_paused:
                                game_paused = True
                                dialog_timer = current_time
                
                elif event.key == pygame.K_SPACE and game_paused:
                    if dialog_queue:
                        dialog_queue.pop(0)
                        if dialog_queue:
                            dialog_timer = current_time
                        else:
                            game_paused = False
                    else:
                        game_paused = False

        # --- DIBUJADO ---
        game_world.draw(screen)
        # Dibujar personaje
        game_character.draw(screen)
        central_tree.draw(screen)

        # Dibujar recursos
        for resource in game_world.resources:
            resource.draw(screen)
        
       
        for enemy in game_world.enemies:
            enemy.draw(screen)

        # Movimiento del personaje (solo si no está pausado)
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
                
                # ✅ NUEVO: Verificar si el enemigo capturó al jugador
                if enemy.check_capture(game_character):
                    show_defeat_screen(screen)
                    return "defeat"

            # Recolección de recursos (código existente)
            for resource in game_world.resources:
                if not resource.collected and game_character.check_collision(game_character.x, game_character.y, resource):
                    resource.collected = True
                    temp_resource_type = resource.type
                    dialog_queue.append(resource.get_dialog_text())
                    
                    if len(collected_resources) == 2:
                        dialog_queue.append("¡Has recolectado todos los recursos!")
                        dialog_queue.append("Ahora ve al árbol central y")
                        dialog_queue.append("presiona 'E' para entregarlos.")
                        puede_entregar = True
                    
                    collected_resources.append(temp_resource_type)
                    
                    if not game_paused:
                        game_paused = True
                        dialog_timer = current_time
                    
                    break

       
        if game_paused and dialog_queue and (current_time - dialog_timer > 10000):  
            dialog_queue.pop(0)  
            
            if dialog_queue:
                dialog_timer = current_time  
            else:
                game_paused = False

       
        seconds_passed = effective_time // 1000
        remaining_time = max(0, constants.LEVEL_TIME - seconds_passed)
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Tiempo: {remaining_time}s", True, constants.BLACK)
        screen.blit(text, (10, 10))

       
        draw_inventory(screen, collected_resources)

        
        if dialog_queue and game_paused:
           
            dialog_text = "\n".join(dialog_queue[:8]) 
            draw_dialog(screen, dialog_text)
            
            
            time_left = 12 - ((current_time - dialog_timer) // 1000)
            if time_left < 13:  
                time_font = pygame.font.SysFont(None, 20)
                time_text = time_font.render(f"Desaparece en: {time_left}s", True, (255, 220, 0))
                screen.blit(time_text, (constants.WIDTH - 150, constants.HEIGHT - 190))

   
        if remaining_time == 0:
            show_defeat_screen(screen)
            return "defeat"

        pygame.display.flip()
        clock.tick(60)

    return "quit"

def main():
    """Función principal que maneja la repetición del nivel"""
    while True:
        result = run_level()
        
        if result == "victory":
            # Si gana, salir del bucle y terminar el nivel
            break
        elif result == "defeat":
            # Si pierde, el bucle continúa y repite el nivel automáticamente
            continue
        elif result == "quit":
            # Si el jugador cierra la ventana, salir
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()