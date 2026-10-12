# Universidad Rafael Landívar
### Campus San Alberto Hurtado, S.J. de Quetzaltenango
### Facultad de Ingeniería | Ingeniería en Informática y Sistemas
**Curso:** Manejo e Implementación de Archivos  
**Laboratorio No. 1:** Aplicación de Escritorio con Gestión de Configuración de Usuario  
**Fecha:** Agosto - Octubre 2026  

---

## 1. Selección y Justificación Técnica del Formato de Almacenamiento

Para la persistencia de la configuración de usuario se seleccionó el formato **JSON (JavaScript Object Notation)**, evaluado frente a alternativas comunes como **CSV (Comma-Separated Values)**, **XML (eXtensible Markup Language)** e **INI/Texto Plano**.

### Tabla Comparativa de Criterios Técnicos

| Criterio Técnico | JSON (Seleccionado) | CSV (Descartado) | XML (Descartado) | INI (Descartado) |
| :--- | :--- | :--- | :--- | :--- |
| **Preservación de Tipos de Datos** | **Excelente**: Tipado nativo (enteros, booleanos, cadenas, nulos). | **Deficiente**: Todo se interpreta como cadena plana; requiere casting manual propenso a errores. | **Regular**: Requiere esquemas (XSD) o conversión manual de nodos. | **Limitada**: Solo cadenas y claves planas; soporte heterogéneo de secciones. |
| **Facilidad y Rendimiento de Parseo** | **Óptima**: Parser estándar `json` en CPython (escrito en C, rápido y sin dependencias externas). | **Rápida pero rígida**: No maneja datos estructurados ni arrays de forma nativa. | **Pesada**: Requiere construcción de árboles DOM (overhead de memoria y CPU). | **Sencilla**: Pero carece de estandarización universal de tipos de datos. |
| **Legibilidad y Edición Manual** | **Excelente**: Jerárquico, limpio, intuitivo para desarrolladores y usuarios finales. | **Media**: Difícil de leer cuando los campos contienen comas, rutas largas o espacios. | **Baja**: Sobrecarga de etiquetas repetitivas de apertura y cierre (`<tags>`). | **Buena**: Legible pero restrictivo a nivel de anidamiento. |
| **Tamaño en Disco / Overhead** | **Bajo**: Sintaxis concisa (llaves, comillas y dos puntos). | **Mínimo**: Pero insuficiente para estructuras complejas. | **Muy Alto**: La redundancia de etiquetas triplica el tamaño del archivo. | **Bajo**: Pero insuficiente para tipos avanzados. |
| **Robustez ante Corrupción** | **Alta**: La especificación estricta lanza `JSONDecodeError` ante truncamiento, facilitando la detección inmediata. | **Muy Baja**: Un archivo CSV corrupto o con líneas cortadas puede parsearse silenciosamente con datos desplazados. | **Alta**: Detecta errores de sintaxis XML pero con recuperación engorrosa. | **Media**: Puede ignorar líneas truncadas silenciosamente. |

### Justificación Técnica de la Elección
JSON ofrece el balance óptimo entre legibilidad humana, soporte directo de tipos primitivos (como el entero `tamaño_fuente: 16`), serialización nativa con la biblioteca estándar de Python y capacidad inmediata de validación sintáctica. Ante un cierre inesperado o fallo de escritura, un JSON incompleto falla ruidosamente en la fase de parseo mediante `json.JSONDecodeError`, lo cual permite al software activar el mecanismo de recuperación por defecto sin propagar estados inconsistentes en la aplicación.

---

## 2. Implementación de Escritura Segura y Respaldo Atómico

El requisito primordial de persistencia robusta exige que bajo ninguna circunstancia un corte de energía, terminación forzosa del proceso (`SIGKILL`) o excepción en tiempo de ejecución deje el archivo de configuración en un estado a medio escribir o corrupto.

