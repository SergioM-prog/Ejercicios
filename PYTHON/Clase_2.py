# pruebaDicc: dict[str,int|str|dict|list]= {
#     "x":7,
#     "y":"hola",
#     "a": {"b":3},
#     "z": [1,2,"hola"],
# }
# # 1-------------------------

# if type(pruebaDicc) == dict:
#     print("apruebas 1")
# else: print("suspendes 1")

# # 2-------------------------

# if pruebaDicc["x"] ==7:
#     print("apruebas 2")
# else:print("suspendes 2")

# # 3-------------------------

# if pruebaDicc["y"] =="hola":
#     print("apruebas 3")
# else:print("suspendes 3")

# # 4-------------------------

# if pruebaDicc["a"]["b"] == 3:
#     print("apruebas 4")
# else: print("suspendes 4")

# # 5-------------------------

# if pruebaDicc["z"][1] == 2:
#     print("apruebas 5")
# else:print("suspendes 5")

# # 6-------------------------

# if type(pruebaDicc["z"][2]) == str:
#     print("apruebas 6")
# else:print("suspendes 6")

# # -------------------------

# ----------------------BUCLES---------------------------

# productos = [
#   {"nombre": "Laptop", "categoria": "Electrónica", "precio": 799.99, "stock": 25},
#   {"nombre": "Auriculares Bluetooth", "categoria": "Accesorios", "precio": 59.99, "stock": 50},
#   {"nombre": "Cámara Digital", "categoria": "Fotografía", "precio": 399.99, "stock": 10},
#   {"nombre": "Smartwatch", "categoria": "Relojes", "precio": 149.99, "stock": 75},
#   {"nombre": "Teclado Mecánico", "categoria": "Accesorios", "precio": 89.99, "stock": 30}
#  ]

# # for producto in productos:
# #     print(producto["nombre"])

# # contador = 0
# # while contador <= len(productos) -1:
# #     print(productos[contador]["nombre"])
# #     contador +=1

# # -------------------------

# # for producto in productos:
# #      if producto["precio"] >100:
# #         print(producto["nombre"])

# # contador = 0
# # while contador <= len(productos) -1:
# #     if productos[contador]["precio"] >100:
# #         print(productos[contador]["nombre"])
# #     contador +=1

# # -------------------------

# # for producto in productos:
# #     if producto["stock"] <=25:
# #         print(producto["nombre"])

# # contador = 0
# # while contador <= len(productos) -1:
# #     if productos[contador]["stock"] <=25:
# #         print(productos[contador]["nombre"])
# #     contador +=1


# ----------------------FUNCIONES---------------------------


# def sum(a, b):
#     return a + b

# print(sum(2,2))

# # def frase():
# #     return "Hola"

# # print(frase())

# def saludar(nombre):
#     return f"Hola {nombre}"

# print(saludar("Sergio"))

# def cuenta_caracteres(palabra):

#     if type(palabra)!=str:
#         return "Debe ser ejecutada con un string"
#     else: return len(palabra)

# print(cuenta_caracteres(1))

# def cuenta_caracteres(palabra):

#     if type(palabra) == str:
#         return len(palabra)
#     else: return "Debe ser ejecutada con un string"

# print(cuenta_caracteres("Hola"))

# funcion_letra = lambda texto: texto[0]

# print(funcion_letra("Hola"))

# def obtener_nombre_completo(nombre, apellido):
#     return nombre + " " + apellido

# def main():
#     usuarios = [
#         {"nombre": "Sofía", "apellido": "Martínez"},
#         {"nombre": "Luis", "apellido": "Martínez"},
#     ]
   
#     for usuario in usuarios:
#         completo = obtener_nombre_completo(usuario["nombre"], usuario["apellido"])
#         print(completo)

# main()


