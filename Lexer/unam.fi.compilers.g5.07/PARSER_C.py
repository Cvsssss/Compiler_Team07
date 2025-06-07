import ply.yacc as yacc
from LEX_C import tokens, lexer as base_lexer
from graphviz import Digraph
from graphviz.backend.execute import ExecutableNotFound


def p_program(p):
    '''programa : INT ID LPAREN RPAREN LBRACE statements RBRACE'''
    p[0] = ('programa', p[6])

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | if_statement
                 | printf
                 | return SEMICOLON
                 | return'''
    p[0] = p[1]

# PARA LAS DECLARACIONES
def p_declaration(p):
    '''declaration : tipo ID SEMICOLON'''
    variables[p[2]] = 0
    p[2] = ('id', p[2])
    p[0] = ('declaracion', p[1], p[2])

def p_tipo(p):
    '''tipo : INT
           | FLOAT
           | CHAR
           | DOUBLE
           | LONG
           | SHORT'''
    if p[1] == 'int': 
        p[1] = ('tipo', p[1])
    elif p[1] == 'float': 
        p[1] = ('tipo', p[1])
    elif p[1] == 'char': 
        p[1] = ('tipo', p[1])
    elif p[1] == 'double': 
        p[1] = ('tipo', p[1])
    elif p[1] == 'long': 
        p[1] = ('tipo', p[1])
    elif p[1] == 'short': 
        p[1] = ('tipo', p[1])
    p[0] = p[1]

# PARA LAS ASIGNACIONES
def p_assignment(p):
    '''assignment : ID IGUALS expression SEMICOLON'''
    variables[p[1]] = p[3]
    p[0] = ('asignacion', p[1], p[3])

def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | expression GT term
                  | expression LT term
                  | expression EQUALS term'''
    p[0] = (p[2], p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = (p[2], p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = ('num', p[1])

def p_factor_id(p):
    'factor : ID'
    p[0] = ('id', p[1])

# PARA LAS EXPRESIONES
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE'''
    if p[3]:
        for stmt in p[6]: execute(stmt)
    else:
        for stmt in p[10]: execute(stmt)
    p[10] = ('else', p[10])
    p[0] = ('if', p[3], p[6], p[10])

# Para el printf
def p_printf(p):
    '''printf : PRINTF LPAREN STRING RPAREN SEMICOLON'''
    #print(p[3])
    p[0] = ('printf', p[3])

# Para el return
def p_return(p):
    '''return : RETURN expression
              | RETURN SEMICOLON'''
    if p[2] == ';':
        p[0] = ('return', None)
    else:
        p[0] = ('return', p[2])

# Para los errores de sintaxis
def p_error(p):
    if p:
        erroresPAR.append(f"Error de sintaxis cerca de '{p.value}' en la línea {p.lineno} columna {p.lexpos - p.lexer.lexdata.rfind('\n', 0, p.lexpos) + 1}")
    else:
        erroresPAR.append("Error de sintaxis al final del archivo, falta un  '}' o un ';'")

# Construir el parser
parser = yacc.yacc()

def execute(stmt):
    if stmt[0] == 'declaracion':
        pass
    elif stmt[0] == 'asignacion':
        variables[stmt[1]] = stmt[2]

def generar_arbol_sintactico(arbol, dot=None, padre=None):
    if dot is None:
        dot = Digraph()

    if isinstance(arbol, tuple):
        etiqueta = str(arbol[0])
        nombre_nodo = str(id(arbol))
        dot.node(nombre_nodo, etiqueta)
        if padre:
            dot.edge(padre, nombre_nodo)
        for hijo in arbol[1:]:
            generar_arbol_sintactico(hijo, dot, nombre_nodo)

    elif isinstance(arbol, list):
        for sub_arbol in arbol:
            generar_arbol_sintactico(sub_arbol, dot, padre)

    else:
        nombre_nodo = str(id(arbol))
        dot.node(nombre_nodo, str(arbol))
        if padre:
            dot.edge(padre, nombre_nodo)

    return dot

def parse_code(code):
    global variables
    global erroresPAR
    erroresPAR = []
    variables = {}

# Crear un nuevo lexer con lineno reiniciado
    lexer = base_lexer.clone()
    lexer.lineno = 1

    result = parser.parse(code, lexer=lexer)
    print(result)
    

    # Generar imagen con Graphviz
    try:
        dot = Digraph(comment='Árbol Sintáctico')
        if result is not None:
            build_graph(dot, result)
            dot.render("arbol_sintactico", format='png', cleanup=True)
            output = "Árbol sintáctico generado correctamente.\n"
            output += "Imagen del árbol generada: arbol_sintactico.png\n"
        else:
            output = "ERROR DE SINTAXIS\nNo se pudo generar el árbol sintáctico.\n"
    except ExecutableNotFound:
        output += "Graphviz no está instalado. No se generó imagen.\n"

    return output

def build_graph(dot, node, parent=None, count=[0]):
    """Construye un árbol sintáctico recursivamente en Graphviz."""
    if isinstance(node, tuple):
        label = node[0]
        node_id = str(count[0])
        count[0] += 1
        dot.node(node_id, label)
        if parent is not None:
            dot.edge(parent, node_id)
        for child in node[1:]:
            build_graph(dot, child, node_id, count)
    elif isinstance(node, list):
        for item in node:
            build_graph(dot, item, parent, count)
    else:
        label = str(node)
        node_id = str(count[0])
        count[0] += 1
        dot.node(node_id, label)
        if parent is not None:
            dot.edge(parent, node_id)