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
    dialog_rect = pygame.Rect(50, constants.HEIGHT - 150, constants.WIDTH - 100, 120)
    
    # Fondo del diálogo
    pygame.draw.rect(screen, (255, 255, 255), dialog_rect)
    pygame.draw.rect(screen, (0, 100, 0), dialog_rect, 3)  # Borde verde
    
    # Texto del diálogo
    font = pygame.font.SysFont(None, 24)
    y_offset = dialog_rect.y + 20
    for line in text.split('\n'):
        text_surface = font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (dialog_rect.x + 20, y_offset))
        y_offset += 30
    
    # Instrucción para continuar
    continue_text = font.render("Presiona ESPACIO para continuar...", True, (100, 100, 100))
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
    
    y_offset = 35
    for resource_type in ["composta", "agua", "semillas"]:
        count = collected_resources.count(resource_type)
        status = f"{resource_type}: {count}" if count > 0 else f"{resource_type}: 0"
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
    
    # Hitbox del personaje (la misma que usas para colisiones)
    player_rect = pygame.Rect(
        character.x + character.gx,
        character.y + character.gy,
        constants.PERSONAJE * character.ry,
        constants.PERSONAJE * character.rx
    )
    
    return player_rect.colliderect(interaction_rect)

def main():
    clock = pygame.time.Clock()
    game_world = World(constants.WIDTH, constants.HEIGHT)
    game_character = Character(5, 386)
    
    # CREAR ÁRBOL CENTRAL
    central_tree = CentralTree(350, 50)
    game_world.set_central_tree(central_tree)

    start_ticks = pygame.time.get_ticks()
    
    collected_resources = []
    current_dialog = None
    game_paused = False
    puede_entregar = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not game_paused:
                    near_resource = game_character.check_near_resource(game_world.resources)
                    if near_resource and not near_resource.collected:
                        near_resource.collected = True
                        collected_resources.append(near_resource.type)
                        current_dialog = near_resource.get_dialog_text()
                        game_paused = True
                        
                        # Verificar si ya tiene los 3 recursos
                        if len(collected_resources) >= 3:
                            puede_entregar = True
                            current_dialog = "¡Has recolectado todos los recursos! \nAhora ve al árbol central y presiona 'E' para entregarlos."
                            game_paused = True
                
                elif event.key == pygame.K_e and not game_paused:
                    # ✅ CORREGIDO: Usar hitbox de interacción más grande
                    if check_interaction(game_character, central_tree):
                        if puede_entregar:
                            screen.blit(victory_img, (0, 0))
                            pygame.display.flip()
                            pygame.time.delay(3000)
                            return "victory"
                        else:
                            current_dialog = "El árbol central necesita todos los recursos para crecer fuerte. \nRecolecta composta, agua y semillas primero."
                            game_paused = True
                
                elif event.key == pygame.K_SPACE and game_paused:
                    game_paused = False
                    current_dialog = None

        # --- DIBUJADO ---
        # Dibujar mundo
        game_world.draw(screen)
        
        # DIBUJAR ÁRBOL CENTRAL
        central_tree.draw(screen)

        # Dibujar recursos
        for resource in game_world.resources:
            resource.draw(screen)
        
        # Dibujar personaje
        game_character.draw(screen)

        # DEBUG: Dibujar hitbox de colisión del árbol central (rojo)
        if hasattr(central_tree, 'image'):
            tree_rect = pygame.Rect(
                central_tree.x + central_tree.image.get_width() * constants.CENTRAL_TREE_HITBOX_X,
                central_tree.y + central_tree.image.get_height() * constants.CENTRAL_TREE_HITBOX_Y,
                central_tree.image.get_width() * constants.CENTRAL_TREE_HITBOX_WIDTH,
                central_tree.image.get_height() * constants.CENTRAL_TREE_HITBOX_HEIGHT
            )
            pygame.draw.rect(screen, (255, 0, 0), tree_rect, 2)
            
            # ✅ NUEVO: Dibujar hitbox de interacción (verde) - solo para debug
            interaction_rect = get_interaction_rect(central_tree)
            pygame.draw.rect(screen, (0, 255, 0), interaction_rect, 2)

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

        # Tiempo restante
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(0, constants.LEVEL_TIME - seconds_passed)
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Tiempo: {remaining_time}s", True, constants.BLACK)
        screen.blit(text, (10, 10))

        # Dibujar inventario
        draw_inventory(screen, collected_resources)

        # Mostrar diálogo si está activo
        if current_dialog and game_paused:
            draw_dialog(screen, current_dialog)

        # Condición de derrota por tiempo
        if remaining_time == 0:
            screen.blit(defeat_img, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            return "defeat"

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()