import sys

mem_size = 10000
int_b = 0
float_b = 10000
char_b = 20000
bool_b = 30000

# Counters
int_counter = 0
float_counter = 0
char_counter = 0
bool_counter = 0
cte_counter = 0

class Memory:
  # constructor, initializes all in 0, false or empty
  def __init__(self, i, f, c, b):
    self.ints = []
    self.floats = []
    self.chars = []
    self.bools = []

    counter = 0

    while (counter < i):
      self.ints.append(0)
      counter += 1
    counter = 0

    while (counter < f):
      self.floats.append(0)
      counter += 1
    counter = 0

    while (counter < c):
      self.chars.append('')
      counter += 1
    counter = 0

    while (counter < b):
      self.bools.append(False)
      counter += 1
    counter = 0

  # To Do
  # Borrar este metodo
  # representacion del objeto de cualquier expresion valida de python
  def __repr__(self):
    return "Integer:% s Float:% s Char:% s Bools:% s" % (self.ints, self.floats, self.chars, self.bools)

  def update(self, address, val):
    var_type = int(address / 10000) % 10
    if var_type == 0:
      self.ints[address % 10000] = val
    elif var_type == 1:
      self.floats[address % 10000] = val
    elif var_type == 2:
      self.chars[address % 10000] = val
    elif var_type == 3:
      self.bools[address % 10000] = val
    else:
      print("Error en manejo de memoria")
      sys.exit()

  def get_type(self, address):
    if (int(address) / 10000) % 10 < 1:
      return 'int'
    elif (int(address) / 10000) % 10 < 2:
      return 'float'
    elif (int(address) / 10000) % 10 < 3:
      return 'char'
    elif (int(address) / 10000) % 10 < 4:
      return 'bool'
    else:
      print("Error en manejo de memoria")
      sys.exit()

  # To Do
  # Cambie algo de esto así que puede que falle
  def get_val(self, address):
    var_type = int(address / 10000) % 10
    if var_type == 0:
      return self.ints[address % 10000]
    elif var_type == 1:
      return self.floats[address % 10000]
    elif var_type == 2:
      return self.chars[address % 10000]
    elif var_type == 3:
      return self.bools[address % 10000]
    else:
      print("Error en manejo de memoria")
      sys.exit()
