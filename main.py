##############################
#   David Acevedo  A01196678 #
#   Rodrigo Urbina A01281933 #
#   Proyecto Final           #
##############################

# To Do
# Corregir que guarde cuando se introducen matrices
# Maquina virtual

import lex
import yacc
import sys
import cuboSemantico
import tablaVariables

quadruples = [['GOTO',None,None,0]]

symbols = {
    'global': {
        'param': {
        },
        'vars': {
        },
        'count': {
            'int': 0,
            'float': 0,
            'char': 0,
            'bool': 0
        }
    },
    'main': {
        'param': {
        },
        'vars': {
        },
        'count': {
            'int': 0,
            'float': 0,
            'char': 0,
            'bool': 0
        }
    }
}

constants = {
    'count': {
        'int': 0,
        'float': 0,
        'char': 0,
        'bool': 0
    },
    'data': {}
}

# Aux variables to keep track of current data
current_function = 'global'
current_type = ''
current_var = ''
current_param_count = 0
current_func_var_count = 0
current_function_call = ''

# Stacks for quadruples
stack_operands = [] # stack that keeps the operands before they are located in a quadruple (PilaO)
stack_operators = [] # stack for operators (precedenece) (POper)
stack_types = [] # stack that keeps track of the type every operand has; moves together with the stack for operands
stack_jumps = []

# Sets of available variables (used to check if variable already exists)
set_var_global = set()
set_var_main = set()
set_var_function = set()

# Addresses bases
const_b = 0
global_b = 100000
local_b = 200000

mem_size = 10000
int_b = 0
float_b = 10000
char_b = 20000
bool_b = 30000

# These are reset everytime we start processing a new function
int_counter = 0
float_counter = 0
char_counter = 0
bool_counter = 0

# These are saved through the whole execution, as there may be constants anywhere
cte_counter = 0

# Lexer

# Declaration of tokens
tokens = [
    'ID',  # variable
    'LPAREN',  # (
    'RPAREN',  # )
    'LBRACKET',  # {
    'RBRACKET',  # }
    'LSQUARE',  # [
    'RSQUARE',  # ]
    'COLON',  # :
    'COMMA',  # ,
    'SEMICOLON',  # ;
    'QUOTATION',  # "
    'ASSIGN',  # =
    'LESSTHAN',  # <
    'GREATERTHAN',  # >
    'EQUAL',  # ==
    'PLUS',  # +
    'MINUS',  # -
    'MULT',  # *
    'DIV',  # /
    'AND',  # &
    'OR',  # |
    'CTE_INT',  # 123
    'CTE_FLOAT',  # 123.123
    'CTE_CHAR'  # a
]

# Reserved words
reserved = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'void': 'VOID',
    'main': 'MAIN',
    'module': 'MODULE',
    'return': 'RETURN',
    'read': 'READ',
    'write': 'WRITE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'do': 'DO',
    'to': 'TO'
}

tokens += list(reserved.values())

# Tokens symbols
t_ignore = ' \t\n'

# Symbols
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_COLON = r'\:'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
T_QUOTATION = r'\"'

# Comparison
t_ASSIGN = r'\='
t_LESSTHAN = r'\<'
t_GREATERTHAN = r'\>'
t_EQUAL = r'\=='

# Logic Operators
t_AND = r'\&'
t_OR = r'\|'

# Arithmetic Operators
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'

# Constants
#t_CTE_INT = r'([0-9])+'
#t_CTE_FLOAT = r'[0-9]+\.[0-9]+'
t_CTE_CHAR = r'(\' [^ \' ]* \' )'


# Declaration for letters with words
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Lexer error function


def t_error(t):
    global success
    success = False
    print("Caracter no valido '%s'" % t.value[0])
    t.lexer.skip(1)

# Integer
def t_CTE_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

# Float
def t_CTE_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

# New line
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


lexer = lex.lex()

# Parser


def p_program(p):
    '''program : PROGRAM ID SEMICOLON vars aux_funcion pn_go_main main pn_program_end
              | PROGRAM ID SEMICOLON vars pn_go_main main pn_program_end
              | PROGRAM ID SEMICOLON aux_funcion pn_go_main main pn_program_end
              | PROGRAM ID SEMICOLON pn_go_main main pn_program_end'''
    print("\nQuadruples")
    counter = 0
    for q in quadruples:
        print(str(counter) + ". " + str(q))
        counter += 1
    #print(symbols)

