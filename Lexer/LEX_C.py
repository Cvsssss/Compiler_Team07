import ply.lex as lex

# Definimos los tokens
tokens = ('KEYWORDS', 'IDENTIFIER', 'OPERATOR', 'CONSTANT', 'PUNCTUATION', 'LITERAL')

# Definición de expresiones regulares para cada tipo de token
def t_KEYWORDS(t):
    r'int|return'
    return t
    
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_OPERATOR(t):
    r'==|!=|<=|>=|<|>|=|\+|\-|\*|/'
    return t

def t_CONSTANT(t):
    r'\d+(\.\d+)?'
    return t

def t_PUNCTUATION(t):
    r'[\(\):\[\]\{\};,.]'
    return t

def t_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    return t

# Ignorar espacios y saltos de línea
t_ignore = ' \t\n'

# Manejo de errores en caracteres desconocidos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la posición {t.lexpos}")
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
    result = "\n=== Tokens ===\n"
    for key, values in tokens_by_type.items():
        result += f"{key}: {values}\n"
    result += f"\nTotal de tokens = {total_tokens}"
    
    return result
