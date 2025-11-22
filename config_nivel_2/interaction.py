# Funciones de interacción y colisiones
import pygame
import constants

def get_interaction_rect(central_tree):
    """Obtiene el rectángulo de interacción del árbol central"""
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
    """Verifica si el personaje puede interactuar con el árbol central"""
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
