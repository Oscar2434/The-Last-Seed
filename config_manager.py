import json
import os

CONFIG_FILE = "game_config.json"

def load_config():
    """Carga la configuración desde el archivo JSON"""
    default_config = {
        "lenguaje": True,  # True = Español, False = Inglés
        "music": True,
        "volume_master": 0.5,
        "selected_character": None,
        "difficulty": None
    }
    
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                # Actualizar solo las claves existentes en default_config
                for key in default_config:
                    if key in loaded_config:
                        default_config[key] = loaded_config[key]
    except Exception as e:
        print(f"Error cargando configuración: {e}")
    
    return default_config

def save_config(config_data):
    """Guarda la configuración en el archivo JSON"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error guardando configuración: {e}")
        return False