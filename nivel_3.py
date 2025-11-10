import pygame
import sys
import random
import os
import constants

pygame.init()

# ------------------------------------
# CONFIGURACIÓN
# ------------------------------------
WIDTH, HEIGHT = constants.WIDTH, constants.HEIGHT
TAM_CELDA = 32
FPS = 10
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nivel 3 - recolecta de basura")

# COLORES
BLANCO = (255, 255, 255)

# FUENTE
FUENTE = pygame.font.SysFont("arial", 24, True)

# ------------------------------------
# CARGA DE IMÁGENES
# ------------------------------------
ASSETS_PATH = os.path.join("assets")

# Fondo
background_img = pygame.image.load(os.path.join('assets', 'images', 'objects', 'grass3.png')).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Basura
trash_img = pygame.image.load(os.path.join('assets', 'images', 'character', 'escombro.png')).convert_alpha()
trash_img = pygame.transform.scale(trash_img, (TAM_CELDA, TAM_CELDA))

# Cuerpo / cola
bag_img = pygame.image.load(os.path.join('assets', 'images', 'character', 'basura.png')).convert_alpha()
bag_img = pygame.transform.scale(bag_img, (TAM_CELDA, TAM_CELDA))

# Imágenes de victoria/derrota
victory_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'victoria.png')).convert_alpha()
victory_img = pygame.transform.scale(victory_img, (WIDTH, HEIGHT))

defeat_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'derrota.png')).convert_alpha()
defeat_img = pygame.transform.scale(defeat_img, (WIDTH, HEIGHT))

# ------------------------------------
# CARGAR Y CORTAR SPRITES DEL NIÑO
# ------------------------------------
def cargar_spritesheet(ruta, columnas, filas):
    imagen = pygame.image.load(ruta).convert_alpha()
    ancho_celda = imagen.get_width() // columnas
    alto_celda = imagen.get_height() // filas
    sprites = []

    for fila in range(filas):
        fila_sprites = []
        for col in range(columnas):
            rect = pygame.Rect(col * ancho_celda, fila * alto_celda, ancho_celda, alto_celda)
            frame = imagen.subsurface(rect)
            frame = pygame.transform.scale(frame, (TAM_CELDA, TAM_CELDA))
            fila_sprites.append(frame)
        sprites.append(fila_sprites)
    return sprites

# El sprite tiene 4 filas (direcciones) y 4 columnas (frames por movimiento)
nino_sprites = cargar_spritesheet(os.path.join('assets', 'images', 'character', 'nino.png'), 4, 4)

# Mapeo de direcciones (por fila del sprite)
DIRECCIONES = {
    "ABAJO": 0,
    "IZQUIERDA": 1,
    "DERECHA": 2,
    "ARRIBA": 3
}

# ------------------------------------
# FUNCIONES
# ------------------------------------
def mostrar_texto(texto, color, x, y):
    surface = FUENTE.render(texto, True, color)
    screen.blit(surface, (x, y))

def generar_basura():
    x = random.randrange(0, WIDTH - TAM_CELDA, TAM_CELDA)
    y = random.randrange(0, HEIGHT - TAM_CELDA, TAM_CELDA)
    return [x, y]

def dibujar_cuerpo(cuerpo, direccion, frame_index):
    for i, parte in enumerate(cuerpo):
        if i == len(cuerpo) - 1:
            fila = DIRECCIONES[direccion]
            screen.blit(nino_sprites[fila][frame_index], (parte[0], parte[1]))  # cabeza (animada)
        else:
            screen.blit(bag_img, (parte[0], parte[1]))  # cuerpo (saco)

# ------------------------------------
# LOOP PRINCIPAL
# ------------------------------------
def main():
    cuerpo = [[WIDTH // 2, HEIGHT // 2]]
    direccion = "DERECHA"
    longitud = 1
    basura = generar_basura()
    puntuacion = 0

    frame_index = 0
    frame_counter = 0
    tiempo_max = 45  # segundos
    start_ticks = pygame.time.get_ticks()

    while True:
        # EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direccion = "ARRIBA"
                elif event.key == pygame.K_DOWN:
                    direccion = "ABAJO"
                elif event.key == pygame.K_LEFT:
                    direccion = "IZQUIERDA"
                elif event.key == pygame.K_RIGHT:
                    direccion = "DERECHA"

        # MOVIMIENTO
        cabeza = list(cuerpo[-1])
        if direccion == "ARRIBA":
            cabeza[1] -= TAM_CELDA
        elif direccion == "ABAJO":
            cabeza[1] += TAM_CELDA
        elif direccion == "IZQUIERDA":
            cabeza[0] -= TAM_CELDA
        elif direccion == "DERECHA":
            cabeza[0] += TAM_CELDA
        cuerpo.append(cabeza)

        # Animación (cambia frame cada 3 ciclos)
        frame_counter += 1
        if frame_counter >= 3:
            frame_counter = 0
            frame_index = (frame_index + 1) % 4

        # COLISIÓN CON BASURA
        cabeza_rect = pygame.Rect(cabeza[0], cabeza[1], TAM_CELDA, TAM_CELDA)
        basura_rect = pygame.Rect(basura[0], basura[1], TAM_CELDA, TAM_CELDA)
        if cabeza_rect.colliderect(basura_rect):
            puntuacion += 1
            longitud += 1
            basura = generar_basura()
        elif len(cuerpo) > longitud:
            del cuerpo[0]

        # COLISIONES
        if (cabeza[0] < 0 or cabeza[0] >= WIDTH or
            cabeza[1] < 0 or cabeza[1] >= HEIGHT or
            cabeza in cuerpo[:-1]):
            screen.blit(defeat_img, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            return

        # TIEMPO
        segundos = (pygame.time.get_ticks() - start_ticks) // 1000
        restante = max(0, tiempo_max - segundos)
        if restante == 0:
            screen.blit(victory_img, (0, 0))
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        # DIBUJAR
        screen.blit(background_img, (0, 0))
        dibujar_cuerpo(cuerpo, direccion, frame_index)
        screen.blit(trash_img, (basura[0], basura[1]))
        mostrar_texto(f"Basura recolectada: {puntuacion}", BLANCO, 10, 10)
        mostrar_texto(f"Tiempo: {restante}", BLANCO, 10, 40)

        pygame.display.flip()
        clock.tick(FPS)

# ------------------------------------
# aqi LA EJECUCION
if __name__ == "__main__":
    main()
