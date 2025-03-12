import tkinter as tk
from tkinter import filedialog, messagebox

class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Código")
        self.root.geometry("600x400")
        
        self.selected_language = None
        
        tk.Label(root, text="Seleccione un lenguaje:").pack()
        
        self.create_language_buttons()
        
        self.text_area = tk.Text(root, height=10)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Button(root, text="Cargar Archivo", command=self.load_file).pack()
        tk.Button(root, text="Analizar", command=self.analyze).pack()
    
    def create_language_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()
        
        tk.Button(frame, text='C', command=lambda l='C': self.select_languageC(l)).pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text='Python', command=lambda l='Python': self.select_languagePython(l)).pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text='Java', command=lambda l='Java': self.select_languageJava(l)).pack(side=tk.LEFT, padx=5)

        #languages = ["C", "Python", "Java"]
        #for lang in languages:
        #    tk.Button(frame, text=lang, command=lambda l=lang: self.select_language(l)).pack(side=tk.LEFT, padx=5)

  
    def select_languageC(self, language):
        self.selected_language = language
        messagebox.showinfo("Selección", f"Lenguaje seleccionado: {language}")
        #Codigo para abrir el LEX para C

    def select_languagePython(self, language):
        self.selected_language = language
        messagebox.showinfo("Selección", f"Lenguaje seleccionado: {language}")
        #Codigo para abrir el LEX para Python

    def select_languageJava(self, language):
        self.selected_language = language
        messagebox.showinfo("Selección", f"Lenguaje seleccionado: {language}")
        #Codigo para abrir el LEX para Java
    
    def load_file(self):
        if not self.selected_language:
            messagebox.showwarning("Advertencia", "Seleccione un lenguaje primero")
            return
        
        ext = {"C": "c", "Python": "py", "Java": "java"}
        selected_ext = ext[self.selected_language]
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de Código", f"*.{selected_ext}")])
        
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, file.read())
    
    def analyze(self):
        if not self.selected_language:
            messagebox.showwarning("Advertencia", "Seleccione un lenguaje primero")
            return
        
        code_content = self.text_area.get("1.0", tk.END).strip()
        if not code_content:
            messagebox.showwarning("Advertencia", "No hay código para analizar")
        else:
            messagebox.showinfo("Análisis", f"Analizando código en {self.selected_language}")
            # Aquí puedes agregar análisis adicional del código ingresado.

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeAnalyzerApp(root)
    root.mainloop()
