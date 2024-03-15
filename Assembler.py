symbol_table = {}

def to_binary(num):
    return format(int(num), '016b')

comp_dict = {
    "": "0000000",  # Agregar una entrada para la cadena vacía
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

dest_dict = {
    "": "000",  
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jump_dict = {
    "": "000",  
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

def assemble(asm_file, hack_file):
    binary_code = []
    line_number = 0
    with open(asm_file, 'r') as f:
        for line in f:
            line_number += 1
            line = line.strip()
            if not line or line.startswith("//"):  # Ignorar líneas vacías o comentarios
                continue
            if line.startswith("("):  # Etiqueta
                symbol = line[1:-1]  
                symbol_table[symbol] = len(binary_code)  # Registrar la dirección de la etiqueta
                continue
            if line.startswith("@"):  # Instrucción A
                symbol = line[1:]
                if symbol.isdigit():  # Si es un número, lo convierte a binario
                    binary_code.append(to_binary(symbol))
                else:  # Si es un símbolo, busca su dirección en la tabla de símbolos
                    if symbol not in symbol_table:
                        symbol_table[symbol] = len(symbol_table)  
                    binary_code.append(to_binary(symbol_table[symbol]))
            else:  # Instrucción C
                dest_comp_jump = line.split(";")
                comp_jump = dest_comp_jump[-1]
                dest_comp = dest_comp_jump[0].split("=")
                dest = dest_comp[0].strip() if len(dest_comp) > 1 else ""
                comp = dest_comp[-1]
                jump = dest_comp_jump[-1] if len(dest_comp_jump) > 1 else ""
                binary_code.append("111" + comp_dict[comp] + dest_dict[dest] + jump_dict[jump])

    # Escribe el código binario en el archivo .hack
    with open(hack_file, 'w') as hf:
        for code in binary_code:
            hf.write(code + '\n')

    
    for code in binary_code:
        print(code)


asmfile = "RectL.asm"
hackfile = "RectL.hack"
assemble(asmfile, hackfile)