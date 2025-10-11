# lista_edades = [15, 22, 17, 30, 65, 45, 70, 19]

# # for edad in lista_edades:
# #     if edad >= 65:
# #         print("Edad mayor que 65, saliendo de bucle")
# #         break
# #     elif edad >= 18:
# #         print(f"Edad: {edad}")
# #     else: continue


# contador_intento = 0

# while contador_intento <5:

#     numero = input(f"Hola, introduce un número. Intento {contador_intento}: ")

#     try:
#         int(numero)
#         numero = int(numero)
#         print("Numero es valido")
#         contador_intento += 1
#         break

#     except:
#         print("El valor introducido no es un número")
#         numero = input(f"Hola, vuelve a introducir un número. Intento {contador_intento}: ")

    


# class Animal:
#     def __init__(self, nombre, edad):
#         self.nombre = nombre
#         self.edad = edad


class Producto:
    def __init__(self, nombre, unidades, pvp):
        self.nombre = nombre
        self.unidades = unidades
        self.pvp = pvp
    
    def mostrarDetalles(self):
        print(f"Nombre: {self.nombre}, Unidades: {self.unidades}, PVP: {self.pvp}")
    

# producto1 = Producto("Móvil", 10, 100)
# producto2 = Producto("Piano", 1, 1000)

# producto1.mostrarDetalles()
# producto2.mostraretalles()

# class Electrodomestico(Producto):
#     def __init__(self,nombre, unidades, pvp, marca):
#         super().__init__(nombre, unidades, pvp)
#         self.marca = marca
    
#     def encender(self):
#         print("Encendiendo...")

# nevera1 = Electrodomestico("Nevera1",100,1000,"Sony")
# nevera1.encender()


from Modulos.Saludos import saludar,despedir

saludar("Sergio")
despedir("Sergio")