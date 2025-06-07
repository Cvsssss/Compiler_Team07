import ply.lex as lex

erroresLEX = []

# Tokens
tokens = (
    'INT', 'FLOAT', 'CHAR','DOUBLE', 'LONG', 'SHORT',   # Tipos de datos
    'RETURN','IF', 'ELSE',  # KEYWORDS
    'ID', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'GT', 'LT', 'EQUALS', 'IGUALS',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON',
    'PRINTF', 'STRING'
)

#KEYWORDS
KEYWORDS = {}

#Tipo
def t_tipo(t):
    r'int|float|char|double|long|short'
    t.type = t.value.upper()  # Convertir a mayúsculas para tokens
    return t

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'=='
t_IGUALS  = r'='
t_GT      = r'>'
t_LT      = r'<'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_SEMICOLON = r';'

t_ignore = ' \t'

def t_INT(t):
    r'int|float|char'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_PRINTF(t):
    r'printf'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_STRING(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]  # Quita comillas
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_HEADER(t):
    r'\#include\s*(<[^>]+>|"[^"]+")'
    pass

def t_error(t):
    erroresLEX.append(f"Carácter ilegal '{t.value[0]}' en posición {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

def analyze_code(code):
    lexer.input(code)
    result = ""
    if len(erroresLEX) > 0:
        result += "=== ERROR LEXICO ===\n"
        for error in erroresLEX:
            result += f"Errores lexicos: {error}\n\n"
    result += "=== Tokens Reconocidos ===\n"
    i = 0
    for tok in lexer:
        i = i+1
    result += (f"Total de tokens = "+str(i))
    erroresLEX.clear()  # Limpiar errores después del análisis
    return result