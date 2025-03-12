import ply.lex as lex

# Definimos los tokens
tokens = ('KEYWORDS', 'IDENTIFIER', 'OPERATOR', 'CONSTANT', 'PUNTUACTION', 'LITERAL')

# Listas para almacenar tokens por tipo
keywords = []
identifiers = []
operators = []
constants = []
punctuation = []
literals = []

# Definicion de KEYWORDS
def t_KEYWORDS(t):
    r'int|return'
    keywords.append(t.value)
    return t
    
# Definicion de IDENTIFIERS
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    identifiers.append(t.value)
    return t

# Definicion de OPERATORS
def t_OPERATOR(t):
    r'==|!=|<=|>=|<|>|=|\+|\-|\*|/'
    operators.append(t.value)
    return t

# Definicion de CONSTANTS
def t_CONSTANT(t):
    r'\d+(\.\d+)?'
    constants.append(t.value)
    return t

# Definicion de PUNTUATION
def t_PUNTUACTION(t):
    r'[\(\):\[\]\{\};,]'
    punctuation.append(t.value)
    return t

# Definicion de LITERALS
def t_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    literals.append(t.value)
    return t

# Para ignorar espacios y tabulaciones
t_ignore = ' \t\n'

# Manejo de errores en caracteres desconocidos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la posición {t.lexpos}")
    t.lexer.skip(1)

# Creamos el lexer
lexer = lex.lex()

# Código de prueba
codigoPrueba = """
#include <stdio.h>

int main(){
    int suma = a + b;
    a=2.5;
    b=3;
    printf("Resultado: %d", suma);
}
"""
lexer.input(codigoPrueba)

# Contamos los tokens
TotalTokens = 0

for tok in lexer:
    #print(tok)
    TotalTokens += 1

# Imprimimos los resultados
print("\n=== Tokens ===")
print(f"Keywords: {keywords}")
print(f"Identifiers: {identifiers}")
print(f"Operators: {operators}")
print(f"Constants: {constants}")
print(f"Punctuation: {punctuation}")
print(f"Literals: {literals}")
print(f"\nTotal de tokens = {TotalTokens}")
