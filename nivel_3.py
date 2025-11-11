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
TAM_CELDA = 45         # 🔹 Tamaño base de la cuadrícula
VELOCIDAD = 18
FPS = 15
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nivel 3 - Recolecta de basura")

# COLORES Y FUENTES
BLANCO = (255, 255, 255)
FUENTE = pygame.font.SysFont("arial", 28, True)
FUENTE_GRANDE = pygame.font.SysFont("arial", 80, True)

# ------------------------------------
# CARGA DE IMÁGENES
# ------------------------------------
def cargar_y_escalar(ruta, escala=1.0):
    img = pygame.image.load(ruta).convert_alpha()
    tamaño = int(TAM_CELDA * escala)
    return pygame.transform.scale(img, (tamaño, tamaño))

background_img = pygame.image.load(os.path.join('The-Last-Seed', 'assets', 'images', 'objects', 'grass3.png')).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# 🔧 Escalas ajustables
ESCALA_NIÑO = 1.25     # 🔹 Más grande que antes (ajusta entre 1.1 y 1.3)
ESCALA_BASURA = 1.1    # 🔹 Objetos un poco más grandes

trash_img = cargar_y_escalar(os.path.join('The-Last-Seed', 'assets', 'images', 'character', 'escombro.png'), ESCALA_BASURA)
bag_img = cargar_y_escalar(os.path.join('The-Last-Seed', 'assets', 'images', 'character', 'basura.png'), 1.0)

# 🔹 Fondo de victoria y derrota sin bordes visibles
victory_img = pygame.image.load(os.path.join('The-Last-Seed', 'assets', 'images', 'effects', 'victoria.png')).convert()
victory_img = pygame.transform.smoothscale(victory_img, (WIDTH, HEIGHT))

defeat_img = pygame.image.load(os.path.join('The-Last-Seed', 'assets', 'images', 'effects', 'derrota.png')).convert()
defeat_img = pygame.transform.smoothscale(defeat_img, (WIDTH, HEIGHT))

# ------------------------------------
# SPRITES DEL NIÑO
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
            tamaño = int(TAM_CELDA * ESCALA_NIÑO)
            frame = pygame.transform.scale(frame, (tamaño, tamaño))
            fila_sprites.append(frame)
        sprites.append(fila_sprites)
    return sprites

nino_sprites = cargar_spritesheet(os.path.join('The-Last-Seed', 'assets', 'images', 'character', 'nino.png'), 4, 4)

DIRECCIONES = {
    "ABAJO": 0,
    "IZQUIERDA": 1,
    "DERECHA": 2,
    "ARRIBA": 3
}

# ------------------------------------
# FUNCIONES
# ------------------------------------
def mostrar_texto(texto, fuente, color, x, y):
    screen.blit(fuente.render(texto, True, color), (x, y))

def generar_basura():
    margen = 10
    x = random.randrange(margen, WIDTH - TAM_CELDA - margen, VELOCIDAD)
    y = random.randrange(margen, HEIGHT - TAM_CELDA - margen, VELOCIDAD)
    return [x, y]

def dibujar_cuerpo(cuerpo, direccion, frame_index):
    for i, parte in enumerate(cuerpo):
        if i == len(cuerpo) - 1:
            sprite = nino_sprites[DIRECCIONES[direccion]][frame_index]
            offset = (TAM_CELDA * ESCALA_NIÑO - TAM_CELDA) / 2
            screen.blit(sprite, (parte[0] - offset, parte[1] - offset))
        else:
            screen.blit(bag_img, (parte[0], parte[1]))

def cuenta_regresiva_inicial():
    for i in range(3, 0, -1):
        screen.blit(background_img, (0, 0))
        texto = FUENTE_GRANDE.render(str(i), True, BLANCO)
        screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2 - texto.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(1000)

    screen.blit(background_img, (0, 0))
    texto = FUENTE_GRANDE.render("¡Listo!", True, BLANCO)
    screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(1000)

# ------------------------------------
# LOOP PRINCIPAL
# ------------------------------------
def main():
    cuerpo = [[WIDTH // 2 - TAM_CELDA // 2, HEIGHT // 2 - TAM_CELDA // 2]]
    direccion = "DERECHA"
    longitud = 1
    basura = generar_basura()
    puntuacion = 0
    frame_index = 0
    frame_counter = 0
    tiempo_max = 45

    cuenta_regresiva_inicial()
    start_ticks = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direccion != "ABAJO":
                    direccion = "ARRIBA"
                elif event.key == pygame.K_DOWN and direccion != "ARRIBA":
                    direccion = "ABAJO"
                elif event.key == pygame.K_LEFT and direccion != "DERECHA":
                    direccion = "IZQUIERDA"
                elif event.key == pygame.K_RIGHT and direccion != "IZQUIERDA":
                    direccion = "DERECHA"

        cabeza = list(cuerpo[-1])
        if direccion == "ARRIBA":
            cabeza[1] -= VELOCIDAD
        elif direccion == "ABAJO":
            cabeza[1] += VELOCIDAD
        elif direccion == "IZQUIERDA":
            cabeza[0] -= VELOCIDAD
        elif direccion == "DERECHA":
            cabeza[0] += VELOCIDAD
        cuerpo.append(cabeza)

        frame_counter += 1
        if frame_counter >= 3:
            frame_counter = 0
            frame_index = (frame_index + 1) % 4

        # 🔧 Colisión más precisa (golpea exactamente en el borde)
        cabeza_rect = pygame.Rect(cabeza[0] + 6, cabeza[1] + 6, TAM_CELDA - 12, TAM_CELDA - 12)
        basura_rect = pygame.Rect(basura[0], basura[1], TAM_CELDA, TAM_CELDA)
        if cabeza_rect.colliderect(basura_rect):
            puntuacion += 1
            longitud += 1
            basura = generar_basura()
        elif len(cuerpo) > longitud:
            del cuerpo[0]

        margen = 0  # 🔹 Colisión fina con el borde (ajusta si quieres más tolerancia)
        if (cabeza[0] < -margen or cabeza[0] + TAM_CELDA > WIDTH + margen or
            cabeza[1] < -margen or cabeza[1] + TAM_CELDA > HEIGHT + margen or
            cabeza in cuerpo[:-1]):
            screen.fill((0, 0, 0))
            screen.blit(defeat_img, (0, 0))
            pygame.display.flip()
            pygame.time.delay(3000)
            return

        segundos = (pygame.time.get_ticks() - start_ticks) // 1000
        restante = max(0, tiempo_max - segundos)
        if restante == 0:
            screen.fill((0, 0, 0))
            screen.blit(victory_img, (0, 0))
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        screen.blit(background_img, (0, 0))
        dibujar_cuerpo(cuerpo, direccion, frame_index)
        screen.blit(trash_img, (basura[0], basura[1]))
        mostrar_texto(f"Basura recolectada: {puntuacion}", FUENTE, BLANCO, 10, 10)
        mostrar_texto(f"Tiempo: {restante}", FUENTE, BLANCO, 10, 40)

        pygame.display.flip()
        clock.tick(FPS)

# ------------------------------------
# EJECUCIÓN
# ------------------------------------
if __name__ == "__main__":
    main()
