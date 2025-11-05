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

def main():
    clock = pygame.time.Clock()
    game_world = World(constants.WIDTH, constants.HEIGHT)
    game_character = Character(5, 386)
    
    # CREAR ÁRBOL CENTRAL
    central_tree = CentralTree(350, 50)
    
    # ✅ AGREGAR: Pasar el árbol central al mundo para las colisiones
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
                        
                        if len(collected_resources) >= 3:
                            puede_entregar = True
                            current_dialog = "¡Has recolectado todos los recursos! \nAhora ve al árbol central y presiona 'E' para entregarlos."
                            game_paused = True
                
                elif event.key == pygame.K_e and not game_paused:
                    # ✅ CORREGIDO: Usar central_tree directamente (no game_world.central_tree)
                    if game_character.check_collision(game_character.x, game_character.y, central_tree):
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

        # ... resto del código igual ...

        # Dibujar mundo
        game_world.draw(screen)
        
        # DIBUJAR ÁRBOL CENTRAL (usar la variable local central_tree)
        central_tree.draw(screen)

        if not game_paused:
            # Movimiento personaje (solo si no está pausado)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                game_character.move(dx=-5, dy=0, world=game_world)
            if keys[pygame.K_RIGHT]:
                game_character.move(dx=5, dy=0, world=game_world)
            if keys[pygame.K_UP]:
                game_character.move(dx=0, dy=-5, world=game_world)
            if keys[pygame.K_DOWN]:
                game_character.move(dx=0, dy=5, world=game_world)

        # Dibujar mundo
        game_world.draw(screen)
        

        # Dibujar recursos
        for resource in game_world.resources:
            resource.draw(screen)
        
        # Dibujar personaje
        game_character.draw(screen)

        # DIBUJAR ÁRBOL CENTRAL
        central_tree.draw(screen)

        if hasattr(central_tree, 'image'):
            tree_rect = pygame.Rect(
                central_tree.x + central_tree.image.get_width() * constants.CENTRAL_TREE_HITBOX_X,
                central_tree.y + central_tree.image.get_height() * constants.CENTRAL_TREE_HITBOX_Y,
                central_tree.image.get_width() * constants.CENTRAL_TREE_HITBOX_WIDTH,
                central_tree.image.get_height() * constants.CENTRAL_TREE_HITBOX_HEIGHT
            )
            pygame.draw.rect(screen, (255, 0, 0), tree_rect, 2)


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