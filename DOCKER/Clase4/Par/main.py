import sys

def fun_resta():
    if len(sys.argv) != 2:                                                              #sys.argv es una lista que contiene: [0] Nombre del script main.py [1] y [2] Los argumentos que le pases (En este caso 2 argumentos)
        print("Has introducido más de 1 argumento, por favor vuelve a intentarlo.")
        sys.exit(1)

    try:
        num1 = int(sys.argv[1])
        if num1%2 == 0: print("“Es par”")
        else: print("“Este número no es par”")
    except ValueError:
        print("Por favor, introduce un número válido.")
        sys.exit(1)

if __name__ == "__main__":                                                              # Al ejecutar main.py Python asigna el valor especial "__main__" a la variable interna __name__
    fun_resta()