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
TAM_CELDA = 45
VELOCIDAD = 18
FPS = 15
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nivel 3 - Recolecta de basura")

# COLORES Y FUENTES
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
FUENTE = pygame.font.SysFont("arial", 28, True)
FUENTE_GRANDE = pygame.font.SysFont("arial", 80, True)

# ------------------------------------
# CARGA DE IMÁGENES
# ------------------------------------
def cargar_y_escalar(ruta, escala=1.0):
    img = pygame.image.load(ruta).convert_alpha()
    tamaño = int(TAM_CELDA * escala)
    return pygame.transform.scale(img, (tamaño, tamaño))

background_img = pygame.image.load(os.path.join('assets', 'images', 'objects', 'grass3.png')).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

ESCALA_NIÑO = 1.25
ESCALA_BASURA = 1.1

trash_img = cargar_y_escalar(os.path.join('assets', 'images', 'character', 'escombro.png'), ESCALA_BASURA)
bag_img = cargar_y_escalar(os.path.join('assets', 'images', 'character', 'basura.png'), 1.0)
bote_img = cargar_y_escalar(os.path.join('assets', 'images', 'character', 'bote de basuraaa.png'), 1.6)

# Brillo del bote (efecto)
bote_glow = bote_img.copy()
bote_glow.fill((255, 255, 150, 80), special_flags=pygame.BLEND_RGBA_ADD)

# Fondos de victoria y derrota
victory_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'victoria.png')).convert()
victory_img = pygame.transform.smoothscale(victory_img, (WIDTH, HEIGHT))

defeat_img = pygame.image.load(os.path.join('assets', 'images', 'effects', 'derrota.png')).convert()
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

nino_sprites = cargar_spritesheet(os.path.join('assets', 'images', 'character', 'nino.png'), 4, 4)

DIRECCIONES = {
    "ABAJO": 0,
    "IZQUIERDA": 1,
    "DERECHA": 2,
    "ARRIBA": 3
}

# ------------------------------------
# FUNCIONES
# ------------------------------------
def mostrar_texto_contorno(texto, fuente, color, x, y):
    render_texto = fuente.render(texto, True, color)
    render_contorno = fuente.render(texto, True, NEGRO)
    for dx in (-2, 0, 2):
        for dy in (-2, 0, 2):
            if dx != 0 or dy != 0:
                screen.blit(render_contorno, (x + dx, y + dy))
    screen.blit(render_texto, (x, y))

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
        texto = str(i)
        render_texto = FUENTE_GRANDE.render(texto, True, BLANCO)
        render_contorno = FUENTE_GRANDE.render(texto, True, NEGRO)
        for dx in (-3, 0, 3):
            for dy in (-3, 0, 3):
                if dx != 0 or dy != 0:
                    screen.blit(render_contorno, (WIDTH // 2 - render_texto.get_width() // 2 + dx, HEIGHT // 2 - render_texto.get_height() // 2 + dy))
        screen.blit(render_texto, (WIDTH // 2 - render_texto.get_width() // 2, HEIGHT // 2 - render_texto.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(1000)

    screen.blit(background_img, (0, 0))
    texto = "¡Listo!"
    render_texto = FUENTE_GRANDE.render(texto, True, BLANCO)
    render_contorno = FUENTE_GRANDE.render(texto, True, NEGRO)
    for dx in (-3, 0, 3):
        for dy in (-3, 0, 3):
            if dx != 0 or dy != 0:
                screen.blit(render_contorno, (WIDTH // 2 - render_texto.get_width() // 2 + dx, HEIGHT // 2 - render_texto.get_height() // 2 + dy))
    screen.blit(render_texto, (WIDTH // 2 - render_texto.get_width() // 2, HEIGHT // 2 - render_texto.get_height() // 2))
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
    modo_libre = False
    bote_rect = None
    brillo_activo = False
    brillo_tiempo = 0

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

        if not modo_libre:
            cabeza_rect = pygame.Rect(cabeza[0] + 6, cabeza[1] + 6, TAM_CELDA - 12, TAM_CELDA - 12)
            basura_rect = pygame.Rect(basura[0], basura[1], TAM_CELDA, TAM_CELDA)
            if cabeza_rect.colliderect(basura_rect):
                puntuacion += 1
                longitud += 1
                basura = generar_basura()
            elif len(cuerpo) > longitud:
                del cuerpo[0]

            if puntuacion >= 10:
                modo_libre = True
                bote_rect = bote_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                continue

            if (cabeza[0] < 0 or cabeza[0] + TAM_CELDA > WIDTH or
                cabeza[1] < 0 or cabeza[1] + TAM_CELDA > HEIGHT or
                cabeza in cuerpo[:-1]):
                screen.blit(defeat_img, (0, 0))
                pygame.display.flip()
                pygame.time.delay(3000)
                return

            segundos = (pygame.time.get_ticks() - start_ticks) // 1000
            restante = max(0, tiempo_max - segundos)
            if restante == 0:
                modo_libre = True
                bote_rect = bote_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                continue

        else:
            if len(cuerpo) > longitud:
                del cuerpo[0]

            cabeza_rect = pygame.Rect(cabeza[0], cabeza[1], TAM_CELDA, TAM_CELDA)

            # Colisión con el bote de basura
            if cabeza_rect.colliderect(bote_rect):
                if direccion == "ARRIBA":
                    cabeza[1] += VELOCIDAD
                elif direccion == "ABAJO":
                    cabeza[1] -= VELOCIDAD
                elif direccion == "IZQUIERDA":
                    cabeza[0] += VELOCIDAD
                elif direccion == "DERECHA":
                    cabeza[0] -= VELOCIDAD

                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    brillo_activo = True
                    brillo_tiempo = pygame.time.get_ticks()

            if brillo_activo:
                if pygame.time.get_ticks() - brillo_tiempo > 800:
                    screen.blit(victory_img, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(2500)
                    return

        # DIBUJO
        screen.blit(background_img, (0, 0))
        dibujar_cuerpo(cuerpo, direccion, frame_index)

        if not modo_libre:
            screen.blit(trash_img, (basura[0], basura[1]))
            mostrar_texto_contorno(f"Basura recolectada: {puntuacion}", FUENTE, BLANCO, 10, 10)
            mostrar_texto_contorno(f"Tiempo: {restante}", FUENTE, BLANCO, 10, 40)
        else:
            mostrar_texto_contorno("Lleva la basura a su lugar.", FUENTE, BLANCO, WIDTH // 2 - 170, 20)
            screen.blit(bote_img, bote_rect)
            mostrar_texto_contorno("Presiona E.", FUENTE, BLANCO, bote_rect.centerx - 60, bote_rect.top - 40)

            # Efecto brillo
            if brillo_activo:
                screen.blit(bote_glow, bote_rect)

        pygame.display.flip()
        clock.tick(FPS)

# ------------------------------------
# EJECUCIÓN
# ------------------------------------
if __name__ == "__main__":
    main()
