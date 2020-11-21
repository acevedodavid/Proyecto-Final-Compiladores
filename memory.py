import sys

mem_size = 10000
int_b = 0
float_b = 10000
char_b = 20000
bool_b = 30000

class Memory:
  # constructor, initializes all in 0, false or empty with enough space for all variables required by method
  def __init__(self, i, f, c, b):
    self.ints = [0] * i
    self.floats = [0] * f
    self.chars = [''] * c
    self.bools = [False] * b

  def __repr__(self):
    return "ints:% s floats:% s chars:% s bools:% s" % (self.ints, self.floats, self.chars, self.bools)

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
