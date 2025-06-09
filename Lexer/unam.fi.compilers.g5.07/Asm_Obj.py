import re

#GENERACIÓN DEL CÓDIGO OBJETO EN ENSAMBLADOR ZILOG
def generar_codigo_zilog(ast):
    codigo = []
    etiquetas = {'if': 0}

    def gen_expr(expr):
        if expr[0] == 'num':
            return [f"LD A, {expr[1]}"]
        elif expr[0] == 'id':
            return [f"LD A, ({expr[1]})"]
        elif expr[0] in ['+', '-', '*', '/', '>', '<']:
            izq = gen_expr(expr[1])
            der = gen_expr(expr[2])
            op_map = {'+': 'ADD', '-': 'SUB', '*': 'CALL MUL', '/': 'CALL DIV',
                      '>': 'CP', '<': 'CP'}
            return izq + ["PUSH AF"] + der + ["POP BC", "LD A, B", op_map[expr[0]]]
        return []

    def gen_stmt(stmt):
        nonlocal etiquetas
        codigo_local = []
        if stmt[0] == 'declaracion':
            var = stmt[2][1]
            codigo_local.append(f"{var}: DEFB 0")
        elif stmt[0] == 'asignacion':
            var = stmt[1]
            codigo_local += gen_expr(stmt[2])
            codigo_local.append(f"LD ({var}), A")
        elif stmt[0] == 'printf':
            mensaje = stmt[1].strip('"')
            codigo_local.append(f"; PRINT \"{mensaje}\"")  # comentario
        elif stmt[0] == 'if':
            cond = gen_expr(stmt[1])
            etq_else = f"ELSE_{etiquetas['if']}"
            etq_end = f"ENDIF_{etiquetas['if']}"
            etiquetas['if'] += 1

            codigo_local += cond
            codigo_local.append(f"CP 10")
            codigo_local.append(f"JP LE, {etq_else}")  # Jump si x <= 10

            for s in stmt[2]:
                codigo_local += gen_stmt(s)
            codigo_local.append(f"JP {etq_end}")
            codigo_local.append(f"{etq_else}:")
            for s in stmt[3][1]:  # lista dentro de 'else'
                codigo_local += gen_stmt(s)
            codigo_local.append(f"{etq_end}:")
        return codigo_local

    for s in ast[1]:  # ast es ('programa', [stmt1, stmt2, ...])
        codigo += gen_stmt(s)

    return '\n'.join(codigo)

# SECCION PARA GENERAR EL CÓDIGO OBJETO DEL ENSAMBLADOR ZILOG
INSTRUCTION_SET = {
    r"LD A, (\d+)": lambda n: ["01", f"{int(n):02X}"],
    r"LD A, \((\w+)\)": lambda var: ["02", var],
    r"LD \((\w+)\), A": lambda var: ["03", var],
    r"PUSH AF": lambda: ["04"],
    r"POP BC": lambda: ["05"],
    r"LD A, B": lambda: ["06"],
    r"CALL MUL": lambda: ["07"],
    r"ADD": lambda: ["08"],
    r"CP": lambda: ["09"],
    r"CP (\d+)": lambda n: ["0A", f"{int(n):02X}"],
    r"JP LE, (\w+)": lambda lbl: ["0B", lbl],
    r"JP (\w+)": lambda lbl: ["0C", lbl],
}

symbol_table = {}  # var -> address
labels = {}        # label -> address
program = []       # list of (instr_str, obj_code)
memory_counter = 0x00

def parse_asm_line(line):
    global memory_counter
    line = line.strip()
    if not line or line.startswith(";"):
        return

    # Label
    if re.match(r"^\w+:$", line):
        label = line[:-1]
        labels[label] = memory_counter
        return

    # Variable declaration
    if match := re.match(r"^(\w+): DEFB \d+$", line):
        var = match.group(1)
        symbol_table[var] = memory_counter
        memory_counter += 1
        return

    # Instruction matching
    for pattern, handler in INSTRUCTION_SET.items():
        match = re.match(pattern, line)
        if match:
            args = match.groups()
            obj = handler(*args) if args else handler()
            program.append((line, obj))
            memory_counter += len(obj)
            return

    # Print as comment
    program.append((line, []))

def resolve_symbols(instrs):
    resolved = []
    for code in instrs:
        if code in symbol_table:
            resolved.append(f"{symbol_table[code]:02X}")
        elif code in labels:
            resolved.append(f"{labels[code]:02X}")
        else:
            resolved.append(code)
    return resolved

def assemble(lines):
    # Primer pasada: etiquetas y símbolos
    for line in lines:
        parse_asm_line(line)

    # Segunda pasada: resolver direcciones
    output = []
    for instr, obj_code in program:
        if obj_code:
            resolved = resolve_symbols(obj_code)
            output.append(" ".join(resolved))
        else:
            output.append(f"; {instr}")
    return output
