# ENTIDADES: clases que representan los datos del sistema
# Cada clase tiene sus atributos (propiedades) y sus metodos


class Libro:
    # Representa un libro de la biblioteca

    def __init__(self, codigo, titulo, autor, disponible=True, veces_prestado=0):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.disponible = disponible
        self.veces_prestado = veces_prestado

    def prestar(self):
        # Marca el libro como prestado y suma una vez mas a su contador
        self.disponible = False
        self.veces_prestado = self.veces_prestado + 1

    def devolver(self):
        # El libro vuelve a estar disponible
        self.disponible = True

    def estado(self):
        if self.disponible:
            return "Disponible"
        return "Prestado"

    def mostrar(self):
        # Muestra el libro en una sola linea, con columnas alineadas
        print(f"{self.codigo:<8} {self.titulo:<32} {self.autor:<20} {self.estado()}")

    def a_linea(self):
        # Convierte el libro en una linea de texto para guardarlo en el archivo
        return f"{self.codigo};{self.titulo};{self.autor};{self.disponible};{self.veces_prestado}"


class Estudiante:
    # Representa a un estudiante que puede pedir libros

    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

    def mostrar(self):
        print(f"{self.codigo:<12} {self.nombre}")

    def a_linea(self):
        return f"{self.codigo};{self.nombre}"


class Prestamo:
    # Representa un prestamo de un libro a un estudiante

    def __init__(self, id_prestamo, codigo_estudiante, codigo_libro, dias, estado="Activo"):
        self.id_prestamo = id_prestamo
        self.codigo_estudiante = codigo_estudiante
        self.codigo_libro = codigo_libro
        self.dias = dias
        self.estado = estado

    def extender(self, dias_extra):
        # Suma dias al prestamo
        self.dias = self.dias + dias_extra

    def finalizar(self):
        # Marca el prestamo como devuelto
        self.estado = "Devuelto"

    def mostrar(self):
        print(f"{self.id_prestamo:<4} {self.codigo_estudiante:<12} {self.codigo_libro:<8} {self.dias:<5} {self.estado}")

    def a_linea(self):
        return f"{self.id_prestamo};{self.codigo_estudiante};{self.codigo_libro};{self.dias};{self.estado}"
