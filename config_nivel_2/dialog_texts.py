import pygame
import config

class DialogManager:
    def __init__(self):
        self.dialogs = []
        self.current_dialog_index = 0
        self.game_paused = False
        self.dialog_timer = 0
        self.dialog_duration = 10000  # 10 segundos
        
        # Actualizar configuración
        config.update_global_config()
        
        # Textos según idioma
        if config.lenguaje:  # Español
            self.dialog_texts = {
                "composta": "¡Has recolectado cáscara de plátano!\n\nLas cáscaras de plátano son ricas en nutrientes como potasio, fósforo y calcio, que ayudan a enriquecer el suelo y promover el crecimiento de las plantas.",
                "agua": "¡Has recolectado agua!\n\nEl agua es esencial para la vida de las plantas. Ayuda a transportar nutrientes desde las raíces hasta las hojas y mantiene la planta hidratada y saludable.",
                "semillas": "¡Has recolectado cáscara de huevo!\n\nLas cáscaras de huevo contienen carbonato de calcio que ayuda a reducir la acidez del suelo y proporciona calcio esencial para el crecimiento de las plantas.",
                "need_resources": "¡Hola pequeño guardián!\n\nNecesitas recolectar todos los recursos necesarios para ayudar al árbol central:\n- Cáscara de plátano (composta)\n- Agua\n- Cáscara de huevo (semillas)\n\n¡Busca por el mapa y recógelos antes de que se acabe el tiempo!",
                "all_collected": "¡Felicidades! Has recolectado todos los recursos.\n\nAhora ve al árbol central y presiona 'E' para entregarlos y completar la misión.\n\n¡Rápido, el tiempo se acaba!"
            }
        else:  # Inglés
            self.dialog_texts = {
                "composta": "You have collected banana peel!\n\nBanana peels are rich in nutrients like potassium, phosphorus, and calcium, which help enrich the soil and promote plant growth.",
                "agua": "You have collected water!\n\nWater is essential for plant life. It helps transport nutrients from the roots to the leaves and keeps the plant hydrated and healthy.",
                "semillas": "You have collected egg shell!\n\nEgg shells contain calcium carbonate that helps reduce soil acidity and provides essential calcium for plant growth.",
                "need_resources": "Hello little guardian!\n\nYou need to collect all the necessary resources to help the central tree:\n- Banana peel (compost)\n- Water\n- Egg shell (seeds)\n\nSearch the map and collect them before time runs out!",
                "all_collected": "Congratulations! You have collected all resources.\n\nNow go to the central tree and press 'E' to deliver them and complete the mission.\n\nHurry, time is running out!"
            }

    def add_resource_dialog(self, resource_type):
        if resource_type in self.dialog_texts:
            self.dialogs.append(self.dialog_texts[resource_type])
            if not self.game_paused:
                self.game_paused = True
                self.dialog_timer = pygame.time.get_ticks()
                self.current_dialog_index = len(self.dialogs) - 1

    def add_tree_dialog(self, dialog_type):
        if dialog_type in self.dialog_texts:
            self.dialogs.append(self.dialog_texts[dialog_type])
            if not self.game_paused:
                self.game_paused = True
                self.dialog_timer = pygame.time.get_ticks()
                self.current_dialog_index = len(self.dialogs) - 1

    def next_dialog(self):
        self.current_dialog_index += 1
        self.dialog_timer = pygame.time.get_ticks()
        
        if self.current_dialog_index >= len(self.dialogs):
            self.dialogs = []
            self.current_dialog_index = 0
            self.game_paused = False

    def update(self, current_time):
        if self.game_paused and self.has_dialogs():
            if current_time - self.dialog_timer > self.dialog_duration:
                self.next_dialog()

    def get_current_dialog_text(self):
        if self.current_dialog_index < len(self.dialogs):
            return self.dialogs[self.current_dialog_index]
        return ""

    def has_dialogs(self):
        return len(self.dialogs) > 0