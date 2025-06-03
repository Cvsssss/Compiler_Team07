import ply.lex as lex

errores = []

# Tokens
tokens = (
    'KEYWORDS', 'IDENTIFIER', 'CONSTANT', 'PUNCTUATION', 'LITERAL',
    'ASIGN', 'OR', 'AND', 'EQ', 'NEQ', 'IM', 'DM',
    'MENOS', 'MAS', 'DIVISION', 'MULT'
)

# Palabras clave
def t_KEYWORDS(t):
    r'\b(const|double|float|int|short|char|long|struct|break|for|if|else|switch|case|do|while|default|goto|void|return)\b'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_ASIGN(t):
    r'='
    return t

def t_OR(t):
    r'\|\|'
    return t

def t_AND(t):
    r'&&'
    return t

def t_EQ(t):
    r'=='
    return t

def t_NEQ(t):
    r'!='
    return t

def t_DM(t):
    r'<='
    return t

def t_IM(t):
    r'>='
    return t

def t_MENOS(t):
    r'-'
    return t

def t_MAS(t):
    r'\+'
    return t

def t_DIVISION(t):
    r'/'
    return t

def t_MULT(t):
    r'\*'
    return t

def t_CONSTANT(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_PUNCTUATION(t):
    r'[(){}\[\];,]'
    return t

def t_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    return t

def t_HEADER(t):
    r'\#include\s*(<[^>]+>|"[^"]+")'
    pass

t_ignore = ' \t\n'

def t_error(t):
    errores.append(f"Carácter ilegal '{t.value[0]}' en posición {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

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
        elif tok.type in {"ASIGN", "EQ", "NEQ", "IM", "DM", "MAS", "MENOS", "MULT", "DIVISION", "AND", "OR"}:
            tokens_by_type["Operators"].append(tok.value)
        elif tok.type == "CONSTANT":
            tokens_by_type["Constants"].append(str(tok.value))
        elif tok.type == "PUNCTUATION":
            tokens_by_type["Punctuation"].append(tok.value)
        elif tok.type == "LITERAL":
            tokens_by_type["Literals"].append(tok.value)

    result = "\n"
    for error in errores:
        result += f"{error}\n"
    result += "\n=== Tokens ===\n"
    for key, values in tokens_by_type.items():
        result += f"{key}: {values}\n"
    result += f"\nTotal de tokens = {total_tokens}"
    errores.clear()
    return result
