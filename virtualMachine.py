import memory
import sys

# Addresses bases
const_b = 0
global_b = 100000
local_b = 200000

mem_size = 10000
int_b = 0
float_b = 10000
char_b = 20000
bool_b = 30000

symbols = []
quadruples = []
constants = []

ip = []  # Sirve para regresar de la funcion
current_function = []  # Sirve para saber la funcion actual
param_list = {}  # Guardo los parametros de la funcion
returnArray = []

# To do
# Checar que los tipos de datos se manejen bien (se guarden como fload, entero, etc...)

# Revisa que el al momento de corre_programar se envio un objeto
if len(sys.argv) != 2:
  print('ERROR, no se pudo detectar el archivo')
  raise SyntaxError('Necesitas enviar un archivo .txto correcto')
else:
  data = sys.argv[1]
  with open(data, 'r', newline='\n') as file:
    output_file = eval(file.read())
    symbols = output_file['symbols']
    quadruples = output_file['quadruples']
    constants = output_file['constants']

# Init new space of local memory in the stack
def initFunctionMemory(function):
  global symbols, local_memory,current_function
  lc = symbols[function]['count'] # gets count from the given function
  local_memory.append(memory.Memory(lc['int'],lc['float'],lc['char'],lc['bool'])) # creates new instance of memory with space necessary for given function and pushes it to stack
  current_function.append(function)

# Aux variables
gc = symbols['global']['count'] # global count
cc = constants['count'] # constant count

# Create memory instances only with required addresses
global_memory = memory.Memory(gc['int'],gc['float'],gc['char'],gc['bool'])
constant_memory = memory.Memory(cc['int'],cc['float'],cc['char'],cc['bool'])
# Function calls' stack
local_memory = []

# Copy constant values to constant memory
for key, value in constants['data'].items():
  constant_memory.update(value['address'],key)

# Init local_memory stack with main
initFunctionMemory('main')

######### HASTA AQUI ESTA TODO CM #########

def get_val(address):
  memory_type = (int(address / 100000)) % 10
  if memory_type == 0:
    #constant
    return constant_memory.get_val(address)
  elif memory_type == 1:
    # global
    return global_memory.get_val(address)
  elif memory_type == 2:
    # local
    return local_memory[-1].get_val(address)
  else:
    print("Error en get_value")
    sys.exit()
  return 0

def get_type(address):
  var_type = int(address / 10000) % 10
  if var_type == 0:
    return 'int'
  elif var_type == 1:
    return 'float'
  elif var_type == 2:
    return 'char'
  elif var_type == 3:
    return 'bool'
  else:
    print("Error en get_type")
    sys.exit()

def update(address, val):
  memory_type = (int(address / 100000)) % 10
  if memory_type == 0:
    #constant
    constant_memory.update(address, val)
  elif memory_type == 1:
    # global
    global_memory.update(address, val)
  elif memory_type == 2:
    # local
    local_memory[-1].update(address, val)
  else:
    print("Error en update_value")
    sys.exit()

# Iterate through quadruples
def run(quad, pointer):
  #print("\nrun")
  #print(quad)

  global param_list, current_function

  if quad[0] == 'GOTO':
    return quad[3]

  if quad[0] == 'GOTOF':
    #print(get_val(quad[1]))
    if (get_val(quad[1])):
      return pointer + 1
    else:
      return quad[3]
      #print(quad[3])

  # To Do
  # Checar que el siguiente paso sea pointer + 1
  if quad[0] == 'ERA':
    initFunctionMemory(quad[3])
    return pointer + 1

  # To Do
  # Checar bien como se hace esta
  if quad[0] == 'gosub':
    ip.append(pointer + 1)
    #print(param_list)
    for key, val in param_list.items():
      update(key,val)
      #local_memory[-1].update(key,val)
    param_list = {}
    #print(symbols[quad[3]]['start'])
    #sys.exit()
    return symbols[quad[3]]['start']

  if quad[0] == 'param':
    param_list[quad[3]] = get_val(quad[1])
    #print(param_list)
    return pointer + 1

  if quad[0] == 'return':
    #print("return")
    address = symbols['global']['vars'][current_function[-1]]['address']
    #print(address)
    update(address, get_val(quad[3]))
    #sys.exit()
    return pointer + 1

  if quad[0] == 'ENDFunc':
    local_memory.pop()
    current_function.pop()
    return ip.pop()

  if quad[0] == '=':
    operand_val = get_val(quad[1])
    update(quad[3],operand_val)
    return pointer + 1

  if quad[0] == '+':
    left_operand = get_val(quad[1])
    right_operand = get_val(quad[2])
    update(quad[3],left_operand + right_operand)
    return pointer + 1

  if quad[0] == '-':
    left_operand = get_val(quad[1])
    right_operand = get_val(quad[2])
    update(quad[3],left_operand - right_operand)
    return pointer + 1

  if quad[0] == '*':
    left_operand = get_val(quad[1])
    right_operand = get_val(quad[2])
    update(quad[3],left_operand * right_operand)
    return pointer + 1

  if quad[0] == '/':
    left_operand = get_val(quad[1])
    right_operand = get_val(quad[2])
    result = left_operand / right_operand
    if (get_type(left_operand) == 'int' and get_type(left_operand) == 'int'):
      result = int(result)
    update(quad[3],result)
    return pointer + 1

  if quad[0] == '>':
    left_operand = get_val(quad[1])
    right_operand = get_val(quad[2])
    update(quad[3],left_operand > right_operand)
    return pointer + 1

  if quad[0] == '<':
    left_operand = get_val(quad[1])
    right_operand = get_val(quad[2])
    update(quad[3],left_operand < right_operand)
    return pointer + 1

  if quad[0] == '==':
    left_operand = get_val(quad[1])
    right_operand = get_val(quad[2])
    update(quad[3],left_operand == right_operand)
    return pointer + 1

  if quad[0] == '|':
    left_operand = get_val(quad[1])
    right_operand = get_val(quad[2])
    update(quad[3],left_operand or right_operand)
    return pointer + 1

  if quad[0] == '&':
    left_operand = get_val(quad[1])
    right_operand = get_val(quad[2])
    update(quad[3],left_operand and right_operand)
    return pointer + 1

  if quad[0] == 'write':
    #print(quad[3])
    print(get_val(quad[3]))
    return pointer + 1

  # To Do
  # Checar que el input sea valido
  if quad[0] == 'read':
    aux = input()
    update(quad[3],aux)
    return pointer + 1

  if quad[0] == 'End':
    return pointer + 1


pointer = 0
#print(constants)
#print(constant_memory)
while (pointer < len(quadruples)):
    # Se envia a la funcion el cuadruplo y su indice
    #print(quadruples[pointer])
    pointer = run(quadruples[pointer], pointer)
    #print("Constant memory " + str(constant_memory))
    #print("Global memory " + str(global_memory))
    #if (local_memory[-1] is not None):
    #  print(local_memory[-1])