def p_main(p):
    '''main : MAIN pn_current_function LPAREN RPAREN vars bloque
            | MAIN pn_current_function LPAREN RPAREN bloque'''


def p_aux_funcion(p):
    '''aux_funcion : funcion
                   | funcion aux_funcion'''


def p_funcion(p):
    '''funcion : tipo_retorno MODULE ID pn_add_function LPAREN parametros pn_param_count RPAREN vars pn_func_var_count bloque pn_end_function
               | tipo_retorno MODULE ID pn_add_function LPAREN parametros pn_param_count RPAREN bloque pn_end_function
               | tipo_retorno MODULE ID pn_add_function LPAREN RPAREN vars pn_func_var_count bloque pn_end_function
               | tipo_retorno MODULE ID pn_add_function LPAREN RPAREN bloque pn_end_function'''
    #print("termino funcion")


def p_vars(p):
    'vars : VAR var'
    #print("termino vars")

def p_var(p):
    '''var : tipo COLON lista_ids SEMICOLON
           | tipo COLON lista_ids SEMICOLON var'''
    #print("termino var")

def p_tipo_retorno(p):
    '''tipo_retorno : tipo
                    | VOID pn_current_type'''
    #print("termino tipo_retorno")

def p_tipo(p):
    '''tipo : INT pn_current_type
          | FLOAT pn_current_type
          | CHAR pn_current_type'''
    #print("termino tipo")


def p_parametros(p):
    '''parametros : tipo ID pn_add_parameter
                  | tipo ID pn_add_parameter COMMA parametros'''
    #print("termino parametros")


def p_lista_ids(p):
    'lista_ids : aux_lista_rec'


def p_aux_lista_rec(p):
    '''aux_lista_rec : aux_lista
                    | aux_lista COMMA aux_lista_rec'''

# Declaration of variable name and adds symbol to function
def p_aux_lista(p):
    '''aux_lista : ID pn_add_symbol LSQUARE CTE_INT RSQUARE LSQUARE CTE_INT RSQUARE
                 | ID pn_add_symbol LSQUARE CTE_INT RSQUARE
                 | ID pn_add_symbol'''


def p_escritura(p):
    'escritura : WRITE LPAREN aux_escritura RPAREN SEMICOLON'
    #print("termino escritura")


def p_aux_escritura(p):
    '''aux_escritura : pn_push_write_operator letrero pn_write
                     | pn_push_write_operator expresion pn_write
                     | pn_push_write_operator letrero pn_write COMMA aux_escritura
                     | pn_push_write_operator expresion pn_write COMMA aux_escritura'''
    #print("termino aux_escritura")


def p_condicional(p):
    'condicional : WHILE pn_while_1 LPAREN expresion pn_while_2 RPAREN DO bloque pn_while_3'
    #print("termino condicional")


def p_bloque(p):
    '''bloque : LBRACKET estatutos RBRACKET
              | LBRACKET RBRACKET'''
    #print("termino bloque")


def p_estatutos(p):
    '''estatutos : estatuto estatutos
                  | estatuto'''
    #print("termino estatuto")


def p_estatuto(p):
    '''estatuto : asignacion
                | condicional
                | escritura
                | retorno
                | lectura
                | decision
                | no_condicional
                | llamada SEMICOLON'''
    #print("termino estatuto")


def p_asignacion(p):
    '''asignacion : ID pn_push_operand_and_type dimensiones ASSIGN pn_push_operator expresion pn_assign SEMICOLON
                  | ID pn_push_operand_and_type ASSIGN pn_push_operator expresion pn_assign SEMICOLON'''
    #print("termino asgignacion")

def p_retorno(p):
    'retorno : RETURN pn_push_operator LPAREN expresion pn_retorno RPAREN SEMICOLON'
    #print("termino retorno")


def p_lectura(p):
    'lectura : READ LPAREN aux_lectura RPAREN SEMICOLON'
    #print("termino lectura")


# To Do
# Corregir para que guarde que es una matriz
def p_aux_lectura(p):
    '''aux_lectura : pn_push_read_operator ID pn_push_operand_and_type pn_read
                   | pn_push_read_operator ID pn_push_operand_and_type pn_read dimensiones
                   | pn_push_read_operator ID pn_push_operand_and_type pn_read COMMA aux_lectura
                   | pn_push_read_operator ID pn_push_operand_and_type pn_read dimensiones COMMA aux_lectura'''

