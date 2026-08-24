import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "nombre_usuario": "Usuario",
    "tema_interfaz": "claro",
    "idioma": "es/es-ES",
    "tamaño_fuente": 12,
    "color_barra_menu": "#f0f0f0",
    "color_letra": "#000000",
    "foto_perfil": ""
}

class ConfigManager:
    def __init__(self):
        self.config = DEFAULT_CONFIG.copy()
        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    self.config.update(json.load(f))
            except Exception:
                pass

    def save_config(self, new_config):
        self.config.update(new_config)
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception:
            return False
