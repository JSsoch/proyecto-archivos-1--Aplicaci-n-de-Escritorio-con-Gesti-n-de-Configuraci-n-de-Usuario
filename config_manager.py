import json
import os
import shutil
import stat

CONFIG_FILE = "config.json"
BACKUP_FILE = "config.bak"
TEMP_FILE = "config.tmp"

DEFAULT_CONFIG = {
    "nombre_usuario": "José Núñez",
    "tema_interfaz": "claro",
    "idioma": "es/es-ES",
    "tamaño_fuente": 14,
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
            print("INFO: Archivo de configuración no encontrado. Usando valores por defecto.")
            return

        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                self.config.update(loaded_config)
            print("INFO: Configuración cargada exitosamente.")
        except json.JSONDecodeError:
            print("ERROR: Archivo de configuración corrupto o con formato inválido. Degradando a valores por defecto.")
        except PermissionError:
            print("ERROR: Falta de permisos de lectura para el archivo de configuración. Degradando a valores por defecto.")
        except Exception as e:
            print(f"ERROR: Fallo inesperado al leer la configuración: {e}")

    def save_config(self, new_config):
        self.config.update(new_config)

        if os.path.exists(CONFIG_FILE):
            if os.path.exists(BACKUP_FILE):
                try:
                    os.chmod(BACKUP_FILE, stat.S_IWRITE)
                except Exception:
                    pass
            try:
                shutil.copy2(CONFIG_FILE, BACKUP_FILE)
            except PermissionError:
                print("ERROR: Sin permisos para crear el archivo de respaldo (.bak).")
                return False
            except Exception as e:
                print(f"ERROR: Fallo al crear el respaldo: {e}")
                return False

        try:
            with open(TEMP_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except PermissionError:
            print("ERROR: Sin permisos para escribir en el archivo temporal (.tmp).")
            return False
        except Exception as e:
            print(f"ERROR: Fallo al escribir el archivo temporal: {e}")
            return False

        try:
            os.replace(TEMP_FILE, CONFIG_FILE)
            print("INFO: Configuración guardada y actualizada correctamente.")
            return True
        except PermissionError:
            print("ERROR: Sin permisos para reemplazar el archivo de configuración original.")
            return False
        except Exception as e:
            print(f"ERROR: Fallo al reemplazar el archivo original: {e}")
            return False

    def restore_defaults(self):
        self.config = DEFAULT_CONFIG.copy()
        return self.save_config(self.config)
