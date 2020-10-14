'''
tipo = typeOperator['int']['int']['+']
if tipo is "bool":
    ERROR
'''
# Cubo semantico para conocer el resultado de operaciones
typeOperator = {
    "int": {
        "int": {
            "+": "int",
            "-": "int",
            "*": "int",
            "/": "int",
            "=": "int",
            ">": "bool",
            "<": "bool",
            ">=": "bool",
            "<=": "bool",
            "==": "bool",
            "&": "bool",
            "|": "bool"
        },
        "float": {
            "+": "float",
            "-": "float",
            "*": "float",
            "/": "float",
            "=": None,
            ">": "bool",
            "<": "bool",
            ">=": "bool",
            "<=": "bool",
            "==": "bool",
            "&": "bool",
            "|": "bool"
        },
        "char": {
            "+": None,
            "-": None,
            "*": None,
            "/": None,
            "=": None,
            ">": None,
            "<": None,
            ">=": None,
            "<=": None,
            "==": None,
            "&": None,
            "|": None
        },
        "bool": {
            "+": None,
            "-": None,
            "*": None,
            "/": None,
            "=": None,
            ">": None,
            "<": None,
            ">=": None,
            "<=": None,
            "==": None,
            "&": None,
            "|": None
        }
    },
    "float": {
        "int": {
            "+": "float",
            "-": "float",
            "*": "float",
            "/": "float",
            "=": None,
            ">": "bool",
            "<": "bool",
            ">=": "bool",
            "<=": "bool",
            "==": "bool",
            "&": "bool",
            "|": "bool"
        },
        "float": {
            "+": "float",
            "-": "float",
            "*": "float",
            "/": "float",
            "=": "float",
            ">": "bool",
            "<": "bool",
            ">=": "bool",
            "<=": "bool",
            "==": "bool",
            "&": "bool",
            "|": "bool"
        },
        "char": {
            "+": None,
            "-": None,
            "*": None,
            "/": None,
            "=": None,
            ">": None,
            "<": None,
            ">=": None,
            "<=": None,
            "==": None,
            "&": None,
            "|": None
        },
        "bool": {
            "+": None,
            "-": None,
            "*": None,
            "/": None,
            "=": None,
            ">": None,
            "<": None,
            ">=": None,
            "<=": None,
            "==": None,
            "&": None,
            "|": None
        }
    },
    "char": {
        "int": {
            "+": None,
            "-": None,
            "*": None,
            "/": None,
            "=": None,
            ">": None,
            "<": None,
            ">=": None,
            "<=": None,
            "==": None,
            "&": "bool",
            "|": "bool"
        },
        "float": {
            "+": None,
            "-": None,
            "*": None,
            "/": None,
            "=": None,
            ">": None,
            "<": None,
            ">=": None,
            "<=": None,
            "==": None,
            "&": "bool",
            "|": "bool"
        },
        "char": {
            "+": None,
            "-": None,
            "*": None,
            "/": None,
            "=": "char",
            ">": None,
            "<": None,
            ">=": None,
            "<=": None,
            "==": "bool",
            "&": "bool",
            "|": "bool"
        },
        "bool": {
            "+": None,
            "-": None,
            "*": None,
            "/": None,
            "=": None,
            ">": None,
            "<": None,
            ">=": None,
            "<=": None,
            "==": None,
            "&": "bool",
            "|": "bool"
        }
    },
    "bool": {
        "int": {
            "+": None,
            "-": None,
            "*": None,
            "/": None,
            "=": None,
            ">": None,
            "<": None,
            ">=": None,
            "<=": None,
            "==": None,
            "&": None,
            "|": None
        },
        "float": {
            "+": None,
            "-": None,
            "*": None,
            "/": None,
            ">": None,
            "<": None,
            ">=": None,
            "<=": None,
            "==": None,
            "&": None,
            "|": None
        },
        "char": {
            "+": None,
            "-": None,
            "*": None,
            "/": None,
            ">": None,
            "<": None,
            ">=": None,
            "<=": None,
            "==": None,
            "&": "bool",
            "|": "bool"
        },
        "bool": {
            "+": "bool",
            "-": "bool",
            "*": "bool",
            "/": "bool",
            "=": "bool",
            ">": "bool",
            "<": "bool",
            ">=": "bool",
            "<=": "bool",
            "==": "bool",
            "&": "bool",
            "|": "bool"
        }
    }
}


def ReturnType(opA, opB, operator):
    return typeOperator[opA][opB][operator]
