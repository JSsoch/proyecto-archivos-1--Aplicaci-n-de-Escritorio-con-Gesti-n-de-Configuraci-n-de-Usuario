import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from config_manager import ConfigManager
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("App Gestión de Configuración (Lab 1)")
        self.geometry("600x400")
        
        # Inicializa configuración
        self.config_manager = ConfigManager()

        self.create_menu()
        self.apply_config()

    def create_menu(self):
        menubar = tk.Menu(self)

        # Archivo (simulado)
        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Nuevo", command=lambda: messagebox.showinfo("Simulado", "Acción de Archivo > Nuevo simulada."))
        archivo_menu.add_command(label="Abrir", command=lambda: messagebox.showinfo("Simulado", "Acción de Archivo > Abrir simulada."))
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)

        # Edición (simulado)
        edicion_menu = tk.Menu(menubar, tearoff=0)
        edicion_menu.add_command(label="Deshacer", command=lambda: messagebox.showinfo("Simulado", "Acción de Edición > Deshacer simulada."))
        edicion_menu.add_command(label="Copiar", command=lambda: messagebox.showinfo("Simulado", "Acción de Edición > Copiar simulada."))
        menubar.add_cascade(label="Edición", menu=edicion_menu)

        # Ver (simulado)
        ver_menu = tk.Menu(menubar, tearoff=0)
        ver_menu.add_command(label="Zoom In", command=lambda: messagebox.showinfo("Simulado", "Acción de Ver > Zoom In simulada."))
        menubar.add_cascade(label="Ver", menu=ver_menu)

        # Settings (funcional)
        menubar.add_command(label="Settings", command=self.open_settings)

        self.config(menu=menubar)

    def apply_config(self):
        """Aplica la configuración visualmente a la ventana principal."""
        cfg = self.config_manager.config
        
        # Tema de interfaz (fondo)
        bg_color = "#2E2E2E" if cfg["tema_interfaz"] == "oscuro" else "#F0F0F0"
        self.configure(bg=bg_color)
        
        # Limpiar widgets previos (si los hay)
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()
        
        fg_color = cfg["color_letra"]
        font_size = int(cfg["tamaño_fuente"])
        
        welcome_text = f"¡Bienvenido, {cfg['nombre_usuario']}!\nIdioma configurado: {cfg['idioma']}"
        lbl = tk.Label(self, text=welcome_text, bg=bg_color, fg=fg_color, font=("Arial", font_size))
        lbl.pack(expand=True)
        
        # Nota: El color de la barra de menú en Windows/Tkinter puro es manejado por el SO
        # pero guardamos el dato como exige el laboratorio.

    def open_settings(self):
        SettingsWindow(self, self.config_manager)

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, config_manager):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("450x450")
        self.resizable(False, False)
        
        self.parent = parent
        self.config_manager = config_manager
        
        # Hacemos una copia local de la configuración para editar
        self.cfg = self.config_manager.config.copy()
        
        self.create_widgets()

    def create_widgets(self):
        pad_options = {'padx': 10, 'pady': 5, 'anchor': 'w'}
        
        # Contenedor para hacer el layout más limpio
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)

        # 1. Nombre de usuario
        ttk.Label(frame, text="Nombre de usuario:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nombre = ttk.Entry(frame, width=30)
        self.entry_nombre.insert(0, self.cfg.get("nombre_usuario", ""))
        self.entry_nombre.grid(row=0, column=1, sticky="w", pady=5)

        # 2. Tema interfaz
        ttk.Label(frame, text="Tema de interfaz:").grid(row=1, column=0, sticky="w", pady=5)
        self.tema_var = tk.StringVar(value=self.cfg.get("tema_interfaz", "claro"))
        ttk.Combobox(frame, textvariable=self.tema_var, values=["claro", "oscuro"], state="readonly", width=27).grid(row=1, column=1, sticky="w", pady=5)

        # 3. Idioma
        ttk.Label(frame, text="Idioma:").grid(row=2, column=0, sticky="w", pady=5)
        self.idioma_var = tk.StringVar(value=self.cfg.get("idioma", "es/es-ES"))
        ttk.Combobox(frame, textvariable=self.idioma_var, values=["es/es-ES", "en/en-US"], state="readonly", width=27).grid(row=2, column=1, sticky="w", pady=5)

        # 4. Tamaño de fuente
        ttk.Label(frame, text="Tamaño de fuente:").grid(row=3, column=0, sticky="w", pady=5)
        self.fuente_var = tk.IntVar(value=self.cfg.get("tamaño_fuente", 12))
        ttk.Spinbox(frame, from_=8, to=48, textvariable=self.fuente_var, width=28).grid(row=3, column=1, sticky="w", pady=5)

        # 5. Color de la barra de menú
        ttk.Label(frame, text="Color barra de menú:").grid(row=4, column=0, sticky="w", pady=5)
        self.color_menu_var = self.cfg.get("color_barra_menu", "#f0f0f0")
        self.btn_color_menu = tk.Button(frame, text="Elegir Color", bg=self.color_menu_var, command=self.pick_color_menu, width=15)
        self.btn_color_menu.grid(row=4, column=1, sticky="w", pady=5)

        # 6. Color de letra
        ttk.Label(frame, text="Color de letra:").grid(row=5, column=0, sticky="w", pady=5)
        self.color_letra_var = self.cfg.get("color_letra", "#000000")
        self.btn_color_letra = tk.Button(frame, text="Elegir Color", bg=self.color_letra_var, fg="#ffffff" if self.color_letra_var=="#000000" else "#000000", command=self.pick_color_letra, width=15)
        self.btn_color_letra.grid(row=5, column=1, sticky="w", pady=5)

        # 7. Foto de perfil
        ttk.Label(frame, text="Foto de perfil:").grid(row=6, column=0, sticky="w", pady=5)
        self.foto_path = self.cfg.get("foto_perfil", "")
        self.btn_foto = ttk.Button(frame, text="Seleccionar Archivo", command=self.pick_foto)
        self.btn_foto.grid(row=6, column=1, sticky="w", pady=5)
        
        # Mostrar nombre del archivo corto
        foto_name = os.path.basename(self.foto_path) if self.foto_path else "Ninguna"
        self.lbl_foto = ttk.Label(frame, text=foto_name)
        self.lbl_foto.grid(row=7, column=1, sticky="w")

        # Botón Guardar
        btn_save = ttk.Button(self, text="Guardar Configuración", command=self.save)
        btn_save.pack(pady=20)

    def pick_color_menu(self):
        color = colorchooser.askcolor(title="Elige color de la barra de menú", initialcolor=self.color_menu_var)
        if color[1]:
            self.color_menu_var = color[1]
            self.btn_color_menu.config(bg=self.color_menu_var)

    def pick_color_letra(self):
        color = colorchooser.askcolor(title="Elige color de letra", initialcolor=self.color_letra_var)
        if color[1]:
            self.color_letra_var = color[1]
            self.btn_color_letra.config(bg=self.color_letra_var)

    def pick_foto(self):
        filepath = filedialog.askopenfilename(
            title="Seleccionar Foto de Perfil", 
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")]
        )
        if filepath:
            self.foto_path = filepath
            self.lbl_foto.config(text=os.path.basename(self.foto_path))

    def save(self):
        # Recopilamos valores
        new_config = {
            "nombre_usuario": self.entry_nombre.get(),
            "tema_interfaz": self.tema_var.get(),
            "idioma": self.idioma_var.get(),
            "tamaño_fuente": self.fuente_var.get(),
            "color_barra_menu": self.color_menu_var,
            "color_letra": self.color_letra_var,
            "foto_perfil": self.foto_path
        }
        
        # Intentamos guardar
        success = self.config_manager.save_config(new_config)
        
        if success:
            messagebox.showinfo("Éxito", "Configuración guardada correctamente.\nSe generó un respaldo seguro.")
            self.parent.apply_config()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar la configuración. Ver consola para detalles.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