def p_letrero(p):
    '''letrero : QUOTATION aux_letrero QUOTATION
               | QUOTATION QUOTATION'''


def p_aux_letrero(p):
    '''aux_letrero : CTE_CHAR
                   | CTE_CHAR aux_letrero'''


def p_decision(p):
    '''decision : IF LPAREN expresion pn_if_1 RPAREN THEN bloque pn_if_2
                | IF LPAREN expresion pn_if_1 RPAREN THEN bloque ELSE pn_else bloque pn_if_2'''

def p_llamada(p):
    'llamada : ID pn_verify_func LPAREN pn_func_era aux_llamada RPAREN pn_func_gosub'
    #print("termino llamada")

def p_aux_llamada(p):
    '''aux_llamada : expresion pn_verify_argument
                   | expresion pn_verify_argument COMMA aux_llamada'''
    #print("termino aux_llamada")


def p_no_condicional(p):
    '''no_condicional : FOR ID pn_push_operand_and_type dimensiones ASSIGN pn_push_operator expresion pn_assign TO expresion pn_for_push_comparison pn_comparison pn_for_go_false DO bloque pn_for_go_back
                      | FOR ID pn_push_operand_and_type ASSIGN pn_push_operator expresion pn_assign TO expresion pn_for_push_comparison pn_comparison pn_for_go_false DO bloque pn_for_go_back'''


def p_dimensiones(p):
    '''dimensiones : LSQUARE expresion RSQUARE LSQUARE expresion RSQUARE
                   | LSQUARE expresion COMMA expresion RSQUARE
                   | LSQUARE expresion RSQUARE'''


def p_expresion(p):
    '''expresion : comparacion aux_expresion
                 | aux_comparacion'''
    #print("termino expresion")

def p_aux_expresion(p):
    '''aux_expresion : AND pn_push_operator comparacion pn_and
                     | OR pn_push_operator comparacion pn_or
                     | AND pn_push_operator comparacion pn_and aux_expresion
                     | OR pn_push_operator comparacion pn_or aux_expresion'''
    #print("termino aux_expresion")

def p_comparacion(p):
    '''comparacion : exp LESSTHAN pn_push_operator exp pn_comparison
                   | exp GREATERTHAN pn_push_operator exp pn_comparison
                   | exp EQUAL pn_push_operator exp pn_comparison'''
    #print("termino comparacion")


def p_aux_comparacion(p):
    '''aux_comparacion : exp LESSTHAN pn_push_operator exp pn_comparison
                       | exp GREATERTHAN pn_push_operator exp pn_comparison
                       | exp EQUAL pn_push_operator exp pn_comparison
                       | exp'''


def p_exp(p):
    '''exp : termino pn_addition_substraction
           | termino pn_addition_substraction PLUS pn_push_operator exp
           | termino pn_addition_substraction MINUS pn_push_operator exp'''
    #print("termino exp")


def p_termino(p):
    '''termino : factor pn_multiplication_division
             | factor pn_multiplication_division MULT pn_push_operator termino
             | factor pn_multiplication_division DIV pn_push_operator termino'''


def p_factor(p):
    '''factor : LPAREN expresion RPAREN
              |  PLUS var_cte
              |  PLUS llamada
              |  MINUS var_cte
              |  MINUS llamada
              |  var_cte
              |  llamada'''


def p_var_cte(p):
    '''var_cte : ID pn_push_operand_and_type
               | CTE_INT pn_push_constant_and_type
               | CTE_FLOAT pn_push_constant_and_type'''
    #print("termino var_cte")

def p_error(p):
    #print(p)
    counter = 0
    for q in quadruples:
        print(str(counter) + ". " + str(q))
        counter += 1
    #print("Error de sintaxis en '%s'" % p.value)
    sys.exit()

# Puntos Neuralgicos (PN)

def resetCounters():
    global int_counter, float_counter, char_counter, bool_counter
    int_counter = 0
    float_counter = 0
    char_counter = 0
    bool_counter = 0

