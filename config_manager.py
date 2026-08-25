import json
import os
import shutil

CONFIG_FILE = "config.json"
BACKUP_FILE = "config.bak"
TEMP_FILE = "config.tmp"

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
        if not os.path.exists(CONFIG_FILE):
            return
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                self.config.update(json.load(f))
        except (json.JSONDecodeError, PermissionError):
            pass

    def save_config(self, new_config):
        self.config.update(new_config)
        if os.path.exists(CONFIG_FILE):
            try:
                shutil.copy2(CONFIG_FILE, BACKUP_FILE)
            except PermissionError:
                return False
        try:
            with open(TEMP_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except PermissionError:
            return False
        try:
            os.replace(TEMP_FILE, CONFIG_FILE)
            return True
        except PermissionError:
            return False

    def restore_defaults(self):
        self.config = DEFAULT_CONFIG.copy()
        return self.save_config(self.config)
