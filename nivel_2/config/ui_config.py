# Configuraciones de interfaz de usuario
import pygame

# Diálogos
DIALOG_CONFIG = {
    "box_rect": (40, 300, 700, 160),  # x, y, width, height
    "font_size": 22,
    "line_spacing": 22
}

# Inventario
INVENTORY_CONFIG = {
    "position": (630, 10),
    "size": (140, 80),
    "font_size": 20
}

# Nombres para mostrar en inventario
RESOURCE_DISPLAY_NAMES = {
    "composta": "Cáscara Plátano",
    "agua": "Agua",
    "semillas": "Cáscara Huevo"
}

def draw_dialog(screen, text, constants):
    """Dibuja el cuadro de diálogo en pantalla"""
    dialog_rect = pygame.Rect(40, constants.HEIGHT - 180, constants.WIDTH - 80, 160)
    
    pygame.draw.rect(screen, (255, 255, 255), dialog_rect)
    pygame.draw.rect(screen, (0, 100, 0), dialog_rect, 3)
    
    font = pygame.font.SysFont(None, 22)
    y_offset = dialog_rect.y + 15
    
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split(' ')
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < dialog_rect.width - 40:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
    
    for line in lines:
        if y_offset + 20 > dialog_rect.y + dialog_rect.height - 30:
            break
        text_surface = font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (dialog_rect.x + 20, y_offset))
        y_offset += 22
    
    continue_font = pygame.font.SysFont(None, 20)
    continue_text = continue_font.render("Presiona ESPACIO para continuar...", True, (100, 100, 100))
    screen.blit(continue_text, (dialog_rect.x + 20, dialog_rect.y + dialog_rect.height - 30))

def draw_inventory(screen, collected_resources, constants):
    """Dibuja el inventario en pantalla"""
    inventory_bg = pygame.Rect(constants.WIDTH - 150, 10, 140, 80)
    
    transparent_bg = pygame.Surface((inventory_bg.width, inventory_bg.height), pygame.SRCALPHA)
    pygame.draw.rect(transparent_bg, (0, 0, 0, 80), transparent_bg.get_rect())
    pygame.draw.rect(transparent_bg, (100, 100, 100, 100), transparent_bg.get_rect(), 1)
    
    screen.blit(transparent_bg, inventory_bg)
    
    font = pygame.font.SysFont(None, 20)
    
    title_shadow = font.render("Inventario:", True, (0, 0, 0, 100))
    screen.blit(title_shadow, (constants.WIDTH - 139, 16))
    
    title = font.render("Inventario:", True, (255, 255, 255))
    screen.blit(title, (constants.WIDTH - 140, 15))
    
    y_offset = 35
    for resource_type in ["composta", "agua", "semillas"]:
        count = collected_resources.count(resource_type)
        display_name = RESOURCE_DISPLAY_NAMES.get(resource_type, resource_type)
        status = f"{display_name}: {count}" if count > 0 else f"{display_name}: 0"
        color = (200, 250, 200) if count > 0 else (180, 0, 0)
        text = font.render(status, True, color)
        screen.blit(text, (constants.WIDTH - 140, y_offset))
        y_offset += 20

def draw_timer(screen, remaining_time, constants):
    """Dibuja el temporizador en pantalla"""
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Tiempo: {remaining_time}s", True, constants.BLACK)
    screen.blit(text, (10, 10))

def draw_dialog_timer(screen, current_time, dialog_timer, constants):
    """Dibuja el temporizador de desaparición del diálogo"""
    time_left = 12 - ((current_time - dialog_timer) // 1000)
    if time_left < 13:
        time_font = pygame.font.SysFont(None, 20)
        time_text = time_font.render(f"Desaparece en: {time_left}s", True, (255, 220, 0))
        screen.blit(time_text, (constants.WIDTH - 150, constants.HEIGHT - 190))