# Get next address for variable
def nextAddress(var_type):
    global global_b, local_b
    global int_b, float_b, char_b, mem_size
    global int_counter, float_counter, char_counter, bool_counter

    if (int_counter >= mem_size or float_counter >= mem_size or char_counter >= mem_size or bool_counter >= mem_size):
        print("Error, no hay espacio de memoria suficiente")
        sys.exit()

    result = 0

    # sumar la base de
    if (current_function == 'global'):
        result += global_b
    else:
        result += local_b

    if (var_type == 'int'):
        result += int_b
        result += int_counter
        int_counter += 1
    elif (var_type == 'float'):
        result += float_b
        result += float_counter
        float_counter += 1
    elif (var_type == 'char'):
        result += char_b
        result += char_counter
        char_counter += 1
    elif (var_type == 'bool'):
        result += bool_b
        result += bool_counter
        bool_counter += 1
    else:
        print(var_type)
        print("Error: se recibio una variable de un tipo no valido")
        sys.exit()

    #print(result)
    return result

def nextCteAddress():
    global mem_size, cte_counter
    if (cte_counter >= mem_size):
        print("Error, no hay espacio de memoria suficiente")
        sys.exit()

    result = const_b
    result += cte_counter
    cte_counter += 1
    #print(result)
    return result

# Update current function
def p_pn_current_function(p):
    'pn_current_function : '
    global current_function, current_param_count, current_func_var_count
    resetCounters()
    current_function = p[-1]
    current_param_count = 0
    current_func_var_count = 0

# Update current type
def p_pn_current_type(p):
    'pn_current_type : '
    global current_type
    current_type = p[-1]

def p_pn_go_main(p):
    'pn_go_main : '
    global quadruples
    quadruples[0][3] = len(quadruples)

def p_pn_program_end(p):
    'pn_program_end : '
    global quadruples
    quad = ['End',None,None,None]
    quadruples.append(quad)

# Add symbol to the dictionary of symbols when they are declared
def p_pn_add_symbol(p):
    'pn_add_symbol : '
    # Guardar el id y el tipo del simbolo encontrado
    #print("\npn_add_symbol")
    global symbols, current_type, current_function, set_var_global, set_var_main, set_var_function, current_func_var_count
    if (symbols[current_function].get(p[-1]) is None):
        if (current_function == 'global'):
            if (p[-1] in set_var_global) :
                print("Variable has already been declared globally")
                sys.exit()
            else :
                set_var_global.add(p[-1])

        elif (current_function == 'main'):
            if (p[-1] in set_var_global) :
                print("Variable has already been declared globally")
                sys.exit()
            elif (p[-1] in set_var_main):
                print("Variable has already been declared in function: main")
                sys.exit()
            else :
                set_var_main.add(p[-1])
        else:
            if (p[-1] in set_var_global) :
                print("Variable has already been declared globally")
                sys.exit()
            elif (p[-1] in set_var_main):
                # To Do
                # agregar al error en que funcion esta repetida
                print("Variable has already been declared in function")
                sys.exit()
            else :
                set_var_function.add(tuple((current_function,p[-1])))

        current_func_var_count += 1

        symbols[current_function]['vars'][p[-1]] = {
            'name': p[-1],
            'address': nextAddress(current_type),
            'type': current_type
        }
        symbols[current_function]['count'][current_type] += 1
        #print(p[-1])
    else :
        print("Error: variable ya habia sido declarada")


# Push constant name and type to the respective stacks when it is used
def p_pn_push_constant_and_type(p):
    'pn_push_constant_and_type : '
    global constants, cte_counter
    #print("\npush_constant_and_type")
    cte_address = 0
    cte_type = type(p[-1]).__name__
    if (constants['data'].get(p[-1]) is None):
        cte_address = nextCteAddress()
        constants['data'][p[-1]] = {
            'address': cte_address,
            'type': cte_type
        }
        constants['count'][cte_type] += 1
    else:
        cte_address = constants['data'][p[-1]]['address']
    #print(cte_address)
    stack_operands.append(cte_address)
    stack_types.append(cte_type)

