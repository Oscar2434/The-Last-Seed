import pygame
import constants

def colision_cola(jugador):
    if not hasattr(jugador, "cola"):
        return False
    if len(jugador.cola) < 1:
        return False
    head = jugador.get_head_rect()
    for rect in jugador.cola[:-1]:
        if head.colliderect(rect):
            return True
    return False

def fuera_de_limites(jugador, width, height):
    head = jugador.get_head_rect()
    if head.left < 0:
        return True
    if head.right > width:
        return True
    if head.top < 0:
        return True
    if head.bottom > height:
        return True
    return False

def colision_obstaculos(jugador, obstaculos):
    head = jugador.get_head_rect()
    for obs in obstaculos:
        if head.colliderect(obs.rect):
            return True
    return False
