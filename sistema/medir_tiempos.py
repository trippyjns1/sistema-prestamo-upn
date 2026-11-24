# MEDIR TIEMPOS: prueba de rendimiento del sistema con muchos libros
# Crea datos ficticios en memoria (no toca la carpeta datos) y mide
# cuanto tardan las operaciones principales con 100, 1000, 2000 y 5000 libros.

import time
from gestion import SistemaPrestamos
from entidades import Libro


def crear_sistema(cantidad):
    # Crea un sistema con 'cantidad' libros y 1 estudiante
    sistema = SistemaPrestamos()
    for i in range(cantidad, 0, -1):  # en orden inverso, el peor caso para ordenar
        sistema.libros.append(Libro(f"LIB{i:05d}", f"Titulo {i:05d}", "Autor"))
    sistema.registrar_estudiante("N00000001", "Estudiante Prueba")
    return sistema


def medir(funcion):
    # Devuelve el tiempo en milisegundos que tarda la funcion
    inicio = time.perf_counter()
    funcion()
    return (time.perf_counter() - inicio) * 1000


print(f"{'LIBROS':<8} {'BUSCAR (ms)':<12} {'PRESTAMO (ms)':<14} {'BURBUJA (ms)':<13} {'SELECCION (ms)':<15} {'RECURSIVO (ms)':<14}")
for cantidad in [100, 1000, 2000, 5000]:
    sistema = crear_sistema(cantidad)
    ultimo = f"LIB{1:05d}"  # esta al final de la lista: peor caso de busqueda
    t_buscar = medir(lambda: sistema.buscar_libro(ultimo))
    t_prestamo = medir(lambda: sistema.registrar_prestamo("N00000001", ultimo, 7))
    t_burbuja = medir(sistema.ordenar_por_titulo)
    t_seleccion = medir(sistema.ordenar_por_codigo)
    t_recursivo = medir(sistema.contar_disponibles)
    print(f"{cantidad:<8} {t_buscar:<12.3f} {t_prestamo:<14.3f} {t_burbuja:<13.1f} {t_seleccion:<15.1f} {t_recursivo:<14.3f}")
