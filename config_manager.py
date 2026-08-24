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
        # Carga básica sin manejo de errores ni validaciones
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                self.config.update(loaded_config)
                print("Configuración cargada (Versión Inicial).")

    def save_config(self, new_config):
        # Guardado directo (sin archivo temporal, sin backups)
        self.config.update(new_config)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4)
        print("Configuración guardada (Versión Inicial).")
        return True
