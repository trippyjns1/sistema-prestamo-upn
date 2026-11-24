# Sistema de Préstamo de Libros – Biblioteca UPN

Proyecto del curso **Fundamentos de Programación (CIIN1205P)** – Universidad Privada del Norte, Equipo 4.

Sistema de consola en Python para registrar libros y estudiantes, gestionar préstamos, devoluciones y extensiones, y guardar la información en archivos de texto.

## Integrantes

- Gomez Valle, Mathias Nicolas
- Barrientos Sánchez, Ailish Damaris
- Jurado Castillo, Mikjael
- Natividad Infante, Jhader
- Livia Tello, Jesus Alexander

## Cómo ejecutarlo

Requiere Python 3. Desde la carpeta del proyecto:

```
cd sistema
python main.py
```

La primera vez no hay datos: use la opción **17** para cargar datos de ejemplo (ficticios). Los datos se guardan en la carpeta `sistema/datos/`.

## Estructura

```
sistema/
├── main.py        # Menú principal (formulario de consola). Crea el objeto SistemaPrestamos y llama a sus métodos
├── entidades.py   # Clases Libro, Estudiante y Prestamo
├── gestion.py     # Clase SistemaPrestamos: reglas del negocio, CRUD, ordenamientos, reportes y recursividad
├── utilidades.py  # Funciones reutilizables para pedir y validar datos
├── archivos.py    # Guardar y leer archivos .txt
├── medir_tiempos.py # Mide el tiempo de las operaciones con 100 a 5000 libros
└── datos/         # libros.txt, estudiantes.txt, prestamos.txt, historial.txt (se crea sola)
```

## Temas del curso aplicados

| Tema | Dónde se aplica |
| --- | --- |
| 01 Control de versiones y estructuras | Git/GitHub con ramas; `if/elif`, `while`, `for` en todo el sistema |
| 02 Funciones y modularidad | Funciones con parámetros y retorno; 5 módulos |
| 03 Arreglos | Listas de objetos, CRUD, Burbuja (`ordenar_por_titulo`) y Selección (`ordenar_por_codigo`) |
| 04 Cadenas y arreglos paralelos | `split`, `replace`, `find`, `upper`, `title`, slicing; búsqueda por título y por autor; reporte de libros más prestados con 3 listas paralelas |
| 05 Persistencia | Archivos `.txt` con datos separados por `;` |
| 06 Programación modular y reutilización | Entidades / gestión / formulario; funciones de `utilidades.py` usadas en todo el menú |
| 07 Recursividad | `contar_disponibles()` y `sumar_dias_prestados()` |

## Reglas del sistema

- Máximo **30 días** por préstamo (incluidas las extensiones).
- Máximo **3 libros** prestados a la vez por estudiante.
- No se puede eliminar un libro que está prestado.

## Repositorio y ramas

- `main`: versión estable del sistema.
- `tema-04-busqueda-autor`: búsqueda de libros por autor (métodos de cadenas).
- `docs-readme`: documentación del proyecto.
- `analisis-tiempos`: script para medir el rendimiento del sistema.
