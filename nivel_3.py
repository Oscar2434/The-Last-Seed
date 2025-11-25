import pygame
import sys
import os
import random
import constants
import config
import world_nivel3
import player_nivel3
import objects_nivel3
import snake_logic
import pause_menu  # IMPORTAR MENÚ DE PAUSA

pygame.init()

def cargar_imagen_bolsa():
    base_path = os.path.join("assets", "images", "effects")
    try:
        img = pygame.image.load(os.path.join(base_path, "bolsa.png")).convert_alpha()
    except:
        img = pygame.image.load(os.path.join(base_path, "basura.png")).convert_alpha()
    return img

def dibujar_hud(screen, tiempo, recogidas, objetivo):
    # Obtener textos según el idioma
    if config.lenguaje:  # Español
        texto_tiempo = f"Tiempo: {tiempo}"
        texto_basura = f"Basura: {recogidas}/{objetivo}"
    else:  # Inglés
        texto_tiempo = f"Time: {tiempo}"
        texto_basura = f"Trash: {recogidas}/{objetivo}"
    
    font = pygame.font.SysFont(None, 36)
    
    # Renderizar textos
    texto1 = font.render(texto_tiempo, True, constants.BLACK)
    texto2 = font.render(texto_basura, True, constants.BLACK)
    
    # Dibujar textos en la pantalla
    screen.blit(texto1, (10, 10))
    screen.blit(texto2, (10, 50))

