import sqlite3
import os

# Nombre del archivo de la base de datos
DB_NAME = "colegio_db.sqlite"
# Ruta completa al archivo de la base de datos en la raíz del proyecto
# __file__ se refiere al archivo actual (donde se ejecuta este código)

def conectar_db():
    """
    Crea la conexión a la base de datos y activa las claves foráneas.
    Returns:
        tuple: (conn, cursor) si la conexión es exitosa, de lo contrario (None, None).
    """
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("PRAGMA foreign_keys = ON;") # Habilitar claves foráneas
        cursor = conn.cursor()
        # No imprimimos aquí para evitar mensajes repetitivos desde execute_query
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        if conn:
            conn.close()
        return None, None

def execute_query(query, params=None):
    """
    Ejecuta una consulta en la base de datos.
    Abre y cierra la conexión para cada consulta.
    """
    conn, cursor = conectar_db()
    if not conn or not cursor:
        print("No se pudo conectar a la base de datos para ejecutar la consulta.")
        return False # Indicar fallo

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        # print(f"Consulta ejecutada exitosamente: {query[:60]}...") # Opcional para depuración
        return True # Indicar éxito
    except sqlite3.Error as e:
        print(f"Error ejecutando la consulta: {e}")
        print(f"Consulta: {query}")
        if conn:
            conn.rollback() # Revertir cambios en caso de error
        return False # Indicar fallo
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            # print("Conexión cerrada tras ejecutar consulta.") # Opcional para depuración

# -----------------------------------
# * Definición de Tablas para COLEGIO
# -----------------------------------

def crear_tabla_curso():
    """Crea la tabla 'curso' si no existe."""
    query = """
    CREATE TABLE IF NOT EXISTS curso (
        id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT
    );
    """
    if execute_query(query):
        print("Tabla 'curso' verificada/creada.")

def crear_tabla_estudiante():
    """Crea la tabla 'estudiante' si no existe."""
    query = """
    CREATE TABLE IF NOT EXISTS estudiante (
        id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        fecha_nacimiento TEXT, -- Formato YYYY-MM-DD
        direccion TEXT,
        telefono TEXT,
        email TEXT UNIQUE,
        id_curso INTEGER,
        FOREIGN KEY (id_curso) REFERENCES curso(id_curso) ON DELETE CASCADE
    );
    """
    if execute_query(query):
        print("Tabla 'estudiante' verificada/creada.")

def crear_tabla_materia():
    """Crea la tabla 'materia' si no existe."""
    query = """
    CREATE TABLE IF NOT EXISTS materia (
        id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_materia TEXT NOT NULL UNIQUE,
        descripcion TEXT
    );
    """
    if execute_query(query):
        print("Tabla 'materia' verificada/creada.")

def crear_tabla_profesor():
    """Crea la tabla 'profesor' si no existe."""
    query = """
    CREATE TABLE IF NOT EXISTS profesor (
        id_profesor INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        email TEXT UNIQUE,
        telefono TEXT
    );
    """
    if execute_query(query):
        print("Tabla 'profesor' verificada/creada.")

def crear_tabla_profesor_materia():
    """Crea la tabla 'profesor_materia' (relación muchos a muchos) si no existe."""
    query = """
    CREATE TABLE IF NOT EXISTS profesor_materia (
        id_profesor INTEGER,
        id_materia INTEGER,
        PRIMARY KEY (id_profesor, id_materia),
        FOREIGN KEY (id_profesor) REFERENCES profesor(id_profesor) ON DELETE CASCADE,
        FOREIGN KEY (id_materia) REFERENCES materia(id_materia) ON DELETE CASCADE
    );
    """
    if execute_query(query):
        print("Tabla 'profesor_materia' verificada/creada.")

def crear_tabla_asistencia():
    """Crea la tabla 'asistencia' si no existe."""
    query = """
    CREATE TABLE IF NOT EXISTS asistencia (
        id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
        id_estudiante INTEGER,
        fecha TEXT NOT NULL, -- Formato YYYY-MM-DD
        estado_asistencia TEXT DEFAULT 'Presente'
        CHECK(estado_asistencia IN ('Presente', 'Ausente', 'Tarde')),
        FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante) ON DELETE CASCADE
    );
    """
    if execute_query(query):
        print("Tabla 'asistencia' verificada/creada.")

def crear_tabla_notas():
    """Crea la tabla 'notas' si no existe."""
    query = """
    CREATE TABLE IF NOT EXISTS notas (
        id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
        id_estudiante INTEGER,
        id_materia INTEGER,
        nota REAL NOT NULL CHECK(nota >= 0 AND nota <= 100), -- Ajusta la escala si es necesario
        fecha TEXT NOT NULL, -- Formato YYYY-MM-DD
        FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante) ON DELETE CASCADE,
        FOREIGN KEY (id_materia) REFERENCES materia(id_materia) ON DELETE CASCADE
    );
    """
    if execute_query(query):
        print("Tabla 'notas' verificada/creada.")

#----------------------
# Función para crear todas las tablas
#----------------------

def crear_todas_las_tablas_colegio():
    """Ejecuta todas las funciones para crear las tablas del colegio, en orden de dependencia."""
    print("Iniciando creación/verificación de tablas para la base de datos del colegio...")

    # Tablas sin dependencias directas o dependencias básicas
    crear_tabla_curso()
    crear_tabla_materia()
    crear_tabla_profesor()

    # Tablas que dependen de las anteriores
    crear_tabla_estudiante() # Depende de 'curso'
    crear_tabla_profesor_materia() # Depende de 'profesor' y 'materia'

    # Tablas que dependen de 'estudiante' y/o 'materia'
    crear_tabla_asistencia() # Depende de 'estudiante'
    crear_tabla_notas() # Depende de 'estudiante' y 'materia'

    print("Proceso de creación/verificación de tablas completado.")


def inicializar_db_colegio():
    """
    Inicializa la base de datos del colegio.
    Si el archivo de la BD no existe, crea todas las tablas.
    Si ya existe, simplemente informa que ya está presente.
    """
    # Verificar si la BD existe es implícito, ya que sqlite3.connect la crea si no está.
    # Lo importante es asegurarse que las tablas estén allí.
    # En este modelo, `execute_query` no devuelve el cursor directamente,
    # así que no podemos simplemente pasar conn y cursor como en la primera versión.
    # Por eso, `crear_todas_las_tablas_colegio` llama a las funciones que usan `execute_query`.

    # La primera vez que se ejecute, connect_db() creará el archivo si no existe.
    # Luego, crear_todas_las_tablas_colegio() se asegurará de que las tablas existan.
    if not os.path.exists(DB_NAME):
        print(f"Base de datos '{DB_NAME}' no encontrada en '{DB_NAME}'. Creando y configurando tablas...")
        crear_todas_las_tablas_colegio()
        # Aquí podrías añadir funciones para poblar datos iniciales si es necesario
        # Ejemplo: poblar_cursos_iniciales()
    else:
        print(f"Base de datos '{DB_NAME}' ya existente en '{DB_NAME}'. Verificando/creando tablas si es necesario...")
        # Aunque la BD exista, las tablas podrían no estar.
        # `CREATE TABLE IF NOT EXISTS` se encarga de esto.
        crear_todas_las_tablas_colegio()

if __name__ == "__main__":

    inicializar_db_colegio()
    print("Inicialización de la base de datos del colegio finalizada.")