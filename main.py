import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from config_manager import ConfigManager
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Panel de Control Moderno")
        self.geometry("750x450")
        self.config_manager = ConfigManager()
        self.is_fullscreen = False
        
        self.style = ttk.Style(self)
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")
        
        self.create_menu()
        self.setup_ui()
        self.apply_config()

    def create_menu(self):
        menubar = tk.Menu(self, font=("Segoe UI", 10))
        
        archivo_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 10))
        archivo_menu.add_command(label="Nuevo", command=lambda: messagebox.showinfo("Simulado", "Acción: Nuevo"))
        archivo_menu.add_command(label="Abrir", command=lambda: messagebox.showinfo("Simulado", "Acción: Abrir"))
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)

        edicion_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 10))
        edicion_menu.add_command(label="Deshacer", command=lambda: messagebox.showinfo("Simulado", "Acción: Deshacer"))
        edicion_menu.add_command(label="Copiar", command=lambda: messagebox.showinfo("Simulado", "Acción: Copiar"))
        menubar.add_cascade(label="Edición", menu=edicion_menu)

        ver_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 10))
        ver_menu.add_command(label="Minimizar", command=self.iconify)
        ver_menu.add_command(label="Maximizar", command=self.maximize_window)
        ver_menu.add_command(label="Restaurar Tamaño", command=self.restore_window)
        ver_menu.add_separator()
        ver_menu.add_command(label="Pantalla Completa", command=self.toggle_fullscreen)
        menubar.add_cascade(label="Ver", menu=ver_menu)

        menubar.add_command(label="Configuración", command=self.open_settings)
        self.config(menu=menubar)

    def maximize_window(self):
        self.state('zoomed')
        
    def restore_window(self):
        self.state('normal')

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def setup_ui(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)
        
        self.lbl_welcome = tk.Label(self.main_frame, justify="center")
        self.lbl_welcome.pack(expand=True)
        
        self.status_bar = ttk.Label(self, text=" Sistema iniciado", relief="sunken", anchor="w", padding=2)
        self.status_bar.pack(side="bottom", fill="x")

    def apply_config(self):
        cfg = self.config_manager.config
        bg_color = "#1e1e1e" if cfg["tema_interfaz"] == "oscuro" else "#f7f7f7"
        fg_color = cfg["color_letra"]
        font_size = int(cfg["tamaño_fuente"])
        font_family = "Segoe UI"
        
        self.main_frame.configure(bg=bg_color)
        
        welcome_text = f"Hola, {cfg['nombre_usuario']}\nIdioma configurado: {cfg['idioma'].split('/')[0].upper()}"
        self.lbl_welcome.configure(
            text=welcome_text,
            bg=bg_color,
            fg=fg_color,
            font=(font_family, font_size, "bold")
        )
        
        self.status_bar.configure(text=f" Usuario actual: {cfg['nombre_usuario']}  |  Tema: {cfg['tema_interfaz'].capitalize()}  |  Estado: Archivo Seguro")

    def open_settings(self):
        SettingsWindow(self, self.config_manager)

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, config_manager):
        super().__init__(parent)
        self.title("Configuración Avanzada")
        self.geometry("450x550")
        self.resizable(False, False)
        self.parent = parent
        self.config_manager = config_manager
        self.cfg = self.config_manager.config.copy()
        
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style(self)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=4)
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

    def create_widgets(self):
        main_container = ttk.Frame(self, padding=25)
        main_container.pack(fill="both", expand=True)
        
        ttk.Label(main_container, text="Ajustes de Perfil", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        ttk.Label(main_container, text="Nombre:").grid(row=1, column=0, sticky="w", pady=8)
        self.entry_nombre = ttk.Entry(main_container, width=32, font=("Segoe UI", 10))
        self.entry_nombre.insert(0, self.cfg.get("nombre_usuario", ""))
        self.entry_nombre.grid(row=1, column=1, sticky="w", pady=8)

        ttk.Label(main_container, text="Tema:").grid(row=2, column=0, sticky="w", pady=8)
        self.tema_var = tk.StringVar(value=self.cfg.get("tema_interfaz", "claro"))
        ttk.Combobox(main_container, textvariable=self.tema_var, values=["claro", "oscuro"], state="readonly", width=30, font=("Segoe UI", 10)).grid(row=2, column=1, sticky="w", pady=8)

        ttk.Label(main_container, text="Idioma:").grid(row=3, column=0, sticky="w", pady=8)
        self.idioma_var = tk.StringVar(value=self.cfg.get("idioma", "es/es-ES"))
        ttk.Combobox(main_container, textvariable=self.idioma_var, values=["es/es-ES", "en/en-US"], state="readonly", width=30, font=("Segoe UI", 10)).grid(row=3, column=1, sticky="w", pady=8)

        ttk.Label(main_container, text="Tamaño fuente:").grid(row=4, column=0, sticky="w", pady=8)
        self.fuente_var = tk.IntVar(value=self.cfg.get("tamaño_fuente", 12))
        ttk.Spinbox(main_container, from_=8, to=48, textvariable=self.fuente_var, width=30, font=("Segoe UI", 10)).grid(row=4, column=1, sticky="w", pady=8)

        ttk.Label(main_container, text="Color menú:").grid(row=5, column=0, sticky="w", pady=8)
        self.color_menu_var = self.cfg.get("color_barra_menu", "#f0f0f0")
        self.btn_color_menu = tk.Button(main_container, text="■", bg=self.color_menu_var, fg=self.color_menu_var, font=("Segoe UI", 10), command=self.pick_color_menu, width=5, relief="flat", cursor="hand2")
        self.btn_color_menu.grid(row=5, column=1, sticky="w", pady=8)

        ttk.Label(main_container, text="Color letra:").grid(row=6, column=0, sticky="w", pady=8)
        self.color_letra_var = self.cfg.get("color_letra", "#000000")
        self.btn_color_letra = tk.Button(main_container, text="■", bg=self.color_letra_var, fg=self.color_letra_var, font=("Segoe UI", 10), command=self.pick_color_letra, width=5, relief="flat", cursor="hand2")
        self.btn_color_letra.grid(row=6, column=1, sticky="w", pady=8)

        ttk.Label(main_container, text="Avatar:").grid(row=7, column=0, sticky="w", pady=8)
        self.foto_path = self.cfg.get("foto_perfil", "")
        
        foto_frame = ttk.Frame(main_container)
        foto_frame.grid(row=7, column=1, sticky="w", pady=8)
        
        ttk.Button(foto_frame, text="Examinar", command=self.pick_foto).pack(side="left")
        self.lbl_foto = ttk.Label(foto_frame, text=os.path.basename(self.foto_path) if self.foto_path else "Ninguno", font=("Segoe UI", 9, "italic"))
        self.lbl_foto.pack(side="left", padx=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=10, padx=25)
        
        ttk.Button(btn_frame, text="Restaurar Fábrica", command=self.restore).pack(side="left")
        ttk.Button(btn_frame, text="Guardar Cambios", command=self.save).pack(side="right")

    def pick_color_menu(self):
        color = colorchooser.askcolor(initialcolor=self.color_menu_var)
        if color[1]:
            self.color_menu_var = color[1]
            self.btn_color_menu.config(bg=color[1], fg=color[1])

    def pick_color_letra(self):
        color = colorchooser.askcolor(initialcolor=self.color_letra_var)
        if color[1]:
            self.color_letra_var = color[1]
            self.btn_color_letra.config(bg=color[1], fg=color[1])

    def pick_foto(self):
        filepath = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if filepath:
            self.foto_path = filepath
            self.lbl_foto.config(text=os.path.basename(self.foto_path))

    def restore(self):
        if messagebox.askyesno("Confirmar", "¿Restaurar todos los valores de fábrica?"):
            self.config_manager.restore_defaults()
            self.parent.apply_config()
            self.destroy()

    def save(self):
        new_config = {
            "nombre_usuario": self.entry_nombre.get(),
            "tema_interfaz": self.tema_var.get(),
            "idioma": self.idioma_var.get(),
            "tamaño_fuente": self.fuente_var.get(),
            "color_barra_menu": self.color_menu_var,
            "color_letra": self.color_letra_var,
            "foto_perfil": self.foto_path
        }
        
        if self.config_manager.save_config(new_config):
            self.parent.apply_config()
            self.destroy()
        else:
            messagebox.showerror("Error", "Ocurrió un problema de permisos al guardar.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
