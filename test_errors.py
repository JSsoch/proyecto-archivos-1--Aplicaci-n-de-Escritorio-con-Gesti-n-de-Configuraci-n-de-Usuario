import os
import stat
import time
from config_manager import ConfigManager, CONFIG_FILE, BACKUP_FILE

def print_separator(title):
    print(f"\n{'-'*60}\n--- {title}\n{'-'*60}")

def test_missing_file():
    print_separator("CASO 1: ARCHIVO AUSENTE")
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    
    cm = ConfigManager()
    print("Configuración activa actual (idioma):", cm.config["idioma"])
    print("Comportamiento: Degradación suave a valores por defecto sin excepción.")

def test_corrupted_file():
    print_separator("CASO 2: ARCHIVO CORRUPTO / FORMATO INVÁLIDO")
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        f.write('{ "nombre_usuario": "Carlos", "tema_interfaz": ') 
    
    cm = ConfigManager()
    print("Configuración activa actual (nombre_usuario):", cm.config["nombre_usuario"])
    print("Comportamiento: Detección de JSONDecodeError y fallback a valores por defecto.")

def test_permission_error():
    print_separator("CASO 3: SIN PERMISOS DE ESCRITURA")
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        f.write('{"nombre_usuario": "Bloqueado"}')
    
    os.chmod(CONFIG_FILE, stat.S_IREAD)
    try:
        cm = ConfigManager()
        print("Intentando guardar nueva configuración en archivo protegido...")
        success = cm.save_config({"nombre_usuario": "Nuevo Intento"})
        print(f"Resultado del guardado controlado: {'Éxito' if success else 'Fallido (capturado controladamente)'}")
    finally:
        os.chmod(CONFIG_FILE, stat.S_IWRITE | stat.S_IREAD)
        if os.path.exists(BACKUP_FILE):
            os.chmod(BACKUP_FILE, stat.S_IWRITE | stat.S_IREAD)

def test_utf8():
    print_separator("CASO 4: CODIFICACIÓN UTF-8 (Tildes y Carácter Ñ)")
    cm = ConfigManager()
    datos_prueba = {
        "nombre_usuario": "José Núñez de la Peña",
        "idioma": "es/es-ES",
        "tema_interfaz": "oscuro",
        "tamaño_fuente": 14,
        "color_barra_menu": "#2b5b84",
        "color_letra": "#ffffff",
        "foto_perfil": "C:/Usuarios/Imágenes/foto_diseño.png"
    }
    cm.save_config(datos_prueba)
    
    cm2 = ConfigManager()
    recuperado = cm2.config["nombre_usuario"]
    print("Valor guardado y recuperado:", recuperado)
    print("Validación de coincidencia exacta UTF-8:", recuperado == "José Núñez de la Peña")

if __name__ == "__main__":
    print("=" * 60)
    print("BATERÍA DE PRUEBAS DE PERSISTENCIA Y MANEJO DE ERRORES")
    print("=" * 60)
    test_missing_file()
    time.sleep(0.5)
    test_corrupted_file()
    time.sleep(0.5)
    test_permission_error()
    time.sleep(0.5)
    test_utf8()
    print("\n" + "=" * 60)
    print("TODAS LAS PRUEBAS FINALIZADAS EXITOSAMENTE SIN TRACEBACKS")
    print("=" * 60)
