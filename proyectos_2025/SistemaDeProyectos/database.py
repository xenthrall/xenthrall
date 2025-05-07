import mysql.connector

"""
Asocia una materia a un profesor.

:param id_profesor: ID del profesor
:param id_materia: ID de la materia
:return: Tupla (nombre, apellido) o None si no existe
"""

db_name = "SistemaDeProyectos"

def conectar_db():
    """
    retorna dos instancias de conexion:

    :return: ""conn""  
    ejemplos de uso
    conn.commit() para guardar  cambios
    conn.close() para cerrar  la conexion
    :return: ""cursor""  ejemplos de uso
    cursor para ejecutar declaraciones y capturar datos

    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Inthesky1@",
        database=db_name
    )
   
    cursor = conn.cursor()
    conn.commit()

    return conn, cursor


"""
TABLE tareas (
    id_tarea INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT,
    estado VARCHAR(30),
    fecha_inicio DATE,
    fecha_fin DATE,
    id_proyecto INT,
    id_empleado INT,
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto),
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);
"""
class Tarea:
    """
    :param nombre: nombre del empleado
    :param correo: correo del empleado
    :param: 
    __init__(self,id_proyecto, id_empleado, fecha_inicio, fecha_fin, descripcion = None, estado = None, id_tarea = None):

    :returns:
    obtenertodos()
    id, descripcion, estado, fecha_inicio, fecha_fin, id_proyecto, id_empleado


    
    """
    def __init__(self,id_proyecto, id_empleado, fecha_inicio, fecha_fin = None, descripcion = None, estado = None, id_tarea = None):
        self.id_tarea = id_tarea
        self.descripcion = descripcion
        self.estado = estado
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.id_proyecto = id_proyecto
        self.id_empleado = id_empleado


    def guardar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "INSERT INTO tareas (descripcion, estado, fecha_inicio, fecha_fin, id_proyecto, id_empleado) VALUES (%s, %s, %s, %s, %s, %s)"
            valores = (self.descripcion, self.estado, self.fecha_inicio, self.fecha_fin, self.id_proyecto, self.id_empleado)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    @staticmethod
    def actualizar_registro(estado, fecha_fin, id_tarea):
        """
        parametros estado fecha_fin, id_tarea
        """
        conn, cursor = conectar_db()
        if conn:
            sql = "UPDATE tareas SET estado=%s, fecha_fin=%s WHERE id_tarea=%s"
            valores = (estado, fecha_fin, id_tarea)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    @staticmethod
    def eliminar_registro(id):
        conn, cursor = conectar_db()
        if conn:
            sql = "DELETE FROM tareas WHERE id_tarea=%s"
            valores = (id,)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    @staticmethod
    def obtener_todos():
        conn, cursor = conectar_db()
        if conn:
            cursor.execute("SELECT * FROM tareas")
            resultados = cursor.fetchall()
            conn.close()
        return resultados
    

    @staticmethod
    def obtener_por_id_proyecto(id_proyecto):
        """
        Objetivo:Filtrar proyectos por id.

        Args:
            (id_proyecto).

        Returns:
            Lista: de .
        """
        conn, cursor = conectar_db()

        sql = "SELECT * FROM tareas WHERE id_tarea=%s"
        valores = (id_proyecto,)
        cursor.execute(sql, valores)
        resultado = cursor.fetchall()
        conn.close()
        return resultado


"""
TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100),
    telefono VARCHAR(20)
);
"""

class Empleados:
    """
    :param nombre: nombre del empleado
    :param correo: correo del empleado
    :param: 
    __init__(self, nombre, correo = None, telefono = None, id_empleado = None):


    
    """
    def __init__(self, nombre, correo = None, telefono = None, id_empleado = None):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono


    def guardar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "INSERT INTO empleados (nombre, correo, telefono) VALUES (%s, %s, %s)"
            valores = (self.nombre, self.correo, self.telefono)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    def actualizar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "UPDATE empleados SET nombre=%s, correo=%s, telefono=%s WHERE id_empleado=%s"
            valores = (self.nombre, self.correo, self.telefono, self.id_empleado)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    @staticmethod
    def eliminar_registro(id):
        conn, cursor = conectar_db()
        if conn:
            sql = "DELETE FROM empleados WHERE id_empleado=%s"
            valores = (id,)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    @staticmethod
    def obtener_todos():
        conn, cursor = conectar_db()
        if conn:
            cursor.execute("SELECT * FROM empleados")
            resultados = cursor.fetchall()
            conn.close()
        return resultados
    

    @staticmethod
    def obtener_por_id_proyecto(id_proyecto):
        """
        Objetivo:Filtrar proyectos por id.

        Args:
            (id_proyecto).

        Returns:
            Lista: de .
        """
        conn, cursor = conectar_db()

        sql = "SELECT * FROM proyectos WHERE id_proyecto=%s"
        valores = (id_proyecto,)
        cursor.execute(sql, valores)
        resultado = cursor.fetchall()
        conn.close()
        return resultado



"""
TABLE proyectos (
    id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE
)
"""

class Proyecto:
    """
    :param nombre: nombre del proyecto
    :param descripcion: descripcion del proyecto
    :param: 
    __init__(self, nombre, descripcion, fecha_inicio, fecha_fin, id_proyecto = None):


    
    """
    def __init__(self, nombre, descripcion, fecha_inicio, fecha_fin = None, id_proyecto = None):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin


    def guardar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "INSERT INTO proyectos (nombre, descripcion, fecha_inicio, fecha_fin) VALUES (%s, %s, %s, %s)"
            valores = (self.nombre, self.descripcion, self.fecha_inicio, self.fecha_fin)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    def actualizar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "UPDATE proyectos SET nombre=%s, descripcion=%s, fecha_inicio=%s, fecha_fin=%s WHERE id_proyecto=%s"
            valores = (self.nombre, self.descripcion, self.fecha_inicio, self.fecha_fin, self.id_proyecto)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    @staticmethod
    def eliminar_registro(id):
        conn, cursor = conectar_db()
        if conn:
            sql = "DELETE FROM proyectos WHERE id_proyecto=%s"
            valores = (id,)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    @staticmethod
    def obtener_todos():
        conn, cursor = conectar_db()
        proyectos = []
        if conn:
            cursor.execute("SELECT * FROM proyectos")
            resultados = cursor.fetchall()
            conn.close()
        return resultados
    

    @staticmethod
    def obtener_por_id_proyecto(id_proyecto):
        """
        Objetivo:Filtrar proyectos por id.

        Args:
            (id_proyecto).

        Returns:
            Lista: de .
        """
        conn, cursor = conectar_db()

        sql = "SELECT * FROM proyectos WHERE id_proyecto=%s"
        valores = (id_proyecto,)
        cursor.execute(sql, valores)
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    

