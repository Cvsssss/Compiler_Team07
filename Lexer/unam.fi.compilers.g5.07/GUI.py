import ttkbootstrap as ttk
import subprocess
import os
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
        self.root.geometry("900x600")

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
        
# Código por defecto
        codigo_por_defecto = """int main(){
        int x;
        x = 10 * 2 + 1;
        if (x>10){
        \tprintf("x es mayor a 10");
        }else{
        \tprintf("x es menor a 10");
        }
        }"""
        self.text_area_input.insert("1.0", codigo_por_defecto)


#Botones
        ttk.Button(self.left_panel, text="Cargar Archivo", bootstyle="success-outline", command=self.load_file).pack(pady=5)
        ttk.Button(self.left_panel, text="Analizador Lexico (LEXER)", bootstyle="info-outline", command=self.analyze).pack(pady=5)
        ttk.Button(self.left_panel, text="Analizador Sintactico (PARSER)", bootstyle="warning-outline", command=self.parse).pack(pady=5)
        ttk.Button(self.left_panel, text="Generar Código Objeto (.o)", bootstyle="danger-outline", command=self.compile_to_object).pack(pady=5)


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
        
        # Mostrar resultado en el área de texto
        self.text_area_output.config(state="normal")
        self.text_area_output.delete("1.0", "end")
        self.text_area_output.insert("end", parse_result)
        self.text_area_output.config(state="disabled")

        if parse_result != "ERROR DE SINTAXIS\nNo se pudo generar el árbol sintáctico.\n":
            # Intentar mostrar la imagen si existe
            img_path = "arbol_sintactico.png"
            if os.path.exists(img_path):
                try:
                    # Limpiar ventana anterior si existe
                    if hasattr(self, 'img_window'):
                        try:
                            self.img_window.destroy()
                        except:
                            pass
                    
                    # Crear nueva ventana para la imagen
                    self.img_window = ttk.Toplevel(self.root)
                    self.img_window.title("Árbol Sintáctico")
                    
                    # Cargar imagen
                    img = Image.open(img_path)
                    img = img.resize((800, 600), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    
                    # Mostrar imagen
                    label = ttk.Label(self.img_window, image=photo)
                    label.image = photo  # mantener referencia
                    label.pack(padx=10, pady=10)
                    
                    # Botón para cerrar
                    ttk.Button(
                        self.img_window, 
                        text="Cerrar", 
                        command=self.img_window.destroy
                    ).pack(pady=5)
                    
                except Exception as e:
                    messagebox.showerror("Error", 
                                    f"No se pudo mostrar el árbol: {str(e)}")
            else:
                messagebox.showinfo("Información", 
                                "Árbol sintáctico generado en formato texto. Instala Graphviz para ver la versión gráfica.")
        else:
            from PARSER_C import erroresPAR
            self.text_area_output.config(state="normal")
            self.text_area_output.delete("1.0", "end")
            self.text_area_output.insert("end", parse_result)
            for error in erroresPAR:
                self.text_area_output.insert("end", f"{error}\n")
            self.text_area_output.config(state="disabled")

#Función para el CODIGO OBJETO
    def compile_to_object(self):
        code_content = self.text_area_input.get("1.0", "end").strip()
        if not code_content:
            messagebox.showwarning("Advertencia", "No hay código para compilar")
            return

        archivo_c = "programa.c"
        archivo_objeto = "programa.o"

        # Crear el archivo .c
        with open(archivo_c, 'w') as f:
            f.write("#include <stdio.h>\n\n")
            f.write(code_content)

        # Compilar usando gcc
        comando = ["gcc", "-c", archivo_c, "-o", archivo_objeto]

        try:
            resultado = subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = f"Código objeto generado exitosamente: {archivo_objeto}\n"
        except subprocess.CalledProcessError as e:
            output = f"Error al compilar:\n{e.stderr}"

        # Mostrar resultado en el área de salida
        self.text_area_output.config(state="normal")
        self.text_area_output.delete("1.0", "end")
        self.text_area_output.insert("end", output)
        self.text_area_output.config(state="disabled")



if __name__ == "__main__":
    root = ttk.Window()
    app = CodeAnalyzerApp(root)
    root.mainloop()