# Push variable name and type to the respective stacks when it is used
def p_pn_push_operand_and_type(p):
    'pn_push_operand_and_type : '
    #print(p[-1])
    #print("\npush_operand_and_type")
    global symbols, current_function, stack_var_names, stack_var_types, current_type, current_var
    #print(p[-1])
    #print(symbols)
    if(symbols[current_function]['vars'].get(p[-1]) is not None):
        #print("entre 1")
        stack_operands.append(symbols[current_function]['vars'].get(p[-1])['address'])
        stack_types.append(symbols[current_function]['vars'].get(p[-1])['type'])
        current_var = symbols[current_function]['vars'].get(p[-1])['name']
        current_type = symbols[current_function]['vars'].get(p[-1])['type']
    elif(symbols['global']['vars'].get(p[-1]) is not None):
        #print("entre 2")
        stack_operands.append(symbols['global']['vars'].get(p[-1])['address'])
        stack_types.append(symbols['global']['vars'].get(p[-1])['type'])
        current_var = symbols['global']['vars'].get(p[-1])['name']
        current_type = symbols['global']['vars'].get(p[-1])['type']
    elif(symbols[current_function]['param'].get(p[-1]) is not None):
        #print("entre 3")
        stack_operands.append(symbols[current_function]['param'].get(p[-1])['address'])
        stack_types.append(symbols[current_function]['param'].get(p[-1])['type'])
        current_var = symbols[current_function]['param'].get(p[-1])['name']
        current_type = symbols[current_function]['param'].get(p[-1])['type']
    else :
        print("Variable not defined")
        sys.exit()
    #print(p[-1])
    #print(stack_operands)
    #print(stack_operators)
    #print("termine :)")

def p_pn_push_operator(p):
    'pn_push_operator : '
    #print("\npush_operator")
    stack_operators.append(p[-1])
    #print(stack_operators)
    #print(symbols)

## PN aritmetica

def p_pn_addition_substraction(p):
    'pn_addition_substraction : '
    #print("\npn_addition_substraction")
    global stack_operators, stack_operands
    #print(stack_operands)
    #print(stack_operators)
    if (len(stack_operators) > 0):
        if (stack_operators[-1] == '+' or stack_operators[-1] == '-'):
            right_operand = stack_operands.pop()
            right_type = stack_types.pop()
            left_operand = stack_operands.pop()
            left_type = stack_types.pop()
            operator = stack_operators.pop()

            result_type = cuboSemantico.typeOperator[left_type][right_type][operator]

            if result_type is not None :
                result = nextAddress(result_type)
                symbols[current_function]['count'][result_type] += 1
                quad = [operator,left_operand,right_operand,result]
                quadruples.append(quad)
                stack_operands.append(result)
                stack_types.append(result_type)
            else:
                # To Do
                # Hacer mas especifico este error
                print("Error en suma o resta")
                sys.exit()

def p_pn_multiplication_division(p):
    'pn_multiplication_division : '
    #print("\npn_multiplication_division")
    global stack_operators, stack_operands
    #print(stack_operands)
    #print(stack_operators)
    if (len(stack_operators) > 0):
        if (stack_operators[-1] == '*' or stack_operators[-1] == '/'):
            right_operand = stack_operands.pop()
            right_type = stack_types.pop()
            left_operand = stack_operands.pop()
            left_type = stack_types.pop()
            operator = stack_operators.pop()

            result_type = cuboSemantico.typeOperator[left_type][right_type][operator]

            if result_type is not None :
                result = nextAddress(result_type)
                symbols[current_function]['count'][result_type] += 1
                quad = [operator,left_operand,right_operand,result]
                quadruples.append(quad)
                stack_operands.append(result)
                stack_types.append(result_type)
            else:
                # To Do
                # Hacer mas especifico este error
                print("Error en multiplicacion o division")
                sys.exit()

## PN estatutos

def p_pn_assign(p):
    'pn_assign : '
    #print("\npn_assign")
    global stack_operators, stack_operands, stack_types, quadruples
    #print(stack_operands)
    #print(stack_types)
    #print(stack_operators)

    if (len(stack_operators) > 0):
        if (stack_operators[-1] == '='):
            right_operand = stack_operands.pop()
            right_type = stack_types.pop()
            left_operand = stack_operands.pop()
            left_type = stack_types.pop()
            operator = stack_operators.pop()

            result_type = cuboSemantico.typeOperator[left_type][right_type][operator]

            if result_type is not None :
                quad = [operator,right_operand,None,left_operand]
                quadruples.append(quad)
                #stack_operands.append(result)
                #stack_types.append(result_type)
            else:
                # To Do
                # Hacer mas especifico este error
                print("Error en asginacion")
                sys.exit()

# lectura
def p_pn_push_read_operator(p):
    'pn_push_read_operator : '
    stack_operators.append('read')

