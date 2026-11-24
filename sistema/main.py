# ============================================================
#  SISTEMA DE PRÉSTAMO DE LIBROS - BIBLIOTECA UPN
#  Curso: Fundamentos de Programación (CIIN1205P) - Equipo 4
#  Versión: 2.0.0
#  main.py: menu principal (formulario de consola)
# ============================================================

from gestion import SistemaPrestamos, DIAS_MAXIMOS
from utilidades import (leer_entero, leer_codigo, leer_texto, confirmar,
                        codigo_libro_valido, codigo_estudiante_valido, mostrar_resultado)

VERSION = "2.0.0"


# ---------------- Opciones de libros ----------------

def opcion_registrar_libro(sistema):
    print("\n-- Registrar Libro --")
    codigo = leer_codigo("Código del libro (ej. LIB001): ")
    if not codigo_libro_valido(codigo):
        mostrar_resultado(False, "El código debe tener la forma LIB + números (ej. LIB001).")
        return
    if sistema.buscar_libro(codigo) is not None:
        mostrar_resultado(False, "Código duplicado: ese libro ya está registrado.")
        return
    titulo = leer_texto("Título: ")
    autor = leer_texto("Autor: ")
    mostrar_resultado(*sistema.registrar_libro(codigo, titulo, autor))


def opcion_buscar_libro(sistema):
    print("\n-- Buscar Libro --")
    print(" 1. Por código")
    print(" 2. Por título")
    tipo = leer_entero("Elija: ", 1, 2)
    if tipo == 1:
        libro = sistema.buscar_libro(leer_codigo("Código del libro: "))
        if libro is None:
            mostrar_resultado(False, "Libro no registrado.")
        else:
            libro.mostrar()
    else:
        encontrados = sistema.buscar_por_titulo(leer_texto("Texto a buscar en el título: "))
        if len(encontrados) == 0:
            mostrar_resultado(False, "No se encontraron libros con ese texto.")
        else:
            mostrar_libros(encontrados)


def mostrar_libros(lista):
    # Se reutiliza para listar, buscar y ordenar
    if len(lista) == 0:
        print("No hay libros registrados.")
        return
    print(f"\n{'CÓDIGO':<8} {'TÍTULO':<32} {'AUTOR':<20} ESTADO")
    for libro in lista:
        libro.mostrar()


def opcion_modificar_libro(sistema):
    print("\n-- Modificar Libro --")
    codigo = leer_codigo("Código del libro: ")
    libro = sistema.buscar_libro(codigo)
    if libro is None:
        mostrar_resultado(False, "Libro no registrado.")
        return
    titulo = input(f"Nuevo título [{libro.titulo}]: ").strip().replace(";", ",")
    autor = input(f"Nuevo autor [{libro.autor}]: ").strip().replace(";", ",")
    mostrar_resultado(*sistema.modificar_libro(codigo, titulo, autor))


def opcion_eliminar_libro(sistema):
    print("\n-- Eliminar Libro --")
    codigo = leer_codigo("Código del libro: ")
    libro = sistema.buscar_libro(codigo)
    if libro is not None and libro.disponible:
        if not confirmar(f"¿Seguro que desea eliminar '{libro.titulo}'?"):
            print("Operación cancelada.")
            return
    mostrar_resultado(*sistema.eliminar_libro(codigo))


# ---------------- Opciones de estudiantes ----------------

def opcion_registrar_estudiante(sistema):
    print("\n-- Registrar Estudiante --")
    codigo = leer_codigo("Código del estudiante (ej. N00123456): ")
    if not codigo_estudiante_valido(codigo):
        mostrar_resultado(False, "El código debe ser N + 8 números (ej. N00123456).")
        return
    if sistema.buscar_estudiante(codigo) is not None:
        mostrar_resultado(False, "Ese estudiante ya está registrado.")
        return
    nombre = leer_texto("Nombre completo: ")
    mostrar_resultado(*sistema.registrar_estudiante(codigo, nombre))


def opcion_listar_estudiantes(sistema):
    if len(sistema.estudiantes) == 0:
        print("No hay estudiantes registrados.")
        return
    print(f"\n{'CÓDIGO':<12} NOMBRE")
    for estudiante in sistema.estudiantes:
        estudiante.mostrar()


# ---------------- Opciones de prestamos ----------------

def opcion_registrar_prestamo(sistema):
    print("\n-- Registrar Préstamo --")
    codigo_estudiante = leer_codigo("Código del estudiante: ")
    codigo_libro = leer_codigo("Código del libro: ")
    # Primero se validan las reglas; solo si todo esta bien se piden los dias
    valido, mensaje = sistema.validar_prestamo(codigo_estudiante, codigo_libro)
    if not valido:
        mostrar_resultado(False, mensaje)
        return
    dias = leer_entero(f"Cantidad de días (1 a {DIAS_MAXIMOS}): ", 1, DIAS_MAXIMOS)
    mostrar_resultado(*sistema.registrar_prestamo(codigo_estudiante, codigo_libro, dias))


def opcion_devolucion(sistema):
    print("\n-- Registrar Devolución --")
    codigo_estudiante = leer_codigo("Código del estudiante: ")
    codigo_libro = leer_codigo("Código del libro: ")
    mostrar_resultado(*sistema.registrar_devolucion(codigo_estudiante, codigo_libro))


