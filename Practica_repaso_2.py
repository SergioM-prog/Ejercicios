gente = [
    {"nombre": "Jamiro", "edad": 45},
    {"nombre": "Juan",   "edad": 35},
    {"nombre": "Paco",   "edad": 34},
    {"nombre": "Pepe",   "edad": 14},
    {"nombre": "Pilar",  "edad": 24},
    {"nombre": "Laura",  "edad": 24},
    {"nombre": "Jenny",  "edad": 10},
]

# Nivel 1 – Bucles
# 1. Crea una lista con la gente que su nombre tiene 4 letras.

# lista_nombres = []
# for a in gente:
#     if len(a["nombre"]) == 4:
#         lista_nombres.append(a["nombre"])
# print(lista_nombres)



# Crea una lista con la gente que su nombre empieza por J y sean menores de 40 años.

# lista_nombres = []
# for a in gente:
#     if a["nombre"][0] == "J" and a["edad"]<40:
#         lista_nombres.append(a["nombre"])
# print(lista_nombres)

# Nivel 2 – Funciones
# Crea una función resta que espere dos parámetros a y b y que devuelva la resta de los mismos.

# valor_a = int(input("Introduce el valor de a: "))
# valor_b = int(input("Introduce el valor de b: "))

# def funcion_resta(a,b):
#     c = a - b
#     return c

# print(funcion_resta(valor_a,valor_b))


# Crea la función duplicaNumero debe recibir un tipo number y devolver el doble del valor recibido. Si la función no recibe un dato tipo number debe devolver el string ‘Debo ser ejecutada con un número’

# valor_a = input("Introduce el valor a duplicar: ")

# def fun_duplicar_num(a):

#     if type(a) == int:
#         return a *2
#     else:
#         return "Debo ser ejecutada con un número"
    
# print(fun_duplicar_num(valor_a))



# Crea la función ultimoCaracter debe recibir un tipo string y devolver un string con el último carácter.
# Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'.
# Si recibe un string vacío debe devolver 'Debo ser ejecutada con un string no vacío'


# def fun_ultimo_caracter():
#     var_ultimo_caracter = input("Introduce la palabra: ")

#     if type(var_ultimo_caracter) == str: return str(var_ultimo_caracter[-1])
#     else: return "Debo ser ejecutada con un string"

# print(fun_ultimo_caracter())



# Crea la función cuentaCaracteres debe recibir un tipo string y devolver un number con el número de carácteres
# Si la función no recibe un dato tipo string debe devolver el string 'Debo ser ejecutada con un string'


def fun_cuenta_caract(cadena):

    if type(cadena) == str:
        return len(cadena)
    else:
        return "Debo ser ejecutada con un string"
    
print(fun_cuenta_caract("Hola"))
print(fun_cuenta_caract(1))