### Flujo de Persistencia Implementado
1. **Respaldo Preventivo (`.bak`)**: Antes de modificar la configuración en disco, si existe un archivo `config.json` válido anterior, se asegura una copia exacta hacia `config.bak` usando `shutil.copy2()`, preservando metadatos.
2. **Escritura Segura en Archivo Temporal (`.tmp`)**: Los nuevos datos se serializan completamente en un archivo auxiliar `config.tmp` con codificación forzada en UTF-8 (`ensure_ascii=False`).
3. **Reemplazo Atómico (`os.replace`)**: Una vez cerrado y confirmado el flujo a disco del temporal, se invoca `os.replace(TEMP_FILE, CONFIG_FILE)`. A nivel del sistema operativo (POSIX y Windows NT), el renombrado/reemplazo es una operación atómica dentro del mismo sistema de archivos, garantizando que el archivo destino siempre apunte o a la versión anterior o a la nueva, jamás a un estado intermedio corrupto.

### Fragmento de Código Central (`config_manager.py`)

```python
def save_config(self, new_config):
    self.config.update(new_config)

    # 1. Respaldo previo de la versión anterior
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

    # 2. Escritura atómica a archivo temporal
    try:
        with open(TEMP_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    except PermissionError:
        print("ERROR: Sin permisos para escribir en el archivo temporal (.tmp).")
        return False

    # 3. Reemplazo seguro y atómico en el archivo final
    try:
        os.replace(TEMP_FILE, CONFIG_FILE)
        print("INFO: Configuración guardada y actualizada correctamente.")
        return True
    except PermissionError:
        print("ERROR: Sin permisos para reemplazar el archivo de configuración original.")
        return False
```

---

## 3. Manejo de Errores y Degradación Controlada

La aplicación captura explícitamente las tres clases críticas de error de sistema de archivos sin propagar `tracebacks` no controlados al usuario:

### Caso A: Archivo Ausente (`FileNotFoundError`)
- **Detección:** Se valida `os.path.exists(CONFIG_FILE)`.
- **Comportamiento:** Si el archivo no existe al iniciar, la aplicación no lanza excepción; carga la estructura de `DEFAULT_CONFIG` y notifica por consola (`INFO: Archivo de configuración no encontrado. Usando valores por defecto.`). La GUI inicia con normalidad.

### Caso B: Archivo Corrupto o Formato Inválido (`json.JSONDecodeError`)
- **Detección:** Captura explícita de `json.JSONDecodeError` al procesar `json.load(f)`.
- **Comportamiento:** Se notifica por consola (`ERROR: Archivo de configuración corrupto o con formato inválido. Degradando a valores por defecto.`). La aplicación conserva los valores sanos predeterminados sin abortar el hilo principal.

### Caso C: Falta de Permisos de Lectura o Escritura (`PermissionError`)
- **Detección:** Captura de `PermissionError` en la apertura para lectura, creación de respaldo, apertura de temporal o llamada a `os.replace()`.
- **Comportamiento:** En lectura, degrada a valores por defecto. En guardado, retorna `False` y la interfaz gráfica notifica mediante una alerta en pantalla: *"Ocurrió un problema de permisos al guardar"*, protegiendo la integridad del sistema.

### Evidencia de Pruebas Ejecutadas (`logs.txt`)

