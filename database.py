import sqlite3

DB_NAME = "notas.db"


def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asignaturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cortes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asignatura_id INTEGER NOT NULL,
            numero INTEGER NOT NULL,
            porcentaje REAL NOT NULL DEFAULT 0,
            FOREIGN KEY (asignatura_id) REFERENCES asignaturas (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            corte_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            porcentaje REAL NOT NULL,
            nota REAL NOT NULL,
            FOREIGN KEY (corte_id) REFERENCES cortes (id)
        )
    """)

    conexion.commit()
    conexion.close()


def crear_asignatura(nombre):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO asignaturas (nombre) VALUES (?)", (nombre,))
    asignatura_id = cursor.lastrowid

    for numero_corte in (1, 2, 3):
        cursor.execute(
            "INSERT INTO cortes (asignatura_id, numero, porcentaje) VALUES (?, ?, ?)",
            (asignatura_id, numero_corte, 0)
        )

    conexion.commit()
    conexion.close()
    return asignatura_id


def obtener_asignaturas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM asignaturas ORDER BY nombre")
    filas = cursor.fetchall()
    conexion.close()
    return filas


def obtener_cortes(asignatura_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id, numero, porcentaje FROM cortes WHERE asignatura_id = ? ORDER BY numero",
        (asignatura_id,)
    )
    filas = cursor.fetchall()
    conexion.close()
    return filas


def actualizar_porcentaje_corte(corte_id, porcentaje):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE cortes SET porcentaje = ? WHERE id = ?",
        (porcentaje, corte_id)
    )
    conexion.commit()
    conexion.close()


def crear_actividad(corte_id, nombre, porcentaje, nota):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO actividades (corte_id, nombre, porcentaje, nota) VALUES (?, ?, ?, ?)",
        (corte_id, nombre, porcentaje, nota)
    )
    conexion.commit()
    conexion.close()


def obtener_actividades(corte_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id, nombre, porcentaje, nota FROM actividades WHERE corte_id = ?",
        (corte_id,)
    )
    filas = cursor.fetchall()
    conexion.close()
    return filas