def opcion_extender(sistema):
    print("\n-- Extender Préstamo --")
    codigo_estudiante = leer_codigo("Código del estudiante: ")
    codigo_libro = leer_codigo("Código del libro: ")
    prestamo = sistema.buscar_prestamo_activo(codigo_estudiante, codigo_libro)
    if prestamo is None:
        mostrar_resultado(False, "No existe un préstamo activo con esos datos.")
        return
    disponible = sistema.dias_disponibles(prestamo)
    if disponible <= 0:
        mostrar_resultado(False, f"El préstamo ya tiene el máximo de {DIAS_MAXIMOS} días.")
        return
    extra = leer_entero(f"Días adicionales (1 a {disponible}): ", 1, disponible)
    mostrar_resultado(*sistema.extender_prestamo(prestamo, extra))


def mostrar_prestamos(lista, titulo):
    # Sirve para los prestamos activos y para el historial
    print(f"\n-- {titulo} --")
    if len(lista) == 0:
        print("No hay registros.")
        return
    print(f"{'N°':<4} {'ESTUDIANTE':<12} {'LIBRO':<8} {'DÍAS':<5} ESTADO")
    for prestamo in lista:
        prestamo.mostrar()


# ---------------- Reportes ----------------

def opcion_mas_prestados(sistema):
    print("\n-- Libros más prestados (arreglos paralelos) --")
    codigos, titulos, cantidades = sistema.reporte_mas_prestados()
    if len(codigos) == 0:
        print("No hay libros registrados.")
        return
    print(f"{'CÓDIGO':<8} {'TÍTULO':<32} VECES")
    for i in range(len(codigos)):
        print(f"{codigos[i]:<8} {titulos[i]:<32} {cantidades[i]}")


def opcion_estadisticas(sistema):
    print("\n-- Estadísticas (calculadas con recursividad) --")
    disponibles = sistema.contar_disponibles()
    print(f"Total de libros:           {len(sistema.libros)}")
    print(f"  Disponibles:             {disponibles}")
    print(f"  Prestados:               {len(sistema.libros) - disponibles}")
    print(f"Total de estudiantes:      {len(sistema.estudiantes)}")
    print(f"Préstamos activos:         {len(sistema.prestamos_activos)}")
    print(f"Días prestados en total:   {sistema.sumar_dias_prestados()}")
    print(f"Préstamos devueltos:       {len(sistema.historial)}")


# ---------------- Menu principal ----------------

def mostrar_menu():
    print("\n==================================================")
    print(f"   SISTEMA DE PRÉSTAMO DE LIBROS UPN  v{VERSION}")
    print("==================================================")
    print(" LIBROS                     PRÉSTAMOS")
    print(" 1. Registrar libro          8. Registrar préstamo")
    print(" 2. Buscar libro             9. Registrar devolución")
    print(" 3. Listar libros           10. Extender préstamo")
    print(" 4. Modificar libro         11. Ver préstamos activos")
    print(" 5. Eliminar libro          12. Ver historial")
    print(" ESTUDIANTES                REPORTES")
    print(" 6. Registrar estudiante    13. Ordenar por título (Burbuja)")
    print(" 7. Listar estudiantes      14. Ordenar por código (Selección)")
    print("                            15. Libros más prestados")
    print("                            16. Estadísticas")
    print(" 17. Cargar datos de ejemplo    0. Salir")


def main():
    # Se crea el objeto principal del sistema y se cargan los archivos
    sistema = SistemaPrestamos()
    errores = sistema.cargar_datos()
    if errores > 0:
        print(f"Aviso: se ignoraron {errores} líneas dañadas en los archivos de datos.")

    while True:
        mostrar_menu()
        opcion = leer_entero("Seleccione una opción: ", 0, 17)

        if opcion == 1:
            opcion_registrar_libro(sistema)
        elif opcion == 2:
            opcion_buscar_libro(sistema)
        elif opcion == 3:
            mostrar_libros(sistema.libros)
        elif opcion == 4:
            opcion_modificar_libro(sistema)
        elif opcion == 5:
            opcion_eliminar_libro(sistema)
        elif opcion == 6:
            opcion_registrar_estudiante(sistema)
        elif opcion == 7:
            opcion_listar_estudiantes(sistema)
        elif opcion == 8:
            opcion_registrar_prestamo(sistema)
        elif opcion == 9:
            opcion_devolucion(sistema)
        elif opcion == 10:
            opcion_extender(sistema)
        elif opcion == 11:
            mostrar_prestamos(sistema.prestamos_activos, "Préstamos Activos")
        elif opcion == 12:
            mostrar_prestamos(sistema.historial, "Historial de Préstamos")
        elif opcion == 13:
            print("\nLibros ordenados por título (Burbuja):")
            mostrar_libros(sistema.ordenar_por_titulo())
        elif opcion == 14:
            print("\nLibros ordenados por código (Selección):")
            mostrar_libros(sistema.ordenar_por_codigo())
        elif opcion == 15:
            opcion_mas_prestados(sistema)
        elif opcion == 16:
            opcion_estadisticas(sistema)
        elif opcion == 17:
            sistema.cargar_datos_ejemplo()
            mostrar_resultado(True, "Datos de ejemplo cargados (son ficticios).")
        elif opcion == 0:
            if confirmar("¿Desea salir del sistema?"):
                sistema.guardar_datos()
                print("Datos guardados. ¡Hasta luego!")
                break

        sistema.guardar_datos()  # se guarda despues de cada operacion


if __name__ == "__main__":
    main()
