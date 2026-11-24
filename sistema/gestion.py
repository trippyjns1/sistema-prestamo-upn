# GESTION: clase SistemaPrestamos, que maneja las listas y las reglas del negocio
# Los metodos devuelven (True/False, mensaje) y el menu decide que mostrar

from entidades import Libro, Estudiante, Prestamo
from archivos import guardar_lineas, leer_lineas

DIAS_MAXIMOS = 30  # maximo de dias que puede durar un prestamo
MAX_PRESTAMOS = 3  # maximo de libros prestados a la vez por estudiante


class SistemaPrestamos:

    def __init__(self):
        # Listas (arreglos) donde se guardan los objetos del sistema
        self.libros = []
        self.estudiantes = []
        self.prestamos_activos = []
        self.historial = []
        self.siguiente_id = 1

    # ---------------- Busquedas ----------------

    def buscar_libro(self, codigo):
        # Busqueda secuencial: recorre la lista hasta encontrar el codigo
        for libro in self.libros:
            if libro.codigo == codigo:
                return libro
        return None

    def buscar_estudiante(self, codigo):
        for estudiante in self.estudiantes:
            if estudiante.codigo == codigo:
                return estudiante
        return None

    def buscar_por_titulo(self, texto):
        # Busqueda por nombre: devuelve los libros cuyo titulo contiene el texto
        # find() devuelve la posicion del texto o -1 si no lo encuentra (como IndexOf)
        encontrados = []
        for libro in self.libros:
            if libro.titulo.lower().find(texto.lower()) != -1:
                encontrados.append(libro)
        return encontrados

    def buscar_por_autor(self, texto):
        # Igual que la busqueda por titulo, pero revisando el autor
        encontrados = []
        for libro in self.libros:
            if libro.autor.lower().find(texto.lower()) != -1:
                encontrados.append(libro)
        return encontrados

    def buscar_prestamo_activo(self, codigo_estudiante, codigo_libro):
        for prestamo in self.prestamos_activos:
            if prestamo.codigo_estudiante == codigo_estudiante and prestamo.codigo_libro == codigo_libro:
                return prestamo
        return None

    # ---------------- CRUD de libros ----------------

    def registrar_libro(self, codigo, titulo, autor):
        if self.buscar_libro(codigo) is not None:
            return False, "Código duplicado: ese libro ya está registrado."
        self.libros.append(Libro(codigo, titulo, autor))
        return True, "Libro registrado correctamente."

    def modificar_libro(self, codigo, titulo, autor):
        libro = self.buscar_libro(codigo)
        if libro is None:
            return False, "Libro no registrado."
        # Si se deja vacio, se mantiene el dato actual
        if titulo != "":
            libro.titulo = titulo
        if autor != "":
            libro.autor = autor
        return True, "Libro modificado correctamente."

    def eliminar_libro(self, codigo):
        libro = self.buscar_libro(codigo)
        if libro is None:
            return False, "Libro no registrado."
        if not libro.disponible:
            return False, "Solo se pueden eliminar libros disponibles (este está prestado)."
        self.libros.remove(libro)
        return True, "Libro eliminado."

    # ---------------- Estudiantes ----------------

    def registrar_estudiante(self, codigo, nombre):
        if self.buscar_estudiante(codigo) is not None:
            return False, "Ese estudiante ya está registrado."
        # title() pone en mayuscula la primera letra de cada palabra
        self.estudiantes.append(Estudiante(codigo, nombre.title()))
        return True, "Estudiante registrado correctamente."

    # ---------------- Prestamos ----------------

    def contar_prestamos(self, codigo_estudiante):
        # Cuenta cuantos libros tiene prestados un estudiante
        cantidad = 0
        for prestamo in self.prestamos_activos:
            if prestamo.codigo_estudiante == codigo_estudiante:
                cantidad = cantidad + 1
        return cantidad

    def validar_prestamo(self, codigo_estudiante, codigo_libro):
        # Revisa todas las reglas antes de pedir los dias
        if self.buscar_estudiante(codigo_estudiante) is None:
            return False, "Estudiante no registrado."
        if self.contar_prestamos(codigo_estudiante) >= MAX_PRESTAMOS:
            return False, f"El estudiante ya tiene {MAX_PRESTAMOS} libros prestados. Debe devolver uno primero."
        libro = self.buscar_libro(codigo_libro)
        if libro is None:
            return False, "Libro no registrado."
        if not libro.disponible:
            return False, "El libro no está disponible."
        return True, "Préstamo válido."

    def registrar_prestamo(self, codigo_estudiante, codigo_libro, dias):
        valido, mensaje = self.validar_prestamo(codigo_estudiante, codigo_libro)
        if not valido:
            return False, mensaje
        prestamo = Prestamo(self.siguiente_id, codigo_estudiante, codigo_libro, dias)
        self.prestamos_activos.append(prestamo)
        self.buscar_libro(codigo_libro).prestar()
        self.siguiente_id = self.siguiente_id + 1
        return True, f"Préstamo registrado. Número de operación: {prestamo.id_prestamo}"

    def registrar_devolucion(self, codigo_estudiante, codigo_libro):
        prestamo = self.buscar_prestamo_activo(codigo_estudiante, codigo_libro)
        if prestamo is None:
            return False, "No existe un préstamo activo con esos datos."
        libro = self.buscar_libro(codigo_libro)
        if libro is not None:
            libro.devolver()
        prestamo.finalizar()
        self.prestamos_activos.remove(prestamo)
        self.historial.append(prestamo)
        return True, "Devolución registrada. El libro vuelve a estar disponible."

    def dias_disponibles(self, prestamo):
        # Cuantos dias se pueden agregar sin pasar el maximo
        return DIAS_MAXIMOS - prestamo.dias

    def extender_prestamo(self, prestamo, dias_extra):
        if dias_extra > self.dias_disponibles(prestamo):
            return False, f"El préstamo no puede pasar de {DIAS_MAXIMOS} días."
        prestamo.extender(dias_extra)
        return True, f"Préstamo extendido. Ahora tiene {prestamo.dias} días."

    # ---------------- Ordenamientos ----------------

    def ordenar_por_titulo(self):
        # Metodo Burbuja: compara vecinos y los intercambia si estan en desorden
        copia = self.libros.copy()
        n = len(copia)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                if copia[j].titulo.lower() > copia[j + 1].titulo.lower():
                    copia[j], copia[j + 1] = copia[j + 1], copia[j]
        return copia

    def ordenar_por_codigo(self):
        # Metodo Seleccion: busca el menor y lo pone al inicio
        copia = self.libros.copy()
        n = len(copia)
        for i in range(n - 1):
            menor = i
            for j in range(i + 1, n):
                if copia[j].codigo < copia[menor].codigo:
                    menor = j
            copia[i], copia[menor] = copia[menor], copia[i]
        return copia

    # ---------------- Arreglos paralelos ----------------

    def reporte_mas_prestados(self):
        # Tres listas paralelas: la posicion i de cada una es del mismo libro
        codigos = []
        titulos = []
        cantidades = []
        for libro in self.libros:
            codigos.append(libro.codigo)
            titulos.append(libro.titulo)
            cantidades.append(libro.veces_prestado)

        # Burbuja de mayor a menor; al intercambiar movemos las tres listas juntas
        n = len(cantidades)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                if cantidades[j] < cantidades[j + 1]:
                    cantidades[j], cantidades[j + 1] = cantidades[j + 1], cantidades[j]
                    codigos[j], codigos[j + 1] = codigos[j + 1], codigos[j]
                    titulos[j], titulos[j + 1] = titulos[j + 1], titulos[j]
        return codigos, titulos, cantidades

    # ---------------- Recursividad ----------------

    def contar_disponibles(self, inicio=0, fin=None):
        # Cuenta los libros disponibles dividiendo la lista en dos mitades
        # (divide y venceras); asi soporta miles de libros sin llenar la memoria
        if fin is None:
            fin = len(self.libros)
        # Caso base 1: tramo vacio
        if fin - inicio == 0:
            return 0
        # Caso base 2: tramo de un solo libro
        if fin - inicio == 1:
            if self.libros[inicio].disponible:
                return 1
            return 0
        # Caso recursivo: contar la mitad izquierda + la mitad derecha
        mitad = (inicio + fin) // 2
        return self.contar_disponibles(inicio, mitad) + self.contar_disponibles(mitad, fin)

    def sumar_dias_prestados(self, inicio=0, fin=None):
        # Suma recursiva de los dias de todos los prestamos activos (misma idea)
        if fin is None:
            fin = len(self.prestamos_activos)
        if fin - inicio == 0:
            return 0
        if fin - inicio == 1:
            return self.prestamos_activos[inicio].dias
        mitad = (inicio + fin) // 2
        return self.sumar_dias_prestados(inicio, mitad) + self.sumar_dias_prestados(mitad, fin)

    # ---------------- Archivos ----------------

    def guardar_datos(self):
        guardar_lineas("libros.txt", self.libros)
        guardar_lineas("estudiantes.txt", self.estudiantes)
        guardar_lineas("prestamos.txt", self.prestamos_activos)
        guardar_lineas("historial.txt", self.historial)

    def cargar_datos(self):
        # Lee los archivos y vuelve a crear los objetos
        # Si una linea esta danada, se salta y se cuenta para avisar al usuario
        errores = 0
        for datos in leer_lineas("libros.txt"):
            try:
                self.libros.append(Libro(datos[0], datos[1], datos[2], datos[3] == "True", int(datos[4])))
            except (IndexError, ValueError):
                errores = errores + 1
        for datos in leer_lineas("estudiantes.txt"):
            try:
                self.estudiantes.append(Estudiante(datos[0], datos[1]))
            except IndexError:
                errores = errores + 1
        for nombre_archivo, lista in [("prestamos.txt", self.prestamos_activos), ("historial.txt", self.historial)]:
            for datos in leer_lineas(nombre_archivo):
                try:
                    lista.append(Prestamo(int(datos[0]), datos[1], datos[2], int(datos[3]), datos[4]))
                except (IndexError, ValueError):
                    errores = errores + 1
        # El siguiente numero de prestamo es el mayor guardado + 1
        for prestamo in self.prestamos_activos + self.historial:
            if prestamo.id_prestamo >= self.siguiente_id:
                self.siguiente_id = prestamo.id_prestamo + 1
        return errores

    def cargar_datos_ejemplo(self):
        # Datos ficticios para probar rapido el sistema
        ejemplos = [("LIB003", "Cálculo I", "James Stewart"),
                    ("LIB001", "Fundamentos de Programación", "Luis Joyanes"),
                    ("LIB002", "Base de Datos", "C. J. Date"),
                    ("LIB004", "Física I", "Raymond Serway")]
        for codigo, titulo, autor in ejemplos:
            self.registrar_libro(codigo, titulo, autor)
        self.registrar_estudiante("N00123456", "Estudiante A")
        self.registrar_estudiante("N00456789", "Estudiante B")
