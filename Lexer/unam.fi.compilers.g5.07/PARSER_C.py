import ply.yacc as yacc
from LEX_C import tokens

precedence = (
    ('right', 'ASIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'IM', 'DM'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIVISION'),
)

# Programa completo
def p_programa(p):
    '''programa : KEYWORDS IDENTIFIER PUNCTUATION PUNCTUATION bloque'''
    p[0] = ("funcion_main", p[1], p[2], p[5])

def p_bloque(p):
    '''bloque : PUNCTUATION declaraciones PUNCTUATION'''
    p[0] = ("bloque", p[2])

def p_declaraciones(p):
    '''declaraciones : declaraciones declaracion
                     | declaracion'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_declaracion_variable(p):
    '''declaracion : KEYWORDS IDENTIFIER PUNCTUATION'''
    p[0] = ("declaracion_variable", p[1], p[2])

def p_declaracion_asignacion(p):
    '''declaracion : IDENTIFIER ASIGN expresion PUNCTUATION'''
    p[0] = ("asignacion", p[1], p[3])

def p_expresion_binaria(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion MULT expresion
                 | expresion DIVISION expresion'''
    p[0] = ("operacion", p[2], p[1], p[3])

def p_expresion_valor(p):
    '''expresion : CONSTANT
                 | IDENTIFIER'''
    p[0] = ("valor", p[1])

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}'")
    else:
        print("Error de sintaxis: entrada incompleta")

parser = yacc.yacc()

def parse_code(code):
    result = parser.parse(code)
    return "Árbol sintáctico:\n" + str(result)
