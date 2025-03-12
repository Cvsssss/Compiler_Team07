import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import re

class CodeAnalyzerApp:
    def __init__(self, root):  
        self.root = root
        self.root.title("Analizador de Código")  
        self.root.geometry("600x400")  
        self.root.configure(bg="#f2f2f2") 
        
        self.selected_language = None
        
        tk.Label(root, text="Seleccione un lenguaje:", font=("Helvetica", 12), bg="#f2f2f2").pack(pady=10)
        self.create_language_buttons()  
        
        self.text_area = tk.Text(root, height=10, wrap=tk.WORD, font=("Arial", 10), bd=1, relief="solid")
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(root, text="Cargar Archivo", command=self.load_file, style="TButton").pack(pady=5)
        ttk.Button(root, text="Analizar", command=self.analyze, style="TButton").pack(pady=5)
    
    def create_language_buttons(self):
        frame = tk.Frame(self.root, bg="#f2f2f2")  
        frame.pack(pady=10)
        
        languages = ["C"]  # Solo permitimos C
        for lang in languages:
            button = ttk.Button(frame, text=lang, command=lambda l=lang: self.select_language(l), style="TButton")
            button.grid(row=0, column=languages.index(lang), padx=10)
    
    def select_language(self, language):
        self.selected_language = language
        messagebox.showinfo("Selección", f"Lenguaje seleccionado: {language}")
    
    def load_file(self):
        if self.selected_language != "C":
            messagebox.showwarning("Advertencia", "Solo se permite analizar código en C")
            return 
        
        file_path = filedialog.askopenfilename(filetypes=[("Archivos C", "*.c")])
        
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_area.delete("1.0", tk.END)  
                self.text_area.insert(tk.END, file.read())  
    
    def analyze(self):
        if self.selected_language != "C":
            messagebox.showwarning("Advertencia", "Solo se permite analizar código en C")
            return
    
        code_content = self.text_area.get("1.0", tk.END).strip()
    
        if not code_content:
            messagebox.showwarning("Advertencia", "No hay código para analizar")
            return

        # Expresión regular para contar tokens en C
        token_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b|\b\d+(\.\d+)?\b|\S'
        tokens = re.findall(token_pattern, code_content)
        total_tokens = len(tokens)

        messagebox.showinfo("Análisis de Tokens", f"Lenguaje: C\nTotal de Tokens: {total_tokens}")

if __name__ == "__main__": 
    root = tk.Tk()  
    app = CodeAnalyzerApp(root)  
    root.mainloop()