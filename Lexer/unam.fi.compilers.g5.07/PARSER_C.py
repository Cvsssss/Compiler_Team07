import ply.yacc as yacc
from LEX_C import tokens

# Reglas de precedencia (opcional, según la gramática que manejes)
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'MULT', 'DIVISION'),
)

# Reglas gramaticales básicas
def p_program(p):
    '''program : statement_list'''
    p[0] = ("program", p[1])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : declaration
                 | expression_statement'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : KEYWORDS IDENTIFIER PUNCTUATION'''
    p[0] = ("declaration", p[1], p[2], p[3])

def p_expression_statement(p):
    '''expression_statement : IDENTIFIER OPERATOR CONSTANT PUNCTUATION'''
    p[0] = ("expression", p[1], p[2], p[3], p[4])

def p_error(p):
    if p:
        return f"Error de sintaxis en '{p.value}'"
    else:
        return "Error de sintaxis: entrada incompleta"

# Parser
parser = yacc.yacc()

def parse_code(code):
    result = parser.parse(code)
    if isinstance(result, str):
        return result
    return "Análisis sintáctico correcto:\n" + str(result)
