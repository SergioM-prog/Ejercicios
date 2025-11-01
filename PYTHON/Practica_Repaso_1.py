gente = [
    {"nombre": "Jamiro", "edad": 45},
    {"nombre": "Juan",   "edad": 35},
    {"nombre": "Paco",   "edad": 34},
    {"nombre": "Pepe",   "edad": 14},
    {"nombre": "Pilar",  "edad": 24},
    {"nombre": "Laura",  "edad": 24},
    {"nombre": "Jenny",  "edad": 10},
]

# #### Nivel 1 – Condiciones simples
# 1. Mayoría de edad (uno): Crea una variable p = gente[3] y muestra "mayor" si p["edad"] >= 18, si no "menor".
# 2. Empieza por J: Con p = gente[1], muestra "empieza por J" si su nombre empieza por "J", si no "no empieza por J".
# 3. Nombre de 4 letras: Con p = gente[2], muestra "4 letras" si len(p["nombre"]) == 4, si no "otra longitud".
# 4. CEdad par/impar: Con p = gente[4], muestra "par" si p["edad"] % 2 == 0, si no "impar".
# 5. Termina en “o”: Con p = gente[0], muestra "termina en o" si p["nombre"].endswith("o"), si no "no termina en o".

# 1.
# p = gente[3]
# if p["edad"] >= 18:
#     print("mayor")
# else: print("menor")

# 2.
# p = gente[1]
# if p["nombre"][0] == "J":
#     print("empieza por J")
# else: print("no empieza por J")

# 3.
# p = gente[2]
# if len(p["nombre"]) == 4:
#     print("4 letras")
# else: print("Otra longitud")

#4

# p = gente[4]
# if p["edad"] % 2 == 0:
#     print("Par")
# else: print("Impar")

#5

# p = gente[0]
# if p["nombre"][-1] == "o":
#     print("termina en o")
# else: print("no termina en o")

# p = gente[0]
# if p["nombre"].endswith("o") == True:
#     print("termina en o")
# else: print("no termina en o")


# #### Nivel 2 – if/else + lógicos

# 1. J y menor de 40: Con p = gente[1], muestra "J y <40" si nombre empieza por J y edad < 40, si no "no cumple".
# 2. A o a (sin distinguir mayúsculas): Con p = gente[5], muestra "contiene a" si "a" in p["nombre"].lower(), si no "no contiene a".
# 3. Entre 20 y 35 (ambos inclusive): Con p = gente[4], muestra "rango 20-35" si 20 <= edad <= 35, si no "fuera de rango"."
# 4. No J y mayor de 30: Con p = gente[2], muestra "no J y >30" si no empieza por J y edad > 30, si no "no cumple".
# 5. Dos condiciones alternativas: Con p = gente[0], muestra "o J o <= 24" si empieza por J o su edad es <= 24, si no "no cumple".

# 1.

# p = gente[1]
# if p["nombre"][0] == "J" and p["edad"] < 40:
#     print("J y <40")
# else: print("no cumple")

# 2.

# p = gente[5]
# if "a" in p["nombre"].lower():
#     print("contiene a")
# else: print("no contiene a")

# 3.

# p = gente[4]
# if 20 <= p["edad"] <= 35:
#     print("rango 20-35")
# else: print("fuera de rango")

# 4.

# p = gente[2]
# if p["nombre"][0] != "J" and p["edad"] > 30:
#     print("no J y >30")
# else: print("no cumple")

# 5.

# p = gente[1]
# if p["nombre"][0] == "J" or p["edad"] <= 24:
#     print("o J o <= 24")
# else: print("no cumple")







# #### Nivel 4 – Comparaciones entre 2–3 personas
# 1. Mayor entre dos: Compara a = gente[1] y b = gente[2]; imprime el nombre del mayor. Si empatan, imprime "empate".
# 2. Más largo/ corto (nombre): Con a = gente[5] y b = gente[4], imprime "a más largo", "b más largo" o "igual longitud".
# 3. El mayor de tres (solo ifs): Compara a = gente[0], b = gente[1], c = gente[2] y muestra el nombre del de mayor edad usando solo if/elif/else (sin max).

# 1.

# a = gente[2]
# b = gente[3]

# if a["edad"] > b["edad"]:
#     print("Gana a: " + a["nombre"])

# elif a["edad"] < b["edad"]:
#     print("Gana b: " + b["nombre"])

# else:
#     print("Empate")

# 2.

# a = gente[5]
# b = gente[4]

# if len(a["nombre"]) > len(b["nombre"]):
#     print("a más largo")

# elif len(a["nombre"]) < len(b["nombre"]):
#     print("b más largo")

# else:
#     print("igual longitud")

# 3.

# a = gente[3]
# b = gente[4]
# c = gente[5]

