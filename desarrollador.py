# desarrollador.py
import pygame

MOSTRAR_HITBOX = False

HITBOX_COLISION_ENEMIGO = {
    'width': 20,
    'height': 50,
    'offset_x': 15,
    'offset_y': 5
}

HITBOX_ATAQUE_ENEMIGO = {
    'width': 40,
    'height': 20,
    'offset_x': 5,
    'offset_y': 15
}

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

HITBOX_COLISION_ARBOL_CENTRAL = {
    'width': 30,
    'height': 30,
    'offset_x': 35,
    'offset_y': 70
}

HITBOX_ATAQUE_ARBOL_CENTRAL = {
    'width': 100,
    'height': 100,
    'offset_x': 0,
    'offset_y': 0
}

HITBOX_COLISION_ROCA = {
    'width': 30,
    'height': 30,
    'offset_x': 5,
    'offset_y': 5
}

HITBOX_COLISION_PERSONAJE = {
    'width': 30,
    'height': 35,
    'offset_x': 15,
    'offset_y': 15
}

HITBOX_ENTREGA_RECURSO = {
    'width': 100,
    'height': 100,
    'offset_x': -20,
    'offset_y': -20
}

COLOR_HITBOX_COLISION = (255, 0, 0)
COLOR_HITBOX_ATAQUE = (0, 255, 0)
COLOR_HITBOX_CENTRAL = (0, 0, 255)
COLOR_HITBOX_ROCA = (255, 165, 0)
COLOR_HITBOX_PERSONAJE = (255, 255, 0)
COLOR_HITBOX_ENTREGA = (0, 255, 255)

TREE_PROTECTION_TIME = 5000
COLOR_TREE_PROTECTED = (100, 200, 255)

FIRE_OFFSET_X = -35
FIRE_OFFSET_Y = -10

ESCALA_FUEGO_ARBOL_CENTRAL = 1.5
OFFSET_X_FUEGO_ARBOL_CENTRAL = 0
OFFSET_Y_FUEGO_ARBOL_CENTRAL = 31