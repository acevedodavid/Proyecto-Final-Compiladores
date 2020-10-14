import estructuraTabla
import sys

symbols = {}

symbols = {
    'main': {
        'param': {

        },
        'vars': {

        }
    }
}


# inicializar la tabla para funciones locales y las globales respectivamente
def addFunction(id, dataType):
    insert = estructuraTabla.tabla(dataType, {})
    if len(symbols) <= 0:
        symbols[id] = insert
    elif len(symbols) >= 1 and not sameNameFunc(id):
        symbols[id] = insert


# comprobar si existen funciones con el mismo nombre
def sameNameFunc(id):
    for Keys in symbols:
        if id == Keys:
            print("ERROR, Esta funcion ya fue declarada")
            sys.exit()
            return True
    return False

# comprobar si existen variables globales con el mismo nombre


def sameGlobalVar(id):
    if "global" in symbols.keys():
        for Keys in symbols["global"].value:
            if id == Keys:
                print("Error variable ya declarada")
                sys.exit()
                return True
        return False


# retornar typo de la variable
def variableType(id, function_id):
    type = symbols[function_id].value[id].dataType
    return type


# retornar valor de la variable
def variableValue(id, function_id):
    valor = symbols[function_id].value[id].value
    return valor