# if a["edad"] > b["edad"]:

#     if a["edad"] > c["edad"]:
#         print("Gana a: " + a["nombre"])

#     elif c["edad"] > b["edad"]:
#         print("Gana c: " + c["nombre"])

#     else: print("Gana b: " + b["nombre"])

# else: print("Empate")




# ------------SOLUCIÓN---------------------


# gente = [
#     {"nombre": "Jamiro", "edad": 45},
#     {"nombre": "Juan",   "edad": 35},
#     {"nombre": "Paco",   "edad": 34},
#     {"nombre": "Pepe",   "edad": 14},
#     {"nombre": "Pilar",  "edad": 24},
#     {"nombre": "Laura",  "edad": 24},
#     {"nombre": "Jenny",  "edad": 10},
# ]

# # 1) Mayoría de edad (uno)
# p = gente[3]
# if p["edad"] >= 18:
#     print("1) mayor")
# else:
#     print("1) menor")

# # 2) Empieza por J
# p = gente[1]
# if p["nombre"].startswith("J"):
#     print("2) empieza por J")
# else:
#     print("2) no empieza por J")

# # 3) Nombre de 4 letras
# p = gente[2]
# if len(p["nombre"]) == 4:
#     print("3) 4 letras")
# else:
#     print("3) otra longitud")

# # 4) Edad par/impar
# p = gente[4]
# if p["edad"] % 2 == 0:
#     print("4) par")
# else:
#     print("4) impar")

# # 5) Termina en “o”
# p = gente[0]
# if p["nombre"].endswith("o"):
#     print("5) termina en o")
# else:
#     print("5) no termina en o")

# # 6) J y menor de 40
# p = gente[1]
# if p["nombre"].startswith("J") and p["edad"] < 40:
#     print("6) J y <40")
# else:
#     print("6) no cumple")

# # 7) Contiene 'a' (case-insensitive)
# p = gente[5]
# if "a" in p["nombre"].lower():
#     print("7) contiene a")
# else:
#     print("7) no contiene a")

# # 8) Entre 20 y 35 (ambos inclusive)
# p = gente[4]
# if 20 <= p["edad"] <= 35:
#     print("8) rango 20-35")
# else:
#     print("8) fuera de rango")

# # 9) No J y mayor de 30
# p = gente[2]
# if not p["nombre"].startswith("J") and p["edad"] > 30:
#     print("9) no J y >30")
# else:
#     print("9) no cumple")

# # 10) O empieza por J O edad <= 24
# p = gente[0]
# if p["nombre"].startswith("J") or p["edad"] <= 24:
#     print("10) o J o <= 24")
# else:
#     print("10) no cumple")

# # 11) Clasifica por edad
# p = gente[3]
# if p["edad"] < 12:
#     print("11) niño")
# elif 12 <= p["edad"] <= 17:
#     print("11) adolescente")
# else:
#     print("11) adulto")

# # 12) Etiqueta por longitud de nombre
# p = gente[6]
# ln = len(p["nombre"])
# if ln == 4:
#     print("12) cuatro letras")
# elif ln == 5:
#     print("12) cinco")
# else:
#     print("12) otra")

# # 13) Tarifa por tramo de edad
# p = gente[4]
# if p["edad"] < 14:
#     tarifa = "infantil"
# elif 14 <= p["edad"] <= 25:
#     tarifa = "joven"
# elif 26 <= p["edad"] <= 64:
#     tarifa = "adulto"
# else:
#     tarifa = "senior"
# print(f"13) tarifa: {tarifa}")

# # 14) Mayor entre dos (con empate)
# a = gente[1]  # Juan 35
# b = gente[2]  # Paco 34
# if a["edad"] > b["edad"]:
#     print(f"14) mayor: {a['nombre']}")
# elif b["edad"] > a["edad"]:
#     print(f"14) mayor: {b['nombre']}")
# else:
#     print("14) empate")

# # 15) Más largo/corto (nombre)
# a = gente[5]  # Laura
# b = gente[4]  # Pilar
# if len(a["nombre"]) > len(b["nombre"]):
#     print("15) a más largo")
# elif len(b["nombre"]) > len(a["nombre"]):
#     print("15) b más largo")
# else:
#     print("15) igual longitud")

# # 16) El mayor de tres (elige uno en empates)
# a = gente[0]  # Jamiro 45
# b = gente[1]  # Juan   35
# c = gente[2]  # Paco   34
# if a["edad"] >= b["edad"] and a["edad"] >= c["edad"]:
#     print(f"16) mayor: {a['nombre']}")
# elif b["edad"] >= a["edad"] and b["edad"] >= c["edad"]:
#     print(f"16) mayor: {b['nombre']}")
# else:
#     print(f"16) mayor: {c['nombre']}")
