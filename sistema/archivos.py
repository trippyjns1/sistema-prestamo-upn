# ARCHIVOS: funciones para guardar y leer datos en archivos de texto (.txt)
# Cada linea del archivo es un registro y los datos se separan con ;
# Ejemplo de una linea de libros.txt:  LIB001;Fundamentos de Programación;Luis Joyanes;True;2

import os

# Carpeta "datos" que esta al lado de este archivo
CARPETA_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")


def ruta(nombre_archivo):
    # Devuelve la ruta completa de un archivo dentro de la carpeta datos
    return os.path.join(CARPETA_DATOS, nombre_archivo)


def guardar_lineas(nombre_archivo, objetos):
    # Escribe un objeto por linea usando su metodo a_linea()
    if not os.path.exists(CARPETA_DATOS):
        os.mkdir(CARPETA_DATOS)
    with open(ruta(nombre_archivo), "w", encoding="utf-8") as archivo:
        for objeto in objetos:
            archivo.write(objeto.a_linea() + "\n")


def leer_lineas(nombre_archivo):
    # Lee el archivo y devuelve una lista con los datos de cada linea ya separados
    registros = []
    if not os.path.exists(ruta(nombre_archivo)):
        return registros  # primera vez: el archivo todavia no existe
    with open(ruta(nombre_archivo), "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea != "":
                registros.append(linea.split(";"))
    return registros