def p_pn_read(p):
    'pn_read : '
    if (len(stack_operators) > 0):
        if (stack_operators[-1] == 'read'):
            operand = stack_operands.pop()
            stack_types.pop()
            operator = stack_operators.pop()

            quad = [operator,None,None,operand]
            quadruples.append(quad)

# escritura
# To Do
# Escribir constantes de tipo string
def p_pn_push_write_operator(p):
    'pn_push_write_operator : '
    stack_operators.append('write')

def p_pn_write(p):
    'pn_write : '
    if (len(stack_operators) > 0):
        if (stack_operators[-1] == 'write'):
            operand = stack_operands.pop()
            stack_types.pop()
            operator = stack_operators.pop()

            quad = [operator,None,None,operand]
            quadruples.append(quad)

# comparacion
def p_pn_and(p):
    'pn_and :'
    global stack_operators, stack_operands, stack_types
    #print("\n pn_and")
    #print(stack_operators)
    ##print(stack_operands)
    #print(stack_types)
    if (len(stack_operators) > 0):
        if (stack_operators[-1] == '&'):
            right_operand = stack_operands.pop()
            right_type = stack_types.pop()
            left_operand = stack_operands.pop()
            left_type = stack_types.pop()
            operator = stack_operators.pop()

            result_type = cuboSemantico.typeOperator[left_type][right_type][operator]

            if result_type is not None :
                #print("entre")
                #print(result_type)
                result = nextAddress(result_type)
                symbols[current_function]['count'][result_type] += 1
                quad = [operator,left_operand,right_operand,result]
                quadruples.append(quad)
                stack_operands.append(result)
                stack_types.append(result_type)
                #print("termino if")
            else:
                # To Do
                # Hacer mas especifico este error
                print("Error en asginacion")
                sys.exit()
    #print("termino pn_and")


def p_pn_or(p):
    'pn_or : '
    global stack_operators, stack_operands, stack_types
    #print("\n pn_or")
    #print(stack_operators)
    #print(stack_operands)
    #print(stack_types)
    if (len(stack_operators) > 0):
        if (stack_operators[-1] == '|'):
            right_operand = stack_operands.pop()
            right_type = stack_types.pop()
            left_operand = stack_operands.pop()
            left_type = stack_types.pop()
            operator = stack_operators.pop()

            result_type = cuboSemantico.typeOperator[left_type][right_type][operator]

            if result_type is not None :
                result = nextAddress(result_type)
                symbols[current_function]['count'][result_type] += 1
                quad = [operator,left_operand,right_operand,result]
                quadruples.append(quad)
                stack_operands.append(result)
                stack_types.append(result_type)
            else:
                # To Do
                # Hacer mas especifico este error
                print("Error en asginacion")
                sys.exit()

# decision
def p_pn_comparison(p):
    'pn_comparison : '
    global stack_operands, stack_types, stack_operators, quadruples
    if (len(stack_operators) > 0):
        if (stack_operators[-1] == '<' or stack_operators[-1] == '>' or stack_operators[-1] == '=='):
            right_operand = stack_operands.pop()
            right_type = stack_types.pop()
            left_operand = stack_operands.pop()
            left_type = stack_types.pop()
            operator = stack_operators.pop()

            result_type = cuboSemantico.typeOperator[left_type][right_type][operator]
            #print(left_type)
            #print(right_type)
            #print(operator)
            #print(result_type)
            if result_type is not None :
                result = nextAddress(result_type)
                symbols[current_function]['count'][result_type] += 1
                quad = [operator,left_operand,right_operand,result]
                quadruples.append(quad)
                stack_operands.append(result)
                stack_types.append(result_type)
            else:
                # To Do
                # Hacer mas especifico este error
                print("Error en comparacion")
                sys.exit()

def p_pn_if_1(p):
    'pn_if_1 : '
    global stack_operands, stack_types, quadruples, stack_jumps, quadruples
    #print(stack_operands)
    #print(stack_types)
    result = stack_operands.pop()
    result_type = stack_types.pop()
    if (result_type == 'bool'):
        quad = ['GOTOF',result,None,'.pending_jump']
        quadruples.append(quad)
        stack_jumps.append(len(quadruples)-1)

    else:
        # To Do
        # Hacer mas especifico este error
        print("La expresion no es de tipo bool en la decision")
        sys.exit()

def p_pn_if_2(p):
    'pn_if_2 : '
    global stack_jumps, quadruples
    endOfDecision = stack_jumps.pop()
    fill(endOfDecision,len(quadruples))

