import pygame
import os
import sys

# === CORRECCIÓN DE IMPORTS ===
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import constants
# === FIN DE CORRECCIÓN ===

class DialogManager:
    def __init__(self):
        self.dialog_queue = []
        self.game_paused = False
        self.dialog_timer = 0
        self.auto_close_time = 10000  # 10 segundos

        # Definir diálogos de recursos y árbol
        self.resource_dialogs = {
            "composta": "¡Excelente! La cascara de platano servira como composta para la plantas. \nLa comoposta son nutrientes que ayudaran a las plantas a crecer fuertes.",
            "semillas": "¡Excelente! La cáscara de huevo es rica en calcio y otros minerales que\nbenefician el suelo y las plantas.",
            "agua": "¡Perfecto! ¡El agua es importante para las plantas y transporta sus \nnutrientes por toda la planta!"
        }

        self.tree_dialogs = {
            "need_resources": [
                "El árbol central necesita todos los",
                "recursos para crecer fuerte.",
                "Recolecta composta, agua y semillas primero."
            ],
            "all_collected": [
                "¡Has recolectado todos los recursos!",
                "Ahora ve al árbol central y",
                "presiona 'E' para entregarlos."
            ]
        }

    def add_resource_dialog(self, resource_type):
        """Añade el diálogo correspondiente a un recurso"""
        if resource_type in self.resource_dialogs:
            self.dialog_queue.append(self.resource_dialogs[resource_type])
            self.game_paused = True
            self.dialog_timer = pygame.time.get_ticks()

    def add_tree_dialog(self, dialog_key):
        """Añade diálogo del árbol central"""
        if dialog_key in self.tree_dialogs:
            self.dialog_queue.extend(self.tree_dialogs[dialog_key])
            self.game_paused = True
            self.dialog_timer = pygame.time.get_ticks()

    def update(self, current_time):
        """Actualiza el estado de los diálogos (para cierre automático)"""
        if self.game_paused and self.dialog_queue and (current_time - self.dialog_timer > self.auto_close_time):
            # Limpia todos los diálogos en lugar de solo el primero
            self.dialog_queue.clear()
            self.game_paused = False

    def next_dialog(self):
        """Cierra completamente el diálogo actual al presionar ESPACIO"""
        self.dialog_queue.clear()
        self.game_paused = False

    def has_dialogs(self):
        """Indica si hay diálogos en cola"""
        return len(self.dialog_queue) > 0

    def get_current_dialog_text(self, max_lines=8):
        """Obtiene el texto actual para mostrar (hasta max_lines líneas)"""
        return "\n".join(self.dialog_queue[:max_lines])

    def draw(self, screen):
        """Dibuja el diálogo en pantalla si hay diálogos y el juego está pausado"""
        if self.game_paused and self.dialog_queue:
            self._draw_dialog_box(screen, self.get_current_dialog_text())

    def _draw_dialog_box(self, screen, text):
        """Dibuja la caja de diálogo con el texto"""
        dialog_rect = pygame.Rect(40, constants.HEIGHT - 180, constants.WIDTH - 80, 160)
        
        # Fondo del diálogo
        pygame.draw.rect(screen, (255, 255, 255), dialog_rect)
        pygame.draw.rect(screen, (0, 100, 0), dialog_rect, 3)
        
        # Texto
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
        
        # Texto de continuación
        continue_font = pygame.font.SysFont(None, 20)
        continue_text = continue_font.render("Presiona ESPACIO para continuar...", True, (100, 100, 100))
        screen.blit(continue_text, (dialog_rect.x + 20, dialog_rect.y + dialog_rect.height - 30))

        # Temporizador de cierre automático
        time_left = 10 - ((pygame.time.get_ticks() - self.dialog_timer) // 1000)
        if time_left < 11:
            time_font = pygame.font.SysFont(None, 20)
            time_text = time_font.render(f"Desaparece en: {time_left}s", True, (255, 220, 0))
            screen.blit(time_text, (constants.WIDTH - 150, constants.HEIGHT - 190))