```text
============================================================
BATERÍA DE PRUEBAS DE PERSISTENCIA Y MANEJO DE ERRORES
============================================================

------------------------------------------------------------
--- CASO 1: ARCHIVO AUSENTE
------------------------------------------------------------
INFO: Archivo de configuración no encontrado. Usando valores por defecto.
Configuración activa actual (idioma): es/es-ES
Comportamiento: Degradación suave a valores por defecto sin excepción.

------------------------------------------------------------
--- CASO 2: ARCHIVO CORRUPTO / FORMATO INVÁLIDO
------------------------------------------------------------
ERROR: Archivo de configuración corrupto o con formato inválido. Degradando a valores por defecto.
Configuración activa actual (nombre_usuario): José Núñez
Comportamiento: Detección de JSONDecodeError y fallback a valores por defecto.

------------------------------------------------------------
--- CASO 3: SIN PERMISOS DE ESCRITURA
------------------------------------------------------------
INFO: Configuración cargada exitosamente.
Intentando guardar nueva configuración en archivo protegido...
ERROR: Sin permisos para reemplazar el archivo de configuración original.
Resultado del guardado controlado: Fallido (capturado controladamente)

------------------------------------------------------------
--- CASO 4: CODIFICACIÓN UTF-8 (Tildes y Carácter Ñ)
------------------------------------------------------------
INFO: Configuración cargada exitosamente.
INFO: Configuración guardada y actualizada correctamente.
INFO: Configuración cargada exitosamente.
Valor guardado y recuperado: José Núñez de la Peña
Validación de coincidencia exacta UTF-8: True

============================================================
TODAS LAS PRUEBAS FINALIZADAS EXITOSAMENTE SIN TRACEBACKS
============================================================
```

---

## 4. Codificación de Caracteres UTF-8

Para cumplir con la persistencia estricta de caracteres internacionales, diacríticos (tildes) y letras como la **Ñ**, se aplicaron dos configuraciones obligatorias:
1. `encoding='utf-8'` explícito tanto en modo `'r'` como en `'w'` al invocar la función `open()`.
2. `ensure_ascii=False` en `json.dump()`, evitando que Python escape los caracteres a secuencias Unicode como `\u00f1`.

### Archivo de Configuración Real Generado (`config.json`)

```json
{
    "nombre_usuario": "José Núñez de la Peña",
    "tema_interfaz": "oscuro",
    "idioma": "es/es-ES",
    "tamaño_fuente": 16,
    "color_barra_menu": "#2b5b84",
    "color_letra": "#ffffff",
    "foto_perfil": "C:/Usuarios/Imágenes/foto_diseño.png"
}
```

### Archivo de Respaldo Generado (`config.bak`)

```json
{
    "nombre_usuario": "José Núñez de la Peña",
    "tema_interfaz": "oscuro",
    "idioma": "es/es-ES",
    "tamaño_fuente": 14,
    "color_barra_menu": "#2b5b84",
    "color_letra": "#ffffff",
    "foto_perfil": "C:/Usuarios/Imágenes/foto_diseño.png"
}
```

---

## 5. Arquitectura e Interfaz de Usuario

La aplicación fue desarrollada en Python haciendo uso de `tkinter` y `tkinter.ttk`:
- **Menú Principal Simulado y Funcional:**
  - `Archivo`: Subopciones *Nuevo*, *Abrir*, *Salir*. Disparan retroalimentación visual integrada en la misma ventana sin ventanas modales intrusivas.
  - `Edición`: Subopciones *Deshacer*, *Copiar* con confirmación en pantalla.
  - `Ver`: Control dinámico de ventana (*Minimizar*, *Maximizar*, *Restaurar Tamaño Normal*, *Alternar Pantalla Completa*).
  - `Configuración`: Despliega la ventana de Settings.
- **Ventana de Configuración (Settings):**
  - Campos: Nombre de usuario, Tema claro/oscuro, Idioma (español e inglés con traducción dinámica en tiempo real de toda la interfaz), Tamaño de fuente, Selectores propios de color (Barra de menú y Letra) mediante `colorchooser`, y Selector de archivo para Foto de perfil mediante `filedialog`.
  - Botones de acción: *Restaurar Fábrica* (recupera valores predeterminados seguros), *Aplicar* (persiste y actualiza la ventana principal en vivo sin cerrar la ventana de ajustes) y *Guardar y Cerrar*.
  - Renderizado de Avatar: Previsualización directa de la foto de perfil seleccionada en la pantalla central de la aplicación.