def p_pn_else(p):
    'pn_else : '
    global stack_jumps, quadruples
    endOfElse = stack_jumps.pop()
    stack_jumps.append(len(quadruples)-1)
    fill(endOfElse,len(quadruples))

# condicional (WHILE)
def p_pn_while_1(p):
    'pn_while_1 : '
    #print('pn_while_1')
    stack_jumps.append(len(quadruples))

def p_pn_while_2(p):
    'pn_while_2 : '
    #print('pn_while_1')
    result = stack_operands.pop()
    result_type = stack_types.pop()
    if (result_type == 'bool'):
        quad = ['GOTOF',result,None,'.pending_jump']
        quadruples.append(quad)
        stack_jumps.append(len(quadruples)-1)
    else:
        # To Do
        # Hacer mas especifico este error
        print("La expresion no es de tipo bool en while")
        sys.exit()

def p_pn_while_3(p):
    'pn_while_3 : '
    print('pn_while_3')
    global stack_jumps, quadruples
    endOfWhile = stack_jumps.pop()

    whileComparison = stack_jumps.pop()
    quad = ['GOTO',None,None,whileComparison]
    quadruples.append(quad)

    fill(endOfWhile,len(quadruples))
    print('saliendo 3')

# no_condicional (FOR)

def p_pn_for_push_comparison(p):
    'pn_for_push_comparison : '
    #print("pn_for_push_comparison")
    global stack_operands, stack_types, quadruples, stack_jumps, quadruples, current_func

    stack_operands.append(symbols[current_function][current_var]['address'])
    stack_types.append(current_type)
    stack_operators.append('==')

def p_pn_for_go_false(p):
    'pn_for_go_false : '
    #print('pn_for_go_false')
    global stack_operands, stack_types, quadruples, stack_jumps, quadruples
    stack_jumps.append(len(quadruples)-1)

    result = stack_operands.pop()
    result_type = stack_types.pop()
    if (result_type == 'bool'):
        quad = ['GOTOF',result,None,'.pending_jump']
        quadruples.append(quad)
        stack_jumps.append(len(quadruples)-1)

    else:
        # To Do
        # Hacer mas especifico este error
        print("La expresion no es de tipo bool en el for (probablemente no son enteros)")
        sys.exit()

def p_pn_for_go_back(p):
    'pn_for_go_back : '
    #print('pn_for_go_back')
    global stack_jumps, quadruples

    forOnFalse = stack_jumps.pop()

    forComparison = stack_jumps.pop()
    # To do
    # Cambiar para agregar constante que sea 1 y agregar el id de la variable del for
    quad = ['+','id','1','id']
    quadruples.append(quad)
    quad = ['GOTO',None,None,forComparison]
    quadruples.append(quad)

    fill(forOnFalse,len(quadruples))

# Funciones
def p_pn_add_function(p):
    'pn_add_function : '
    global symbols, current_function, current_param_count, current_func_var_count
    resetCounters()
    current_function = p[-1]
    current_param_count = 0
    current_func_var_count = 0
    if (symbols.get(p[-1]) is None):
        symbols[p[-1]] = {
            'start': len(quadruples),
            'return_type': current_type,
            'param': {},
            'vars': {},
            'count': {
                'int': 0,
                'float': 0,
                'char': 0,
                'bool': 0
            }
        }
        if (current_type != 'void'):
            symbols['global']['vars'][p[-1]] = {
                'name': p[-1],
                'address': nextAddress(current_type),
                'type': current_type
            }
            symbols[current_function]['count'][current_type] += 1
    else:
        print("Error: Function has already been declared")
        sys.exit()

def p_pn_add_parameter(p):
    'pn_add_parameter : '
    #print("\nadd_parameter")
    global symbols, current_function, current_type, current_param_count
    #print(p[-1])
    #print(current_type)
    if (symbols['global']['vars'].get(p[-1]) is None):
        symbols[current_function]['param'][p[-1]] = {
            'name': p[-1],
            'address': nextAddress(current_type),
            'type': current_type
        }
        symbols[current_function]['count'][current_type] += 1
        current_param_count += 1
    else:
        print("Error in function parameters declaration")
        sys.exit()

def p_pn_param_count(p):
    'pn_param_count : '
    global symbols, current_function, current_param_count, current_func_var_count
    symbols[current_function]['param_count'] = current_param_count

