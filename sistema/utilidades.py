# UTILIDADES: funciones reutilizables para pedir y validar datos
# Se usan desde el menu (main.py) en muchas opciones distintas


def leer_entero(mensaje, minimo, maximo=None):
    # Pide un numero entero y no deja avanzar hasta que sea valido
    while True:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print(" Debe ingresar un número entero.")
            continue
        if numero < minimo or (maximo is not None and numero > maximo):
            print(" Número fuera del rango permitido.")
        else:
            return numero


def leer_codigo(mensaje):
    # Pide un codigo y lo deja en mayusculas y sin espacios
    return input(mensaje).strip().upper().replace(" ", "")


def leer_texto(mensaje):
    # Pide un texto que no puede estar vacio
    texto = input(mensaje).strip()
    while texto == "":
        print(" Este dato no puede estar vacío.")
        texto = input(mensaje).strip()
    # El ; se usa para separar datos en los archivos, por eso lo reemplazamos
    return texto.replace(";", ",")


def confirmar(mensaje):
    # Pregunta S/N y devuelve True si la respuesta es S
    respuesta = input(mensaje + " (S/N): ").strip().upper()
    return respuesta == "S"


def codigo_libro_valido(codigo):
    # Un codigo de libro valido tiene la forma LIB + numeros (ej. LIB001)
    # codigo[:3] toma los 3 primeros caracteres (como Substring)
    return codigo[:3] == "LIB" and codigo[3:].isdigit()


def codigo_estudiante_valido(codigo):
    # Un codigo UPN empieza con N y luego 8 numeros (ej. N00123456)
    return len(codigo) == 9 and codigo.find("N") == 0 and codigo[1:].isdigit()


def mostrar_resultado(exito, mensaje):
    # Muestra el mensaje que devuelven los metodos del sistema
    if exito:
        print(" [OK] " + mensaje)
    else:
        print(" [X] " + mensaje)
