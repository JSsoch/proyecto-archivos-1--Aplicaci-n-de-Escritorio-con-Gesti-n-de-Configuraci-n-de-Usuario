import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from config_manager import ConfigManager
import os

TRANSLATIONS = {
    "es/es-ES": {
        "file": "Archivo", "new": "Nuevo", "open": "Abrir", "exit": "Salir",
        "edit": "Edición", "undo": "Deshacer", "copy": "Copiar",
        "view": "Ver", "minimize": "Minimizar", "maximize": "Maximizar", "restore_win": "Restaurar Tamaño", "fullscreen": "Pantalla Completa",
        "settings": "Configuración",
        "simulated": "Ejecutando acción simulada:",
        "welcome": "Hola",
        "lang_config": "Idioma configurado",
        "status_user": "Usuario actual",
        "status_theme": "Tema",
        "status_state": "Estado: Archivo Seguro",
        "set_title": "Configuración Avanzada",
        "set_header": "Ajustes de Perfil",
        "set_name": "Nombre:",
        "set_theme": "Tema:",
        "set_lang": "Idioma:",
        "set_font": "Tamaño fuente:",
        "set_menu_color": "Color menú:",
        "set_font_color": "Color letra:",
        "set_avatar": "Avatar:",
        "btn_browse": "Examinar",
        "btn_none": "Sin Foto",
        "btn_restore": "Restaurar Fábrica",
        "btn_apply": "Aplicar",
        "btn_save": "Guardar y Cerrar",
        "msg_restore": "¿Restaurar todos los valores de fábrica?"
    },
    "en/en-US": {
        "file": "File", "new": "New", "open": "Open", "exit": "Exit",
        "edit": "Edit", "undo": "Undo", "copy": "Copy",
        "view": "View", "minimize": "Minimize", "maximize": "Maximize", "restore_win": "Restore Size", "fullscreen": "Fullscreen",
        "settings": "Settings",
        "simulated": "Executing simulated action:",
        "welcome": "Hello",
        "lang_config": "Configured language",
        "status_user": "Current user",
        "status_theme": "Theme",
        "status_state": "State: Safe File",
        "set_title": "Advanced Settings",
        "set_header": "Profile Settings",
        "set_name": "Name:",
        "set_theme": "Theme:",
        "set_lang": "Language:",
        "set_font": "Font Size:",
        "set_menu_color": "Menu Color:",
        "set_font_color": "Font Color:",
        "set_avatar": "Avatar:",
        "btn_browse": "Browse",
        "btn_none": "No Photo",
        "btn_restore": "Factory Reset",
        "btn_apply": "Apply",
        "btn_save": "Save & Close",
        "msg_restore": "Restore all factory defaults?"
    }
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Panel de Control Moderno")
        self.geometry("750x550")
        self.config_manager = ConfigManager()
        self.is_fullscreen = False
        self._avatar_img = None  # Referencia para que la imagen no sea borrada por el garbage collector
        
        self.style = ttk.Style(self)
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")
        
        self.setup_ui()
        self.apply_config()

    def get_text(self, key):
        lang = self.config_manager.config.get("idioma", "es/es-ES")
        return TRANSLATIONS.get(lang, TRANSLATIONS["es/es-ES"]).get(key, key)

    def load_avatar(self, filepath, max_size=120):
        if not filepath or not os.path.exists(filepath):
            return None
        
        try:
            # Intenta usar Pillow (PIL) si está instalado para soportar JPG y redimensionar suavemente
            from PIL import Image, ImageTk
            img = Image.open(filepath)
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except ImportError:
            # Fallback a Tkinter nativo (Soporta PNG nativamente, no requiere librerías extra)
            try:
                img = tk.PhotoImage(file=filepath)
                # Redimensionado rústico (solo enteros) para que no ocupe toda la pantalla
                w, h = img.width(), img.height()
                factor = max(w, h) // max_size
                if factor > 1:
                    img = img.subsample(factor, factor)
                return img
            except Exception as e:
                print(f"Error cargando imagen nativa (asegúrese de que sea PNG): {e}")
                return None
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            return None

    def simulate_action(self, action_name):
        text = f"{self.get_text('simulated')} {action_name}"
        self.lbl_action.config(text=text, fg="#0078D7")
        self.after(3000, lambda: self.lbl_action.config(text=""))

    def build_menu(self):
        if self.winfo_children():
            for widget in self.winfo_children():
                if isinstance(widget, tk.Menu):
                    widget.destroy()

        menubar = tk.Menu(self, font=("Segoe UI", 10))
        
        archivo_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 10))
        archivo_menu.add_command(label=self.get_text("new"), command=lambda: self.simulate_action(self.get_text("new")))
        archivo_menu.add_command(label=self.get_text("open"), command=lambda: self.simulate_action(self.get_text("open")))
        archivo_menu.add_separator()
        archivo_menu.add_command(label=self.get_text("exit"), command=self.quit)
        menubar.add_cascade(label=self.get_text("file"), menu=archivo_menu)

        edicion_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 10))
        edicion_menu.add_command(label=self.get_text("undo"), command=lambda: self.simulate_action(self.get_text("undo")))
        edicion_menu.add_command(label=self.get_text("copy"), command=lambda: self.simulate_action(self.get_text("copy")))
        menubar.add_cascade(label=self.get_text("edit"), menu=edicion_menu)

        ver_menu = tk.Menu(menubar, tearoff=0, font=("Segoe UI", 10))
        ver_menu.add_command(label=self.get_text("minimize"), command=self.iconify)
        ver_menu.add_command(label=self.get_text("maximize"), command=self.maximize_window)
        ver_menu.add_command(label=self.get_text("restore_win"), command=self.restore_window)
        ver_menu.add_separator()
        ver_menu.add_command(label=self.get_text("fullscreen"), command=self.toggle_fullscreen)
        menubar.add_cascade(label=self.get_text("view"), menu=ver_menu)

        menubar.add_command(label=self.get_text("settings"), command=self.open_settings)
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
        
        # Frame central para mantener todo alineado
        self.center_frame = tk.Frame(self.main_frame)
        self.center_frame.pack(expand=True)
        
        self.lbl_avatar = tk.Label(self.center_frame, justify="center")
        self.lbl_avatar.pack(pady=(0, 15))

        self.lbl_welcome = tk.Label(self.center_frame, justify="center")
        self.lbl_welcome.pack()
        
        self.lbl_action = tk.Label(self.main_frame, font=("Segoe UI", 12, "italic"))
        self.lbl_action.pack(fill="x", pady=20)
        
        self.status_bar = ttk.Label(self, relief="sunken", anchor="w", padding=2)
        self.status_bar.pack(side="bottom", fill="x")

    def apply_config(self):
        self.build_menu()
        
        cfg = self.config_manager.config
        bg_color = "#1e1e1e" if cfg["tema_interfaz"] == "oscuro" else "#f7f7f7"
        fg_color = cfg["color_letra"]
        font_size = int(cfg["tamaño_fuente"])
        font_family = "Segoe UI"
        
        self.main_frame.configure(bg=bg_color)
        self.center_frame.configure(bg=bg_color)
        self.lbl_action.configure(bg=bg_color)
        
        # Actualizar Foto de Perfil
        self._avatar_img = self.load_avatar(cfg.get("foto_perfil", ""), max_size=120)
        if self._avatar_img:
            self.lbl_avatar.configure(image=self._avatar_img, text="", bg=bg_color)
        else:
            self.lbl_avatar.configure(image="", text=f"[ {self.get_text('btn_none')} ]", bg=bg_color, fg=fg_color, font=(font_family, 12, "italic"))
        
        welcome_text = f"{self.get_text('welcome')}, {cfg['nombre_usuario']}\n{self.get_text('lang_config')}: {cfg['idioma'].split('/')[0].upper()}"
        self.lbl_welcome.configure(
            text=welcome_text,
            bg=bg_color,
            fg=fg_color,
            font=(font_family, font_size, "bold")
        )
        
        status_text = f" {self.get_text('status_user')}: {cfg['nombre_usuario']}  |  {self.get_text('status_theme')}: {cfg['tema_interfaz'].capitalize()}  |  {self.get_text('status_state')}"
        self.status_bar.configure(text=status_text)

    def open_settings(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.lift()
                return
        SettingsWindow(self, self.config_manager)

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, config_manager):
        super().__init__(parent)
        self.parent = parent
        self.config_manager = config_manager
        self.cfg = self.config_manager.config.copy()
        
        self.title(self.parent.get_text("set_title"))
        self.geometry("480x600")
        self.resizable(False, False)
        
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style(self)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=4)
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

    def create_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        main_container = ttk.Frame(self, padding=25)
        main_container.pack(fill="both", expand=True)
        
        ttk.Label(main_container, text=self.parent.get_text("set_header"), style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))

        ttk.Label(main_container, text=self.parent.get_text("set_name")).grid(row=1, column=0, sticky="w", pady=8)
        self.entry_nombre = ttk.Entry(main_container, width=32, font=("Segoe UI", 10))
        self.entry_nombre.insert(0, self.cfg.get("nombre_usuario", ""))
        self.entry_nombre.grid(row=1, column=1, sticky="w", pady=8)

        ttk.Label(main_container, text=self.parent.get_text("set_theme")).grid(row=2, column=0, sticky="w", pady=8)
        self.tema_var = tk.StringVar(value=self.cfg.get("tema_interfaz", "claro"))
        ttk.Combobox(main_container, textvariable=self.tema_var, values=["claro", "oscuro"], state="readonly", width=30, font=("Segoe UI", 10)).grid(row=2, column=1, sticky="w", pady=8)

        ttk.Label(main_container, text=self.parent.get_text("set_lang")).grid(row=3, column=0, sticky="w", pady=8)
        self.idioma_var = tk.StringVar(value=self.cfg.get("idioma", "es/es-ES"))
        ttk.Combobox(main_container, textvariable=self.idioma_var, values=["es/es-ES", "en/en-US"], state="readonly", width=30, font=("Segoe UI", 10)).grid(row=3, column=1, sticky="w", pady=8)

        ttk.Label(main_container, text=self.parent.get_text("set_font")).grid(row=4, column=0, sticky="w", pady=8)
        self.fuente_var = tk.IntVar(value=self.cfg.get("tamaño_fuente", 12))
        ttk.Spinbox(main_container, from_=8, to=48, textvariable=self.fuente_var, width=30, font=("Segoe UI", 10)).grid(row=4, column=1, sticky="w", pady=8)

        ttk.Label(main_container, text=self.parent.get_text("set_menu_color")).grid(row=5, column=0, sticky="w", pady=8)
        self.color_menu_var = self.cfg.get("color_barra_menu", "#f0f0f0")
        self.btn_color_menu = tk.Button(main_container, text="■", bg=self.color_menu_var, fg=self.color_menu_var, font=("Segoe UI", 10), command=self.pick_color_menu, width=5, relief="flat", cursor="hand2")
        self.btn_color_menu.grid(row=5, column=1, sticky="w", pady=8)

        ttk.Label(main_container, text=self.parent.get_text("set_font_color")).grid(row=6, column=0, sticky="w", pady=8)
        self.color_letra_var = self.cfg.get("color_letra", "#000000")
        self.btn_color_letra = tk.Button(main_container, text="■", bg=self.color_letra_var, fg=self.color_letra_var, font=("Segoe UI", 10), command=self.pick_color_letra, width=5, relief="flat", cursor="hand2")
        self.btn_color_letra.grid(row=6, column=1, sticky="w", pady=8)

        ttk.Label(main_container, text=self.parent.get_text("set_avatar")).grid(row=7, column=0, sticky="w", pady=8)
        self.foto_path = self.cfg.get("foto_perfil", "")
        
        foto_frame = ttk.Frame(main_container)
        foto_frame.grid(row=7, column=1, sticky="w", pady=8)
        
        ttk.Button(foto_frame, text=self.parent.get_text("btn_browse"), command=self.pick_foto).pack(side="left")
        self.lbl_foto = ttk.Label(foto_frame, text=os.path.basename(self.foto_path) if self.foto_path else self.parent.get_text("btn_none"), font=("Segoe UI", 9, "italic"))
        self.lbl_foto.pack(side="left", padx=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=10, padx=25)
        
        ttk.Button(btn_frame, text=self.parent.get_text("btn_restore"), command=self.restore).pack(side="left")
        
        right_btns = ttk.Frame(btn_frame)
        right_btns.pack(side="right")
        
        ttk.Button(right_btns, text=self.parent.get_text("btn_apply"), command=lambda: self.save(close=False)).pack(side="left", padx=5)
        ttk.Button(right_btns, text=self.parent.get_text("btn_save"), command=lambda: self.save(close=True)).pack(side="left")

    def pick_color_menu(self):
        color = colorchooser.askcolor(initialcolor=self.color_menu_var, parent=self)
        if color[1]:
            self.color_menu_var = color[1]
            self.btn_color_menu.config(bg=color[1], fg=color[1])

    def pick_color_letra(self):
        color = colorchooser.askcolor(initialcolor=self.color_letra_var, parent=self)
        if color[1]:
            self.color_letra_var = color[1]
            self.btn_color_letra.config(bg=color[1], fg=color[1])

    def pick_foto(self):
        # Preferencia por PNG si no hay librerías externas
        filepath = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif")], parent=self)
        if filepath:
            self.foto_path = filepath
            self.lbl_foto.config(text=os.path.basename(self.foto_path))

    def restore(self):
        if messagebox.askyesno(self.parent.get_text("btn_restore"), self.parent.get_text("msg_restore"), parent=self):
            self.config_manager.restore_defaults()
            self.parent.apply_config()
            self.destroy()

    def save(self, close=True):
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
            self.cfg = new_config
            self.parent.apply_config()
            if close:
                self.destroy()
            else:
                self.title(self.parent.get_text("set_title"))
                self.create_widgets()
        else:
            messagebox.showerror("Error", "Ocurrió un problema de permisos al guardar.", parent=self)

if __name__ == "__main__":
    app = App()
    app.mainloop()
