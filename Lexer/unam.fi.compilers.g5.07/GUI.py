import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


#Archivos necesarios (Lexer y Parser)
import LEX_C
import PARSER_C


class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LEXER")
        self.root.geometry("900x550")

        # Lista de temas disponibles
        self.themes = ["flatly", "darkly", "solar", "superhero"]
        self.current_theme = "flatly"

        # Establecer estilo inicial
        self.style = ttk.Style(self.current_theme)

        # Fondo gris claro para la ventana principal
        self.root.configure(bg="#f5f5f5")

# Panel principal con dos columnas
        self.paned_window = ttk.PanedWindow(root, orient=HORIZONTAL)
        self.paned_window.pack(fill=BOTH, expand=True)

# Frame para la entrada
        self.left_panel = ttk.Frame(self.paned_window, padding=10)
        self.paned_window.add(self.left_panel, weight=1)

        self.label_input = ttk.Label(self.left_panel, text="Código Fuente", bootstyle="primary")
        self.label_input.pack(pady=5)

        self.text_area_input = ttk.Text(self.left_panel, height=15, font=("Consolas", 12))
        self.text_area_input.pack(fill=BOTH, expand=True)

#Botones
        ttk.Button(self.left_panel, text="Cargar Archivo", bootstyle="success-outline", command=self.load_file).pack(pady=5)
        ttk.Button(self.left_panel, text="Analizar Código", bootstyle="info-outline", command=self.analyze).pack(pady=5)
        ttk.Button(self.left_panel, text="Analizar Parser", bootstyle="warning-outline", command=self.parse).pack(pady=5)


# Frame de la Salida
        self.right_panel = ttk.Frame(self.paned_window, padding=10)
        self.paned_window.add(self.right_panel, weight=1)

        self.label_output = ttk.Label(self.right_panel, text="Resultado del Análisis", bootstyle="primary")
        self.label_output.pack(pady=5)

        self.text_area_output = ttk.Text(self.right_panel, height=15, font=("Consolas", 12), state="disabled")
        self.text_area_output.pack(fill=BOTH, expand=True)

# Selector de tema
        self.theme_frame = ttk.Frame(root, padding=10)
        self.theme_frame.pack(fill=X)

        self.theme_label = ttk.Label(self.theme_frame, text="Seleccionar Tema:")
        self.theme_label.pack(side=LEFT, padx=5)

        self.theme_combobox = ttk.Combobox(self.theme_frame, values=self.themes, state="readonly")
        self.theme_combobox.set(self.current_theme)
        self.theme_combobox.pack(side=LEFT, padx=5)

        self.change_theme_button = ttk.Button(self.theme_frame, text="Cambiar Tema", bootstyle="secondary", command=self.change_theme)
        self.change_theme_button.pack(side=LEFT, padx=5)

#Funcion para cargar el archivo
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de Código", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_area_input.delete("1.0", "end")
                self.text_area_input.insert("end", file.read())

    def change_theme(self):
            new_theme = self.theme_combobox.get()
            if new_theme != self.current_theme:
                self.current_theme = new_theme
                self.style = ttk.Style(new_theme)
                self.root.configure(bg="#f5f5f5" if new_theme != "darkly" else "#2b2b2b")

                # Actualizar colores de las áreas de texto dependiendo del tema
                if new_theme == "darkly":
                    input_bg = output_bg = "#2b2b2b"
                    input_fg = output_fg = "#ffffff"
                    border_color = "#444444"
                else:
                    input_bg = output_bg = "#fafafa"
                    input_fg = output_fg = "#000000"
                    border_color = "#cccccc"

                self.text_area_input.configure(bg=input_bg, fg=input_fg, highlightbackground=border_color)
                self.text_area_output.configure(bg=output_bg, fg=output_fg, highlightbackground=border_color)

#Funcion para el LEXER
    def analyze(self):
        code_content = self.text_area_input.get("1.0", "end").strip()
        if not code_content:
            messagebox.showwarning("Advertencia", "No hay código para analizar")
            return

        analysis_result = LEX_C.analyze_code(code_content)

        self.text_area_output.config(state="normal")
        self.text_area_output.delete("1.0", "end")
        self.text_area_output.insert("end", analysis_result)
        self.text_area_output.config(state="disabled")

#Funcion para el PARSER
    def parse(self):
        code_content = self.text_area_input.get("1.0", "end").strip()
        if not code_content:
            messagebox.showwarning("Advertencia", "No hay código para analizar")
            return

        parse_result = PARSER_C.parse_code(code_content)

        self.text_area_output.config(state="normal")
        self.text_area_output.delete("1.0", "end")
        self.text_area_output.insert("end", parse_result)
        self.text_area_output.config(state="disabled")


if __name__ == "__main__":
    root = ttk.Window()
    app = CodeAnalyzerApp(root)
    root.mainloop()