def p_pn_func_var_count(p):
    'pn_func_var_count : '
    global symbols, current_function, current_param_count, current_func_var_count
    symbols[current_function]['var_count'] = current_func_var_count

def p_pn_end_function(p):
    'pn_end_function :'
    global quadruples
    # To Do
    # Insert into DirFunc the number of temporal vars used.

    quad = ['ENDFunc',None,None,None]
    quadruples.append(quad)

def p_pn_verify_func(p):
    'pn_verify_func : '
    #print('\nverify_func')
    global symbols, current_function_call,stack_operands,stack_types
    current_function_call = p[-1]
    #print(current_function_call)
    #stack_operands.append(p[-1])
    #stack_types.append('function')
    stack_operands.append('bottom')
    stack_types.append('bottom')
    stack_operators.append('bottom')
    if (symbols[current_function] is None):
        print("Error la funcion no ha sido declarada")
        sys.exit()

def p_pn_func_era(p):
    'pn_func_era : '
    #print("\nfunc_era")
    global current_function, symbols, quadruples, current_param_count
    quad = ["ERA",None,None,p[-3]]
    quadruples.append(quad)
    current_param_count = 1
    #print("termino func_era")

def p_pn_verify_argument(p):
    'pn_verify_argument : '
    #print("verify_argument")
    global current_param_count, symbols, quadruples, current_function_call
    arg_name = stack_operands.pop()
    arg_type = stack_types.pop()
    param = list(symbols[current_function_call]['param'])
    #print(arg_name)
    #print(arg_type)
    #print(param)
    #print(current_function_call)

    #print(current_param_count)
    if (current_param_count <= len(param)):
        if(symbols[current_function_call]['param'][param[current_param_count-1]]['type'] == arg_type):
            #print("flag")
            # To Do
            # Checar si el param1 tmb se pone como direccion
            quad = ['param', arg_name, None, "p" + str(current_param_count)]
            quadruples.append(quad)
            #print("flag")
        else:
            print("No concuerda el tipo de parametro de la funcion")
            sys.exit()
    else:
        print("Hay más parametros de los que pide la funcion")
        sys.exit()
    #print("salida")

def p_pn_func_gosub(p):
    'pn_func_gosub : '
    global current_function_call, symbols, quadruples, current_function
    quad = ["gosub",None,None,current_function_call]
    quadruples.append(quad)
    result_type = symbols[current_function_call]['return_type']
    if (result_type != 'void'):
        result = nextAddress(result_type)
        symbols[current_function]['count'][result_type] += 1
        quad = ["=", symbols['global']['vars'][current_function_call]['address'],None,result]
        quadruples.append(quad)
        stack_operands.pop()
        stack_types.pop()
        stack_operators.pop()
        stack_operands.append(result)
        stack_types.append(result_type)

# retorno
def p_pn_retorno(p):
    'pn_retorno :'
    global stack_operators, stack_operands, stack_types, current_function
    if (len(stack_operators) > 0):
        if (stack_operators[-1] == 'return'):
            right_operand = stack_operands.pop()
            right_type = stack_types.pop()
            operator = stack_operators.pop()

            if (right_type == symbols[current_function]['return_type']):
                quad = [operator,None,None,right_operand]
                quadruples.append(quad)
            else:
                # To Do
                # Hacer mas especifico este error
                print("La expresion no es de tipo bool en while")
                sys.exit()

# Auxiliary functions

def fill(quad_number, jumpTo): #quad_number = int, jumpTo = int
    global quadruples
    quadruples[quad_number][3] = jumpTo

parser = yacc.yacc()

if len(sys.argv) != 2:
    data = input("Introduzca nombre del archivo: ")
else:
    data = sys.argv[1]


try:
    f = open(data, 'r')
    s = f.read()
    f.close()

    #lexer.input(s)
    #for tok in lexer:
    #    print(tok)

except:
    print("No se pudo abrir el archivo")

try:
    parser.parse(s, lexer = lexer)
    object_code = {
        'symbols': symbols,
        'quadruples': quadruples,
        'constants': constants
    }
    with open('output.txt', 'w') as file:
        file.write(str(object_code))
except:
    #counter = 0
    #for q in quadruples:
        #print(str(counter) + ". " + str(q))
        #counter += 1
    print("No se pudo compilar el programa")
