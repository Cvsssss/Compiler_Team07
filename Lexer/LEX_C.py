import ply.lex as lex

# Definicion de palabras clave (keywords)
keywords = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'return': 'RETURN',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'void': 'VOID'
}

# Definicion de los tokens
tokens = [
    'ID',          # Identificadores (variables, funciones)
    'NUMBER',      # Números (enteros y flotantes)
    'TEXT',         # Texto entre comillas 
    'MAS',        # +
    'MENOS',       # -
    'MULTIPLICACION',    # *
    'DIVISION',      # /
    'ASIGNACION',      # =
    'IGUALDAD',          # ==
    'MENORQUE',          # <
    'MAYORQUE',          # >
    'PARENIZQ',      # (
    'PARENDER',      # )
    'CORCHIZQ',      # {
    'CORCHDER',      # }
    'PUNTOCOMA',   # ;
    'COMA'        # ,
] + list(keywords.values())  # Agregamos las palabras clave a los tokens

# Reglas de expresiones regulares para tokens simples
t_MAS               = r'\+'
t_MENOS             = r'-'
t_MULTIPLICACION    = r'\*'
t_DIVISION          = r'/'
t_ASIGNACION        = r'='
t_IGUALDAD          = r'=='
t_MENORQUE          = r'<'
t_MAYORQUE          = r'>'
t_PARENIZQ          = r'\('
t_PARENDER          = r'\)'
t_CORCHIZQ          = r'\{'
t_CORCHDER          = r'\}'
t_PUNTOCOMA         = r';'
t_COMA              = r','

# Para ignorar los espacios y tabulaciones
t_ignore = ' \t'

# Expresión regular para números (enteros y flotantes)
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Expresión regular para literales (enteros y flotantes)
def t_TEXT(t):
    r'"([^"\\]|\\.)*"'
    t.type = keywords.get(t.value, 'TEXT') 
    return t

# Expresión regular para identificadores y palabras clave
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'ID')  # Si es keyword, cambia el tipo
    return t

# Manejo de errores en caracteres desconocidos
def t_error(t):
    #print(f"Carácter ilegal '{t.value[0]}' en la posición {t.lexpos}")
    t.lexer.skip(1)

# Creamos el lexer
lexer = lex.lex()

# Código de prueba
codigoPrueba = """
int suma(a,b){
    int suma = a + b;
    return suma;
}

int main(){
    int suma;
    int a = 10;
    int b = 20; 
    suma = suma(a,b);
    print("El total es: %d",suma);
}
"""
lexer.input(codigoPrueba)

# Contamos los tokens
TotalTokens = 0
for tok in lexer:
    print(tok)
    TotalTokens = TotalTokens+1

# Imprimimos el numero total de tokens
print("Total de tokes = ", TotalTokens)

