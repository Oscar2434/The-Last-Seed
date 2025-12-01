# desarrollador.py
import pygame

# CONFIGURACIÓN DE HITBOXES - MODIFICABLE
MOSTRAR_HITBOX = False  # Cambiar a False para ocultar las hitboxes

# CONFIGURACIÓN DE HITBOXES DE ENEMIGOS
HITBOX_COLISION_ENEMIGO = {
    'width': 20,        # Ancho de la hitbox de colisión
    'height': 50,       # Alto de la hitbox de colisión  
    'offset_x': 15,     # Desplazamiento X desde la posición del enemigo
    'offset_y': 5      # Desplazamiento Y desde la posición del enemigo
}

HITBOX_ATAQUE_ENEMIGO = {
    'width': 40,        # Ancho de la hitbox de ataque
    'height': 20,       # Alto de la hitbox de ataque
    'offset_x': 5,      # Desplazamiento X desde la posición del enemigo
    'offset_y': 15      # Desplazamiento Y desde la posición del enemigo
}

# CONFIGURACIÓN DE HITBOXES DE ÁRBOLES NORMALES
HITBOX_COLISION_ARBOL = {
    'width': 25,
    'height': 25,
    'offset_x': 20,
    'offset_y': 40
}

HITBOX_ATAQUE_ARBOL = {
    'width': 60,
    'height': 50,
    'offset_x': 1,
    'offset_y': 10
}

# CONFIGURACIÓN DE HITBOXES DEL ÁRBOL CENTRAL (MÁS GRANDE)
HITBOX_COLISION_ARBOL_CENTRAL = {
    'width': 30,   # Más grande porque el árbol central es más grande
    'height': 30,
    'offset_x': 35,
    'offset_y': 70
}

HITBOX_ATAQUE_ARBOL_CENTRAL = {
    'width': 100,  # Más grande porque el árbol central es más grande
    'height': 100,
    'offset_x': 0,
    'offset_y': 0
}

# CONFIGURACIÓN DE HITBOXES DE ROCAS
HITBOX_COLISION_ROCA = {
    'width': 30,
    'height': 30,
    'offset_x': 5,
    'offset_y': 5
}

# CONFIGURACIÓN DE HITBOXES DEL PERSONAJE
HITBOX_COLISION_PERSONAJE = {
    'width': 30,
    'height': 35,
    'offset_x': 15,
    'offset_y': 15
}

# CONFIGURACIÓN DE HITBOX DE INTERACCIÓN (ENTREGA DE RECURSOS)
HITBOX_ENTREGA_RECURSO = {
    'width': 100,       # Radio de interacción para entregar
    'height': 100,
    'offset_x': -20,    # Centrado en el personaje
    'offset_y': -20
}

# COLORES PARA DEBUG
COLOR_HITBOX_COLISION = (255, 0, 0)      # Rojo para colisión
COLOR_HITBOX_ATAQUE = (0, 255, 0)        # Verde para ataque
COLOR_HITBOX_CENTRAL = (0, 0, 255)       # Azul para central
COLOR_HITBOX_ROCA = (255, 165, 0)        # Naranja para rocas
COLOR_HITBOX_PERSONAJE = (255, 255, 0)   # Amarillo para personaje
COLOR_HITBOX_ENTREGA = (0, 255, 255)     # Cian para interacción

# CONFIGURACIÓN DE PROTECCIÓN POR RIEGO
TREE_PROTECTION_TIME = 5000  # Milisegundos (5 segundos)
COLOR_TREE_PROTECTED = (100, 200, 255)  # Azul claro para árbol protegido

# CONFIGURACIÓN DE POSICIÓN DE FUEGO
FIRE_OFFSET_X = -35  # Desplazamiento X del fuego respecto al árbol
FIRE_OFFSET_Y = -10  # Desplazamiento Y del fuego respecto al árbol