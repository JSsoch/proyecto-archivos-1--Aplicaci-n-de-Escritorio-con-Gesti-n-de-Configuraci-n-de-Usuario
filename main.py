import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from config_manager import ConfigManager
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Panel de Control - Fase 3")
        self.geometry("600x400")
        self.config_manager = ConfigManager()
        
        self.is_fullscreen = False
        
        self.create_menu()
        self.setup_ui()
        self.apply_config()

    def create_menu(self):
        menubar = tk.Menu(self)
        
        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Nuevo", command=lambda: messagebox.showinfo("Simulado", "Nuevo"))
        archivo_menu.add_command(label="Abrir", command=lambda: messagebox.showinfo("Simulado", "Abrir"))
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)

        edicion_menu = tk.Menu(menubar, tearoff=0)
        edicion_menu.add_command(label="Deshacer", command=lambda: messagebox.showinfo("Simulado", "Deshacer"))
        edicion_menu.add_command(label="Copiar", command=lambda: messagebox.showinfo("Simulado", "Copiar"))
        menubar.add_cascade(label="Edición", menu=edicion_menu)

        ver_menu = tk.Menu(menubar, tearoff=0)
        ver_menu.add_command(label="Minimizar", command=self.iconify)
        ver_menu.add_command(label="Maximizar", command=self.maximize_window)
        ver_menu.add_command(label="Restaurar Tamaño Normal", command=self.restore_window)
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

    def apply_config(self):
        cfg = self.config_manager.config
        bg_color = "#2E2E2E" if cfg["tema_interfaz"] == "oscuro" else "#F0F0F0"
        fg_color = cfg["color_letra"]
        font_size = int(cfg["tamaño_fuente"])
        
        self.main_frame.configure(bg=bg_color)
        self.lbl_welcome.configure(
            text=f"Hola, {cfg['nombre_usuario']}\nIdioma: {cfg['idioma']}",
            bg=bg_color,
            fg=fg_color,
            font=("Arial", font_size)
        )

    def open_settings(self):
        SettingsWindow(self, self.config_manager)

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, config_manager):
        super().__init__(parent)
        self.title("Ajustes Avanzados")
        self.geometry("450x400")
        self.parent = parent
        self.config_manager = config_manager
        self.cfg = self.config_manager.config.copy()
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self, padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nombre = tk.Entry(frame, width=30)
        self.entry_nombre.insert(0, self.cfg.get("nombre_usuario", ""))
        self.entry_nombre.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(frame, text="Tema:").grid(row=1, column=0, sticky="w", pady=5)
        self.tema_var = tk.StringVar(value=self.cfg.get("tema_interfaz", "claro"))
        ttk.Combobox(frame, textvariable=self.tema_var, values=["claro", "oscuro"]).grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(frame, text="Idioma:").grid(row=2, column=0, sticky="w", pady=5)
        self.idioma_var = tk.StringVar(value=self.cfg.get("idioma", "es/es-ES"))
        ttk.Combobox(frame, textvariable=self.idioma_var, values=["es/es-ES", "en/en-US"]).grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(frame, text="Tamaño fuente:").grid(row=3, column=0, sticky="w", pady=5)
        self.fuente_var = tk.IntVar(value=self.cfg.get("tamaño_fuente", 12))
        tk.Spinbox(frame, from_=8, to=48, textvariable=self.fuente_var).grid(row=3, column=1, sticky="w", pady=5)

        tk.Label(frame, text="Color menú:").grid(row=4, column=0, sticky="w", pady=5)
        self.color_menu_var = self.cfg.get("color_barra_menu", "#f0f0f0")
        self.btn_color_menu = tk.Button(frame, text="Elegir", bg=self.color_menu_var, command=self.pick_color_menu)
        self.btn_color_menu.grid(row=4, column=1, sticky="w", pady=5)

        tk.Label(frame, text="Color letra:").grid(row=5, column=0, sticky="w", pady=5)
        self.color_letra_var = self.cfg.get("color_letra", "#000000")
        self.btn_color_letra = tk.Button(frame, text="Elegir", bg=self.color_letra_var, command=self.pick_color_letra)
        self.btn_color_letra.grid(row=5, column=1, sticky="w", pady=5)

        tk.Label(frame, text="Avatar:").grid(row=6, column=0, sticky="w", pady=5)
        self.foto_path = self.cfg.get("foto_perfil", "")
        self.btn_foto = tk.Button(frame, text="Buscar", command=self.pick_foto)
        self.btn_foto.grid(row=6, column=1, sticky="w", pady=5)

        tk.Button(self, text="Guardar Cambios", command=self.save).pack(pady=20)

    def pick_color_menu(self):
        color = colorchooser.askcolor(initialcolor=self.color_menu_var)
        if color[1]:
            self.color_menu_var = color[1]
            self.btn_color_menu.config(bg=color[1])

    def pick_color_letra(self):
        color = colorchooser.askcolor(initialcolor=self.color_letra_var)
        if color[1]:
            self.color_letra_var = color[1]
            self.btn_color_letra.config(bg=color[1])

    def pick_foto(self):
        filepath = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg")])
        if filepath:
            self.foto_path = filepath

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
            messagebox.showerror("Error de Permisos", "No se pudo completar el guardado seguro. Verifique permisos del archivo.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
