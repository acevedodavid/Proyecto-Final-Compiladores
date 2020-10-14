##############################
#   David Acevedo  A01196678 #
#   Rodrigo Urbina A01281933 #
#   Proyecto Final           #
##############################

import lex
import yacc
import sys
import cuboSemantico
import tablaVariables

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
t_CTE_INT = r'[0-9]+'
t_CTE_FLOAT = r'[0-9]+\.[0-9]+'
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


def t_CTEI(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

# Float


def t_CTEF(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

# New line


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


lexer = lex.lex()

# Parser


def p_programa(p):
    '''program : PROGRAM ID SEMICOLON vars aux_funcion MAIN LPAREN RPAREN bloque
              | PROGRAM ID SEMICOLON vars MAIN LPAREN RPAREN bloque
              | PROGRAM ID SEMICOLON aux_funcion MAIN LPAREN RPAREN bloque
              | PROGRAM ID SEMICOLON MAIN LPAREN RPAREN bloque'''
    p[0] = "complete"


def p_aux_funcion(p):
    '''aux_funcion : funcion
                   | funcion aux_funcion'''


def p_funcion(p):
    '''funcion : tipo_retorno MODULE ID LPAREN parametros RPAREN COLON vars bloque
               | tipo_retorno MODULE ID LPAREN parametros RPAREN COLON bloque'''


def p_vars(p):
    'vars : VAR var'


def p_var(p):
    '''var : tipo SEMICOLON lista_ids COLON
           | tipo SEMICOLON lista_ids COLON var'''


def p_tipo_retorno(p):
    '''tipo_retorno : tipo
                    | VOID'''


def p_tipo(p):
    '''tipo : INT
          | FLOAT
          | CHAR'''


def p_parametros(p):
    '''parametros : tipo ID
                  | tipo ID COMMA parametros'''


def p_lista_ids(p):
    'lista_ids : aux_lista_rec'


def p_aux_lista_rec(p):
    '''aux_lista_rec : aux_lista
                    | aux_lista COMMA aux_lista_rec'''


def p_aux_lista(p):
    '''aux_lista : ID LSQUARE CTE_INT RSQUARE LSQUARE CTE_INT RSQUARE
                 | ID LSQUARE CTE_INT RSQUARE
                 | ID'''


def p_escritura(p):
    'escritura : WRITE LPAREN aux_escritura RPAREN SEMICOLON'


def p_aux_escritura(p):
    '''aux_escritura : letrero
                     | expresion
                     | letrero COMMA aux_escritura
                     | expresion COMMA aux_escritura'''


def p_condicional(p):
    'condicional : WHILE LPAREN expresion RPAREN DO bloque'


def p_bloque(p):
    '''bloque : LBRACKET estatutos RBRACKET
              | LBRACKET RBRACKET'''


def p_estatutos(p):
    '''estatutos : estatuto estatutos
                  | estatuto'''


def p_estatuto(p):
    '''estatuto : asignacion
                | condicional
                | escritura
                | retorno
                | lectura
                | llamada_void
                | decision
                | no_condicional'''


def p_asignacion(p):
    '''asignacion : ID dimensiones ASSIGN expresion COLON
                  | ID ASSIGN expresion COLON'''


def p_retorno(p):
    'retorno : RETURN LPAREN expresion RPAREN'


def p_lectura(p):
    'lectura : READ LPAREN aux_lectura RPAREN COLON'


def p_aux_lectura(p):
    '''aux_lectura : ID
                   | ID dimensiones
                   | ID aux_lectura
                   | ID dimensiones aux_lectura'''


def p_letrero(p):
    '''letrero : QUOTATION aux_letrero QUOTATION
               | QUOTATION QUOTATION'''


def p_aux_letrero(p):
    '''aux_letrero : CTE_CHAR
                   | CTE_CHAR aux_letrero'''


def p_decision(p):
    '''decision : IF LPAREN expresion RPAREN THEN bloque
                | IF LPAREN expresion RPAREN THEN bloque ELSE bloque'''


def p_llamada_void(p):
    'llamada_void : llamada'


def p_llamada(p):
    'llamada : ID LPAREN aux_llamada RPAREN'


def p_aux_llamada(p):
    '''aux_llamada : expresion
                   | expresion aux_llamada'''


def p_no_condicional(p):
    '''no_condicional : FOR ID dimensiones ASSIGN expresion TO expresion DO bloque
                      | FOR ID ASSIGN expresion TO
                      | expresion DO bloque'''


def p_dimensiones(p):
    '''dimensiones : LSQUARE expresion RSQUARE LSQUARE expresion RSQUARE
                   | LSQUARE expresion COMMA expresion RSQUARE
                   | LSQUARE expresion RSQUARE'''


def p_expresion(p):
    '''expresion : comparacion aux_expresion
                 | aux_comparacion'''


def p_aux_expresion(p):
    '''aux_expresion : AND comparacion
                     | OR comparacion
                     | AND comparacion aux_expresion
                     | OR comparacion aux_expresion'''


def p_comparacion(p):
    '''comparacion : exp LESSTHAN exp
                   | exp GREATERTHAN exp
                   | exp EQUAL exp'''


def p_aux_comparacion(p):
    '''aux_comparacion : exp LESSTHAN exp
                       | exp GREATERTHAN exp
                       | exp EQUAL exp
                       | exp'''


def p_exp(p):
    '''exp : termino
           | termino PLUS exp
           | termino MINUS exp'''


def p_termino(p):
    '''termino : factor
             | factor MULT termino
             | factor DIV termino'''


def p_factor(p):
    '''factor : LPAREN expresion RPAREN
              |  PLUS var_cte
              |  PLUS llamada
              |  MINUS var_cte
              |  MINUS llamada
              |  var_cte
              |  llamada'''


def p_var_cte(p):
    '''var_cte : ID
               | CTE_INT
               | CTE_FLOAT'''


def p_error(p):
    print("Error de sintaxis en '%s'" % p.value)


parser = yacc.yacc()

#data = raw_input("Introduzca nombre del archivo: ")

# try:
#    f = open(data, 'r')
#    s = f.read()
#    f.close()

# lexer.input(s)
# for tok in lexer:
# print(tok)

#    if parser.parse(s,lexer = lexer) == "complete":
#        print("El programa es valido")
#    else:
#        print("El programa es invalido")
# except:
#    print("El programa es invalido")
