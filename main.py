import tkinter as tk
from config_manager import ConfigManager

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("App Gestión de Configuración (Esqueleto)")
        self.geometry("400x300")
        
        # Inicializa configuración
        self.config_manager = ConfigManager()

        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self)

        # Archivo 
        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)

        # Settings 
        menubar.add_command(label="Settings", command=self.open_settings)

        self.config(menu=menubar)
        
        # Etiqueta de bienvenida temporal
        self.lbl_bienvenida = tk.Label(self, text="Estructura inicial de la aplicación lista.\nFalta implementar diseño visual y configuraciones.", pady=50)
        self.lbl_bienvenida.pack(expand=True)

    def open_settings(self):
        print("Ventana de settings pendiente de implementar en el siguiente commit...")

if __name__ == "__main__":
    app = App()
    app.mainloop()
