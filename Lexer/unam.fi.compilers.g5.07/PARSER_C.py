import ply.yacc as yacc
from LEX_C import tokens
from graphviz import Digraph
import os
import platform
from graphviz.backend.execute import ExecutableNotFound

precedence = (
    ('right', 'ASIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'IM', 'DM'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIVISION'),
)
    
# Gramatica
def p_programa(p):
    '''programa : KEYWORDS IDENTIFIER PUNCTUATION PUNCTUATION bloque'''
    p[0] = ("funcion_main", p[1], p[2], p[5])
    add_node(p[0], p[1])
    add_node(p[0], p[2])
    add_node(p[0], p[5])

def p_bloque(p):
    '''bloque : PUNCTUATION declaraciones PUNCTUATION'''
    p[0] = ("bloque", p[2])
    add_node(p[0], p[2])

def p_declaraciones(p):
    '''declaraciones : declaraciones declaracion
                     | declaracion'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
        for decl in p[1]:
            add_node(p[0], decl)
        add_node(p[0], p[2])
    else:
        p[0] = [p[1]]
        add_node(p[0], p[1])

def p_declaracion_variable(p):
    '''declaracion : KEYWORDS IDENTIFIER PUNCTUATION'''
    p[0] = ("declaracion_variable", p[1], p[2])
    add_node(p[0], p[1])
    add_node(p[0], p[2])

def p_declaracion_asignacion(p):
    '''declaracion : IDENTIFIER ASIGN expresion PUNCTUATION'''
    p[0] = ("asignacion", p[1], p[3])
    add_node(p[0], p[1])
    add_node(p[0], p[3])

def p_expresion_binaria(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion MULT expresion
                 | expresion DIVISION expresion'''
    p[0] = ("operacion", p[2], p[1], p[3])
    add_node(p[0], p[1])
    add_node(p[0], p[2])
    add_node(p[0], p[3])

def p_expresion_valor(p):
    '''expresion : CONSTANT
                 | IDENTIFIER'''
    p[0] = ("valor", p[1])
    add_node(p[0], p[1])

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}'")
    else:
        print("Error de sintaxis: entrada incompleta")

#FUNCIONES PARA CREAR EL ARBOL GRÁFICO
def check_graphviz_installed():
    try:
        #Para verificar si Graphviz está instalado, intentamos crear un gráfico simple
        test_dot = Digraph()
        test_dot.node('A', 'Test')
        test_dot.render('test_graph', format='png', cleanup=True)
        os.remove('test_graph.png') #Y luego borro la imagen generada
        return True
    except ExecutableNotFound:
        return False
    except Exception:
        return False

# Variable global para el árbol gráfico
dot = None
graphviz_installed = check_graphviz_installed()

def add_node(parent, child):
    if graphviz_installed and dot is not None:
        dot.node(str(id(child)), str(child))
        if parent is not None:
            dot.edge(str(id(parent)), str(id(child)))

def generate_text_tree(node, level=0):
    if isinstance(node, tuple):
        result = "  " * level + node[0] + "\n"
        for item in node[1:]:
            result += generate_text_tree(item, level + 1)
        return result
    elif isinstance(node, list):
        result = ""
        for item in node:
            result += generate_text_tree(item, level)
        return result
    else:
        return "  " * level + str(node) + "\n"

parser = yacc.yacc()

def parse_code(code):
    global dot
    
    # Limpiar el árbol anterior
    if graphviz_installed:
        dot = Digraph(comment='Árbol Sintáctico', format='png')
        dot.attr('node', shape='box', style='rounded')
    
    result = parser.parse(code)
    
    text_tree = "Árbol sintáctico:\n" + str(result)
    
    if graphviz_installed:
        try:
            dot.render('arbol_sintactico', format='png', cleanup=True)
            return text_tree + "\n\nÁrbol gráfico generado, busca el archivo como 'arbol_sintactico.png'"
        except Exception as e:
            return text_tree + f"\n\nError al generar gráfico: {str(e)}"
    else:
        install_instructions = {
            'Darwin': "brew install graphviz",
            'Linux': "sudo apt-get install graphviz",
            'Windows': "Descargar de https://graphviz.org/download/"
        }
        system = platform.system()
        instruction = install_instructions.get(system, 
                     "Instala Graphviz desde https://graphviz.org/download/")
        
        return (text_tree + "\n\nPara ver el árbol gráfico, instala Graphviz:\n" +
                instruction + "\nLuego reinicia la aplicación.")