def main():
    # --- DETENER MÚSICA DEL MENÚ ---
    try:
        pygame.mixer.music.fadeout(800)
    except:
        pass

    # --- INICIAR MÚSICA DEL NIVEL 3 ---
    def start_level_music():
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.music.load("music/m3.mp3")
            pygame.mixer.music.set_volume(config.volume_master)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Error cargando música nivel 3:", e)
    
    def stop_level_music():
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
    # Bucle principal para reinicios
    while True:
        # Actualizar configuración al inicio
        config.update_global_config()
        
        # Iniciar música del nivel
        start_level_music()

        screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        clock = pygame.time.Clock()

        # === BOTÓN DE PAUSA ===
        pause_icon_raw = pygame.image.load("assets/images/effects/pausa.png").convert_alpha()
        pause_icon = pygame.transform.scale(pause_icon_raw, (35, 35))
        pause_rect = pause_icon.get_rect(center=(constants.WIDTH // 2, 20))

        # Imágenes de victoria y derrota a pantalla completa
        victory_img = pygame.image.load(
            os.path.join("assets", "images", "effects", "ganar.png")
        ).convert_alpha()

        lose_img = pygame.image.load(
            os.path.join("assets", "images", "effects", "perder.png")
        ).convert_alpha()

        victory_img = pygame.transform.scale(victory_img, (constants.WIDTH, constants.HEIGHT))
        lose_img = pygame.transform.scale(lose_img, (constants.WIDTH, constants.HEIGHT))

        world = world_nivel3.World(constants.WIDTH, constants.HEIGHT)

        if getattr(config, "difficulty", "normal") == "avanzado":
            velocidad = 5
            objetivo = 20
        else:
            velocidad = 4
            objetivo = 12

        start_x = constants.WIDTH // 2 - constants.PERSONAJE // 2
        start_y = constants.HEIGHT - constants.PERSONAJE - 20
        jugador = player_nivel3.SnakePlayer(start_x, start_y, velocidad)

        bolsa_img = cargar_imagen_bolsa()
        bolsa_img = pygame.transform.scale(bolsa_img, (40, 40))

        basura = objects_nivel3.generar_basura(
            objetivo, bolsa_img, constants.WIDTH, constants.HEIGHT, world
        )

        inicio = pygame.time.get_ticks()
        recogidas = 0
        game_paused = False
        restart_requested = False

        while True:
            # VERIFICAR EVENTOS DE NAVEGACIÓN
            for event in pygame.event.get(pump=False):
                if event.type == config.OPEN_MENU_EVENT:
                    stop_level_music()
                    return  # Salir al menú principal

            # === EVENTOS ORIGINALES DEL NIVEL ===
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_level_music()
                    pygame.quit()
                    sys.exit()

                if event.type == config.OPEN_MENU_EVENT:
                    stop_level_music()
                    return  # Salir al menú principal

                if event.type == pygame.KEYDOWN:
                    # TECLA ESC → ABRE MENÚ DE PAUSA
                    if event.key == pygame.K_ESCAPE:
                        game_paused = True
                        result = pause_menu.show_pause_menu(screen, "level3")
                        game_paused = False
                        
                        # Manejar resultado del menú de pausa
                        if result == "restart":
                            restart_requested = True
                        elif result == "menu":
                            stop_level_music()
                            return
                        
                        # Reanudar música si se detuvo por configuración
                        if config.music and not pygame.mixer.music.get_busy():
                            start_level_music()

                # CLICK EN BOTÓN DE PAUSA
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_rect.collidepoint(event.pos):
                        game_paused = True
                        result = pause_menu.show_pause_menu(screen, "level3")
                        game_paused = False
                        
                        # Manejar resultado del menú de pausa
                        if result == "restart":
                            restart_requested = True
                        elif result == "menu":
                            stop_level_music()
                            return
                        
                        # Reanudar música si se detuvo por configuración
                        if config.music and not pygame.mixer.music.get_busy():
                            start_level_music()

            # Verificar si se solicitó reinicio
            if restart_requested:
                break  # Romper el bucle interno y reiniciar

            # Si el juego está en pausa, saltar el resto de la lógica
            if game_paused:
                continue

            keys = pygame.key.get_pressed()
            jugador.mover_perpetuo(keys)

            cabeza = jugador.get_head_rect()

            nuevas_basuras = []
            for b in basura:
                if cabeza.colliderect(b.rect):
                    recogidas += 1
                    jugador.crecer()
                else:
                    nuevas_basuras.append(b)
            basura = nuevas_basuras

            if snake_logic.fuera_de_limites(jugador, constants.WIDTH, constants.HEIGHT):
                screen.blit(lose_img, (0, 0))
                pygame.display.update()
                pygame.time.delay(2000)
                
                # Mostrar menú de pausa después de derrota
                game_paused = True
                result = pause_menu.show_pause_menu(screen, "level3")
                game_paused = False
                
                if result == "restart":
                    restart_requested = True
                elif result == "menu":
                    stop_level_music()
                    return
                else:
                    # Por defecto, reiniciar si no se elige menú
                    restart_requested = True
                
                # Continuar al siguiente ciclo
                continue

            if snake_logic.colision_obstaculos(jugador, world.obstacles):
                screen.blit(lose_img, (0, 0))
                pygame.display.update()
                pygame.time.delay(2000)
                
                # Mostrar menú de pausa después de derrota
                game_paused = True
                result = pause_menu.show_pause_menu(screen, "level3")
                game_paused = False
                
                if result == "restart":
                    restart_requested = True
                elif result == "menu":
                    stop_level_music()
                    return
                else:
                    # Por defecto, reiniciar si no se elige menú
                    restart_requested = True
                
                # Continuar al siguiente ciclo
                continue

            if recogidas >= objetivo and len(jugador.cola) > 0:
                cola_rect = jugador.cola[-1]
                if cola_rect.colliderect(world.bote.rect):
                    screen.blit(victory_img, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    
                    # Mostrar menú de pausa después de victoria
                    game_paused = True
                    result = pause_menu.show_pause_menu(screen, "level3")
                    game_paused = False
                    
                    if result == "restart":
                        restart_requested = True
                    elif result == "menu":
                        stop_level_music()
                        return
                    else:
                        # Por defecto, reiniciar si no se elige menú
                        restart_requested = True
                    
                    # Continuar al siguiente ciclo
                    continue

            tiempo = (pygame.time.get_ticks() - inicio) // 1000

            world.draw(screen)
            for b in basura:
                b.dibujar(screen)
            jugador.dibujar(screen, bolsa_img)
            dibujar_hud(screen, tiempo, recogidas, objetivo)  # LLAMADA A LA FUNCIÓN LOCAL
            
            # === MOSTRAR BOTÓN DE PAUSA ===
            screen.blit(pause_icon, pause_rect)

            # HOVER amarillo del botón de pausa
            if pause_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 255, 0), pause_rect, 2)

            pygame.display.update()
            clock.tick(60)

        # Si salimos del bucle interno por reinicio, continuamos el bucle externo
        if restart_requested:
            continue

if __name__ == "__main__":
    main()