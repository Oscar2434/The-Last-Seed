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
        
        # Variables para control de tiempo
        self.pause_start_time = 0
        self.total_paused_time = 0
        
        # Crear superficie semi-transparente para el fondo
        self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))  # Negro semi-transparente
        
        # Cargar imágenes
        self.load_images()
        
        # Crear botones
        self.buttons = self.create_buttons()
    
    def load_images(self):
        """Carga y escala las imágenes para el menú de pausa"""
        # Cargar título (sin escalar, ya que tiene el tamaño correcto)
        self.title_image = pygame.image.load("imagenes/titulo1.png").convert_alpha()
        
        # Cargar imágenes de botones (usando Exit.png temporalmente para todos)
        button_continue = pygame.image.load("imagenes/Exit.png").convert_alpha()
        button_restart = pygame.image.load("imagenes/Exit.png").convert_alpha()
        button_menu = pygame.image.load("imagenes/Exit.png").convert_alpha()
        
        # Escalar botones - ajusta el factor de escala según necesidad
        scale_factor = 0.4  # Puedes ajustar este valor
        button_width = int(button_continue.get_width() * scale_factor)
        button_height = int(button_continue.get_height() * scale_factor)
        
        self.button_continue = pygame.transform.scale(button_continue, (button_width, button_height))
        self.button_restart = pygame.transform.scale(button_restart, (button_width, button_height))
        self.button_menu = pygame.transform.scale(button_menu, (button_width, button_height))
        
        # Guardar dimensiones de botones para uso posterior
        self.button_width = button_width
        self.button_height = button_height
    
    def create_buttons(self):
        """Crea los botones del menú de pausa"""
        buttons = []
        
        # Calcular posición central para los botones
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Botón de Continuar
        continue_button = {
            'image': self.button_continue,
            'rect': self.button_continue.get_rect(center=(center_x, center_y - 80)),
            'action': 'continue'
        }
        
        # Botón de Reiniciar
        restart_button = {
            'image': self.button_restart,
            'rect': self.button_restart.get_rect(center=(center_x, center_y)),
            'action': 'restart'
        }
        
        # Botón de Salir al Menú
        menu_button = {
            'image': self.button_menu,
            'rect': self.button_menu.get_rect(center=(center_x, center_y + 80)),
            'action': 'menu'
        }
        
        buttons.append(continue_button)
        buttons.append(restart_button)
        buttons.append(menu_button)
        
        return buttons
    
    def toggle(self, current_time):
        """Alterna el estado del menú de pausa y controla el tiempo"""
        self.active = not self.active
        
        if self.active:
            # Iniciar pausa - guardar el momento en que se pausa
            self.pause_start_time = current_time
        else:
            # Terminar pausa - calcular tiempo transcurrido en pausa
            if self.pause_start_time > 0:
                pause_duration = current_time - self.pause_start_time
                self.total_paused_time += pause_duration
                self.pause_start_time = 0
        
        return self.active
    
    def get_effective_time(self, current_time, start_ticks):
        """
        Calcula el tiempo efectivo de juego (tiempo total menos tiempo en pausa)
        """
        current_pause_time = 0
        if self.active and self.pause_start_time > 0:
            current_pause_time = current_time - self.pause_start_time
        
        total_pause_time = self.total_paused_time + current_pause_time
        effective_time = current_time - start_ticks - total_pause_time
        
        return effective_time
    
    def draw(self, screen):
        """Dibuja el menú de pausa en la pantalla"""
        if not self.active:
            return
            
        # Dibujar fondo semi-transparente
        screen.blit(self.overlay, (0, 0))
        
        # Dibujar título ocupando toda la pantalla (sin escalar)
        screen.blit(self.title_image, (0, 0))
        
        # Dibujar botones encima del título (gracias a las áreas transparentes)
        for button in self.buttons:
            # Dibujar botón (solo la imagen, sin texto)
            screen.blit(button['image'], button['rect'])
    
    def handle_event(self, event, current_time):
        """Maneja eventos del mouse para los botones"""
        if not self.active:
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic izquierdo
            mouse_pos = pygame.mouse.get_pos()
            
            for button in self.buttons:
                if button['rect'].collidepoint(mouse_pos):
                    # Si se hace clic en "Continuar", actualizar el tiempo de pausa
                    if button['action'] == 'continue' and self.pause_start_time > 0:
                        pause_duration = current_time - self.pause_start_time
                        self.total_paused_time += pause_duration
                        self.pause_start_time = 0
                    
                    return button['action']
        
        return None

    def is_active(self):
        """Retorna si el menú de pausa está activo"""
        return self.active
    
    def reset(self):
        """Reinicia el contador de tiempo pausado"""
        self.total_paused_time = 0
        self.pause_start_time = 0