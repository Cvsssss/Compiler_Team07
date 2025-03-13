import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import LEX_C

class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LEXER")
        self.root.geometry("900x500")

        style = ttk.Style("darkly")

        # Panel principal con dos columnas
        self.paned_window = ttk.PanedWindow(root, orient=HORIZONTAL)
        self.paned_window.pack(fill=BOTH, expand=True)

        # Panel izquierdo (Entrada)
        self.left_panel = ttk.Frame(self.paned_window, padding=10)
        self.paned_window.add(self.left_panel, weight=1)

        self.label_input = ttk.Label(self.left_panel, text="Código Fuente", bootstyle="primary")
        self.label_input.pack(pady=5)

        self.text_area_input = ttk.Text(self.left_panel, height=15, font=("Consolas", 12))
        self.text_area_input.pack(fill=BOTH, expand=True)

        ttk.Button(self.left_panel, text="Cargar Archivo", bootstyle="success-outline", command=self.load_file).pack(pady=5)
        ttk.Button(self.left_panel, text="Analizar Código", bootstyle="info-outline", command=self.analyze).pack(pady=5)

        # Panel derecho (Salida)
        self.right_panel = ttk.Frame(self.paned_window, padding=10)
        self.paned_window.add(self.right_panel, weight=1)

        self.label_output = ttk.Label(self.right_panel, text="Resultado del Análisis", bootstyle="primary")
        self.label_output.pack(pady=5)

        self.text_area_output = ttk.Text(self.right_panel, height=15, font=("Consolas", 12), state="disabled")
        self.text_area_output.pack(fill=BOTH, expand=True)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de Código", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_area_input.delete("1.0", "end")
                self.text_area_input.insert("end", file.read())

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

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")  # Tema moderno
    app = CodeAnalyzerApp(root)
    root.mainloop()
