import pygame
import sys
import os

# === CORRECCIÓN DE IMPORTS ===
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import constants
# === FIN DE CORRECCIÓN ===

class PauseMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        
        # Crear superficie semi-transparente para el fondo
        self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))  # Negro semi-transparente
        
        # Configuración de botones
        self.button_width = 200
        self.button_height = 50
        self.button_margin = 20
        
        # Colores de botones
        self.button_color = (70, 130, 180)  # Azul acero
        self.button_hover_color = (100, 160, 210)  # Azul más claro
        self.text_color = (255, 255, 255)  # Blanco
        
        # Crear botones
        self.buttons = self.create_buttons()
        
    def create_buttons(self):
        buttons = []
        
        # Calcular posición central para los botones
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Botón de Continuar
        continue_button = {
            'rect': pygame.Rect(
                center_x - self.button_width // 2,
                center_y - self.button_height - self.button_margin // 2,
                self.button_width,
                self.button_height
            ),
            'text': 'Continuar',
            'action': 'continue'
        }
        
        # Botón de Salir al Menú
        menu_button = {
            'rect': pygame.Rect(
                center_x - self.button_width // 2,
                center_y + self.button_margin // 2,
                self.button_width,
                self.button_height
            ),
            'text': 'Salir al Menú',
            'action': 'menu'
        }
        
        buttons.append(continue_button)
        buttons.append(menu_button)
        
        return buttons
    
    def toggle(self):
        """Alterna el estado del menú de pausa"""
        self.active = not self.active
        return self.active
    
    def draw(self, screen):
        """Dibuja el menú de pausa en la pantalla"""
        if not self.active:
            return
            
        # Dibujar fondo semi-transparente
        screen.blit(self.overlay, (0, 0))
        
        # Dibujar título
        title_font = pygame.font.SysFont(None, 72)
        title_text = title_font.render("PAUSA", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        screen.blit(title_text, title_rect)
        
        # Dibujar botones
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.buttons:
            # Determinar color del botón (hover o normal)
            if button['rect'].collidepoint(mouse_pos):
                color = self.button_hover_color
            else:
                color = self.button_color
            
            # Dibujar botón
            pygame.draw.rect(screen, color, button['rect'])
            pygame.draw.rect(screen, (255, 255, 255), button['rect'], 2)  # Borde
            
            # Dibujar texto del botón
            button_font = pygame.font.SysFont(None, 32)
            button_text = button_font.render(button['text'], True, self.text_color)
            text_rect = button_text.get_rect(center=button['rect'].center)
            screen.blit(button_text, text_rect)
    
    def handle_event(self, event):
        """Maneja eventos del mouse para los botones"""
        if not self.active:
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic izquierdo
            mouse_pos = pygame.mouse.get_pos()
            
            for button in self.buttons:
                if button['rect'].collidepoint(mouse_pos):
                    return button['action']
        
        return None

    def is_active(self):
        """Retorna si el menú de pausa está activo"""
        return self.active