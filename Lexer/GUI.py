import tkinter as tk
from tkinter import filedialog, messagebox
import LEX_C # Importamos el lexer

class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LEXER")
        self.root.geometry("800x400")

        # Crear un PanedWindow para dividir la ventana en dos paneles
        self.paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo para la entrada de texto
        self.left_panel = tk.Frame(self.paned_window)
        self.paned_window.add(self.left_panel)
        
        # Área de texto para la entrada
        self.text_area_input = tk.Text(self.left_panel, height=20)
        self.text_area_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botón para cargar archivo
        tk.Button(self.left_panel, text="Cargar Archivo", command=self.load_file).pack()
        
        # Botón para analizar
        tk.Button(self.left_panel, text="Analizar", command=self.analyze).pack()
        
        # Panel derecho para la salida de texto
        self.right_panel = tk.Frame(self.paned_window)
        self.paned_window.add(self.right_panel)
        
        # Área de texto para la salida
        self.text_area_output = tk.Text(self.right_panel, height=20, state=tk.DISABLED)
        self.text_area_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de Código", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_area_input.delete("1.0", tk.END)
                self.text_area_input.insert(tk.END, file.read())
    
    def analyze(self):
        code_content = self.text_area_input.get("1.0", tk.END).strip()
        if not code_content:
            messagebox.showwarning("Advertencia", "No hay código para analizar")
            return

        # Llamamos a la función de análisis del lexer
        analysis_result = LEX_C.analyze_code(code_content)

        # Mostrar el resultado en la salida
        self.text_area_output.config(state=tk.NORMAL)
        self.text_area_output.delete("1.0", tk.END)
        self.text_area_output.insert(tk.END, analysis_result)
        self.text_area_output.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeAnalyzerApp(root)
    root.mainloop()
