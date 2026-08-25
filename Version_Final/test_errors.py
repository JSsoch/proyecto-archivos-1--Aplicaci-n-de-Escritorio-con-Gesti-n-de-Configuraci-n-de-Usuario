import os
import time
from config_manager import ConfigManager, CONFIG_FILE

def print_separator(title):
    print(f"\n{'-'*50}\n--- {title}\n{'-'*50}")

def test_missing_file():
    print_separator("CASO 1: ARCHIVO AUSENTE")
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    
    cm = ConfigManager()
    print("Configuración activa actual (idioma):", cm.config["idioma"])

def test_corrupted_file():
    print_separator("CASO 2: ARCHIVO CORRUPTO")
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        f.write('{ "nombre_usuario": "Carlos", "tema_interfaz": ') 
    
    cm = ConfigManager()
    print("Configuración activa actual (nombre_usuario):", cm.config["nombre_usuario"])

def test_permission_error():
    print_separator("CASO 3: SIN PERMISOS (Lectura/Escritura)")
    # Crear un archivo JSON válido
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        f.write('{"nombre_usuario": "Bloqueado"}')
    
    import stat
    # Quitar permisos de escritura
    os.chmod(CONFIG_FILE, stat.S_IREAD)
    
    cm = ConfigManager()
    print("Intentando guardar nueva configuración en archivo de solo lectura...")
    success = cm.save_config({"nombre_usuario": "Nuevo"})
    print(f"Resultado del guardado: {'Éxito' if success else 'Fallido'}")
    
    # Restaurar permisos para que no fastidie después
    os.chmod(CONFIG_FILE, stat.S_IWRITE | stat.S_IREAD)

if __name__ == "__main__":
    print("INICIANDO BATERÍA DE PRUEBAS DE ERRORES\n")
    test_missing_file()
    time.sleep(1)
    test_corrupted_file()
    time.sleep(1)
    test_permission_error()
    print("\nPRUEBAS FINALIZADAS.")
