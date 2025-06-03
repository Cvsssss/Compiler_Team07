import ply.lex as lex

# Lista para guardar los errores
errores = []
# Definimos los tokens
tokens = ('KEYWORDS', 'IDENTIFIER', 'CONSTANT', 'PUNCTUATION', 'LITERAL',
            'OPERATOR','ASSIGN', 'OR', 'AND', 'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE',
            'MENOS', 'MAS', 'DIVISION', 'MULT')

# Definición de expresiones regulares para cada tipo de token
def t_KEYWORDS(t):
    r'\b(const|double|float|int|short|char|long|struct|break|for|if|else|switch|case|do|while|default|goto|void|return)\b'
    return t
    
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

#Expresion regular de operadores
def t_ASSIGN(t):
    r'\='
    t.type = 'OPERATOR'  # Cambiamos el tipo a OPERATOR
    return t

def t_OR(t):
    r'\|\|'
    t.type = 'OPERATOR'  # Cambiamos el tipo a OPERATOR
    return t

def t_AND(t):
    r'&&'
    t.type = 'OPERATOR'  # Cambiamos el tipo a OPERATOR
    return t

def t_EQ(t):
    r'\=='
    t.type = 'OPERATOR'  # Cambiamos el tipo a OPERATOR
    return t

def t_NEQ(t):
    r'\!='
    t.type = 'OPERATOR'  # Cambiamos el tipo a OPERATOR
    return t

def t_LE(t):
    r'\<='
    t.type = 'OPERATOR'  # Cambiamos el tipo a OPERATOR
    return t

def t_GE(t):
    r'\>='
    t.type = 'OPERATOR'  # Cambiamos el tipo a OPERATOR
    return t

def t_LT(t):
    r'\<'
    t.type = 'OPERATOR'  # Cambiamos el tipo a OPERATOR
    return t

def t_GT(t):
    r'\>'
    t.type = 'OPERATOR'  # Cambiamos el tipo a OPERATOR
    return t

def t_OPERATOR(t):
    r'==|!=|<=|>=|<|>|='
    return t

#Expresion regular para los operadores aritméticos

def t_MENOS(t):
    r'\-'
    return t

def t_MAS(t):
    r'\+'
    return t

def t_DIVISION(t):
    r'\/'
    return t

def t_MULT(t):
    r'\*'
    return t

#Expresion regular para CONSTANTES
def t_CONSTANT(t):
    r'\d+(\.\d+)?'
    return t

#Expresion regular para PUNTUACION
def t_PUNCTUATION(t):
    r'[\(\):\[\]\{\};,.]'
    return t

# Expresion regular para LITERALES
def t_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    return t

#   Expresion regular para ignorar los HEADERS
def t_HEADER(t):
    r'\#include\s*(<[^>]+>|"[^"]+")'
    pass  # No retorna token, lo ignora completamente


# Ignorar espacios y saltos de línea
t_ignore = ' \t\n'

# Manejo de errores en caracteres desconocidos
def t_error(t):
    mensaje_error = f"Carácter ilegal '{t.value[0]}' en la posición {t.lexpos}"
    errores.append(mensaje_error)  # Agregar el mensaje a la lista global
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()

# Función para analizar código y devolver los tokens
def analyze_code(code):
    lexer.input(code)
    
    tokens_by_type = {
        "Keywords": [],
        "Identifiers": [],
        "Operators": [],
        "Constants": [],
        "Punctuation": [],
        "Literals": []
    }
    
    total_tokens = 0
    for tok in lexer:
        total_tokens += 1
        if tok.type == "KEYWORDS":
            tokens_by_type["Keywords"].append(tok.value)
        elif tok.type == "IDENTIFIER":
            tokens_by_type["Identifiers"].append(tok.value)
        elif tok.type == "OPERATOR":
            tokens_by_type["Operators"].append(tok.value)
        elif tok.type == "CONSTANT":
            tokens_by_type["Constants"].append(tok.value)
        elif tok.type == "PUNCTUATION":
            tokens_by_type["Punctuation"].append(tok.value)
        elif tok.type == "LITERAL":
            tokens_by_type["Literals"].append(tok.value)
    
# Formatear salida
    result = "\n"
    for error in errores:
        result += f"{error}\n"
    result += "\n=== Tokens ===\n"
    for key, values in tokens_by_type.items():
        result += f"{key}: {values}\n"
    result += f"\nTotal de tokens = {total_tokens}"
    errores.clear()
    return result