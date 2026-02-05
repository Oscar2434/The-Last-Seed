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
import ui_nivel3
import pause_menu

pygame.init()

def cargar_imagen_bolsa():
    base_path = os.path.join("assets", "images", "effects")
    try:
        img = pygame.image.load(os.path.join(base_path, "bolsa.png")).convert_alpha()
    except:
        img = pygame.image.load(os.path.join(base_path, "basura.png")).convert_alpha()
    return img

def show_tutorial_screens(screen, level_number):
    if config.lenguaje:
        tutorial_path = "assets/images/turorial en español"
    else:
        tutorial_path = "assets/images/tutorial en ingles"
    
    try:
        universal_img = pygame.image.load(os.path.join(tutorial_path, "universal.png")).convert_alpha()
        level_img = pygame.image.load(os.path.join(tutorial_path, f"N{level_number}.png")).convert_alpha()
        continue_img = pygame.image.load("assets/images/Buttons/continuar.png").convert_alpha()
        continue_img = pygame.transform.scale(continue_img, (int(continue_img.get_width() * 0.5), int(continue_img.get_height() * 0.5)))

    except pygame.error as e:
        print(f"Error cargando imágenes de tutorial: {e}")
        return False
    
    universal_img = pygame.transform.scale(universal_img, (constants.WIDTH, constants.HEIGHT))
    level_img = pygame.transform.scale(level_img, (constants.WIDTH, constants.HEIGHT))
    
    continue_rect = continue_img.get_rect(center=(750, 450))
    
    current_screen = 0
    screens = [universal_img, level_img]
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    current_screen += 1
                    if current_screen >= len(screens):
                        return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_rect.collidepoint(event.pos):
                    current_screen += 1
                    if current_screen >= len(screens):
                        return True
        
        screen.blit(screens[current_screen], (0, 0))
        screen.blit(continue_img, continue_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return True

def draw_timer_transparent(screen, remaining_time, total_time, x, y, cabeza_rect):
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    time_text = f"{minutes:02d}:{seconds:02d}"
    
    font = pygame.font.Font(None, 40)
    
    if remaining_time > total_time * 0.6:
        color = constants.GREEN
    elif remaining_time > total_time * 0.3:
        color = constants.YELLOW
    else:
        color = constants.RED
    
    text_surface = font.render(time_text, True, color)
    
    bg_rect = text_surface.get_rect()
    bg_rect.x = x - 10
    bg_rect.y = y - 5
    bg_rect.width += 20
    bg_rect.height += 10
    
    if cabeza_rect and cabeza_rect.colliderect(bg_rect):
        alpha_bg = 100
        alpha_text = 180
    else:
        alpha_bg = 180
        alpha_text = 255
    
    bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(bg_surface, (0, 0, 0, alpha_bg), bg_surface.get_rect(), border_radius=8)
    pygame.draw.rect(bg_surface, (255, 255, 255, 100), bg_surface.get_rect(), 2, border_radius=8)
    
    screen.blit(bg_surface, (bg_rect.x, bg_rect.y))
    
    text_with_alpha = text_surface.copy()
    text_with_alpha.set_alpha(alpha_text)
    screen.blit(text_with_alpha, (x, y))
    
    if remaining_time < 10:
        pulse = (pygame.time.get_ticks() // 200) % 2
        if pulse == 0:
            glow_rect = bg_rect.copy()
            glow_rect.x -= 2
            glow_rect.y -= 2
            glow_rect.width += 4
            glow_rect.height += 4
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (255, 50, 50, 100), glow_surface.get_rect(), 3, border_radius=10)
            screen.blit(glow_surface, (glow_rect.x, glow_rect.y))

def dibujar_hud_traducido(screen, tiempo, recogidas, objetivo, tiempo_total, cabeza_rect):
    draw_timer_transparent(screen, tiempo, tiempo_total, 10, 10, cabeza_rect)
    
    if config.lenguaje:
        texto_basura = f"Basura: {recogidas}/{objetivo}"
    else:
        texto_basura = f"Trash: {recogidas}/{objetivo}"
    
    font = pygame.font.SysFont(None, constants.TRASH_HUD_FONT_SIZE)
    
    texto2 = font.render(texto_basura, True, (255, 255, 220))
    
    bg_rect = texto2.get_rect()
    bg_width = max(texto2.get_width() + constants.TRASH_HUD_BG_PADDING * 2, constants.TRASH_HUD_MIN_WIDTH)
    bg_rect.width = bg_width
    bg_rect.height = texto2.get_height() + constants.TRASH_HUD_BG_PADDING
    bg_rect.x = constants.TRASH_HUD_PADDING_LEFT
    bg_rect.y = constants.TRASH_HUD_PADDING_TOP
    
    if cabeza_rect and cabeza_rect.colliderect(bg_rect):
        alpha_bg = 100
        alpha_text = 180
    else:
        alpha_bg = 180
        alpha_text = 255
    
    bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(bg_surface, (0, 0, 0, alpha_bg), bg_surface.get_rect(), border_radius=8)
    pygame.draw.rect(bg_surface, (255, 255, 255, 100), bg_surface.get_rect(), 2, border_radius=8)
    
    screen.blit(bg_surface, (bg_rect.x, bg_rect.y))
    
    text_x = bg_rect.x + (bg_rect.width - texto2.get_width()) // 2
    text_y = bg_rect.y + constants.TRASH_HUD_BG_PADDING // 2
    
    text_with_alpha = texto2.copy()
    text_with_alpha.set_alpha(alpha_text)
    screen.blit(text_with_alpha, (text_x, text_y))

def main():
    try:
        pygame.mixer.music.fadeout(800)
    except:
        pass

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
    
    while True:
        config.update_global_config()
        
        screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        clock = pygame.time.Clock()

        pause_icon_raw = pygame.image.load("assets/images/effects/pausa.png").convert_alpha()
        pause_icon = pygame.transform.scale(pause_icon_raw, (35, 35))
        pause_rect = pause_icon.get_rect(center=(constants.WIDTH // 2, 20))

        if not show_tutorial_screens(screen, 3):
            return "menu"

        start_level_music()

        world = world_nivel3.World(constants.WIDTH, constants.HEIGHT)

        if getattr(config, "difficulty", "normal") == "avanzado":
            velocidad = 5
            objetivo = 20
            tiempo_total = 40
        else:
            velocidad = 4
            objetivo = 12
            tiempo_total = 60

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
        pause_start_time = 0
        total_pause_time = 0

        while True:
            current_time = pygame.time.get_ticks()
            cabeza = jugador.get_head_rect()
            
            for event in pygame.event.get(pump=False):
                if event.type == config.OPEN_MENU_EVENT:
                    stop_level_music()
                    return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_level_music()
                    pygame.quit()
                    sys.exit()

                if event.type == config.OPEN_MENU_EVENT:
                    stop_level_music()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = True
                        pause_start_time = current_time
                        result = pause_menu.show_pause_menu(screen, "level3")
                        game_paused = False
                        total_pause_time += (pygame.time.get_ticks() - pause_start_time)
                        
                        if result == "restart":
                            restart_requested = True
                        elif result == "menu":
                            stop_level_music()
                            return
                        
                        if config.music and not pygame.mixer.music.get_busy():
                            start_level_music()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_rect.collidepoint(event.pos):
                        game_paused = True
                        pause_start_time = current_time
                        result = pause_menu.show_pause_menu(screen, "level3")
                        game_paused = False
                        total_pause_time += (pygame.time.get_ticks() - pause_start_time)
                        
                        if result == "restart":
                            restart_requested = True
                        elif result == "menu":
                            stop_level_music()
                            return
                        
                        if config.music and not pygame.mixer.music.get_busy():
                            start_level_music()

            if restart_requested:
                break

            if game_paused:
                continue

            keys = pygame.key.get_pressed()
            jugador.mover_perpetuo(keys)

            nuevas_basuras = []
            for b in basura:
                if cabeza.colliderect(b.rect):
                    recogidas += 1
                    jugador.crecer()
                else:
                    nuevas_basuras.append(b)
            basura = nuevas_basuras

            if snake_logic.fuera_de_limites(jugador, constants.WIDTH, constants.HEIGHT):
                if config.lenguaje:
                    lose_img = pygame.image.load(os.path.join("assets", "images", "effects", "perder.png")).convert_alpha()
                else:
                    lose_img = pygame.image.load(os.path.join("assets", "images", "effects", "perderI.png")).convert_alpha()
                lose_img = pygame.transform.scale(lose_img, (constants.WIDTH, constants.HEIGHT))
                screen.blit(lose_img, (0, 0))
                pygame.display.update()
                pygame.time.delay(2000)
                
                game_paused = True
                pause_start_time = pygame.time.get_ticks()
                result = pause_menu.show_pause_menu(screen, "level3")
                game_paused = False
                total_pause_time += (pygame.time.get_ticks() - pause_start_time)
                
                if result == "restart":
                    restart_requested = True
                elif result == "menu":
                    stop_level_music()
                    return
                else:
                    restart_requested = True
                
                continue

            if snake_logic.colision_obstaculos(jugador, world.obstacles):
                if config.lenguaje:
                    lose_img = pygame.image.load(os.path.join("assets", "images", "effects", "perder.png")).convert_alpha()
                else:
                    lose_img = pygame.image.load(os.path.join("assets", "images", "effects", "perderI.png")).convert_alpha()
                lose_img = pygame.transform.scale(lose_img, (constants.WIDTH, constants.HEIGHT))
                screen.blit(lose_img, (0, 0))
                pygame.display.update()
                pygame.time.delay(2000)
                
                game_paused = True
                pause_start_time = pygame.time.get_ticks()
                result = pause_menu.show_pause_menu(screen, "level3")
                game_paused = False
                total_pause_time += (pygame.time.get_ticks() - pause_start_time)
                
                if result == "restart":
                    restart_requested = True
                elif result == "menu":
                    stop_level_music()
                    return
                else:
                    restart_requested = True
                
                continue

            if recogidas >= objetivo and len(jugador.cola) > 0:
                cola_rect = jugador.cola[-1]
                if cola_rect.colliderect(world.bote.rect):
                    if config.lenguaje:
                        victory_img = pygame.image.load(os.path.join("assets", "images", "effects", "ganar.png")).convert_alpha()
                    else:
                        victory_img = pygame.image.load(os.path.join("assets", "images", "effects", "ganarI.png")).convert_alpha()
                    victory_img = pygame.transform.scale(victory_img, (constants.WIDTH, constants.HEIGHT))
                    screen.blit(victory_img, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(2000)
                    
                    game_paused = True
                    pause_start_time = pygame.time.get_ticks()
                    result = pause_menu.show_pause_menu(screen, "level3")
                    game_paused = False
                    total_pause_time += (pygame.time.get_ticks() - pause_start_time)
                    
                    if result == "restart":
                        restart_requested = True
                    elif result == "menu":
                        stop_level_music()
                        return
                    else:
                        restart_requested = True
                    
                    continue

            current_time = pygame.time.get_ticks()
            if game_paused:
                effective_time = (pause_start_time - inicio) - total_pause_time
            else:
                effective_time = (current_time - inicio) - total_pause_time
            
            tiempo_transcurrido = effective_time // 1000
            tiempo_restante = max(0, tiempo_total - tiempo_transcurrido)
            
            if tiempo_restante == 0:
                if config.lenguaje:
                    lose_img = pygame.image.load(os.path.join("assets", "images", "effects", "perder.png")).convert_alpha()
                else:
                    lose_img = pygame.image.load(os.path.join("assets", "images", "effects", "perderI.png")).convert_alpha()
                lose_img = pygame.transform.scale(lose_img, (constants.WIDTH, constants.HEIGHT))
                screen.blit(lose_img, (0, 0))
                pygame.display.update()
                pygame.time.delay(2000)
                
                game_paused = True
                pause_start_time = pygame.time.get_ticks()
                result = pause_menu.show_pause_menu(screen, "level3")
                game_paused = False
                total_pause_time += (pygame.time.get_ticks() - pause_start_time)
                
                if result == "restart":
                    restart_requested = True
                elif result == "menu":
                    stop_level_music()
                    return
                else:
                    restart_requested = True
                
                continue

            world.draw(screen)
            for b in basura:
                b.dibujar(screen)
            jugador.dibujar(screen, bolsa_img)
            
            dibujar_hud_traducido(screen, tiempo_restante, recogidas, objetivo, tiempo_total, cabeza)
            
            screen.blit(pause_icon, pause_rect)

            if pause_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 255, 0), pause_rect, 2)

            pygame.display.update()
            clock.tick(60)

        if restart_requested:
            continue

if __name__ == "__main__":
    main()