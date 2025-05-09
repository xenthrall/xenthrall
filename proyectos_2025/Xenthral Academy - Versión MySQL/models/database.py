import mysql.connector
from datetime import date

db_name = "colegio"

def conectar_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xenthrall1@",
        database=db_name
    )
    cursor = conn.cursor()

    return conn, cursor


def execute_query(query):
    conn, cursor = conectar_db()
    cursor.execute(query)

    lista = cursor.fetchall()
    conn.close()

    return lista


class Reportes:
    """
    Clase para generar diferentes reportes del sistema escolar.
    """
    @staticmethod
    def reporte_inscripcion_cursos():
        """
        Retorna el número de estudiantes inscritos en cada curso.
        :return: Lista de tuplas (id_curso, nombre_curso, total_estudiantes)
        """
        conn, cursor = conectar_db()
        try:
            sql = (
                "SELECT c.id_curso, c.nombre, COUNT(e.id_estudiante) "
                "FROM curso c "
                "LEFT JOIN estudiante e ON c.id_curso = e.id_curso "
                "GROUP BY c.id_curso, c.nombre"
            )
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def reporte_asistencia_por_estudiante(id_estudiante: int, fecha_inicio: date = None, fecha_fin: date = None):
        """
        Retorna conteo de estados de asistencia ('Presente','Ausente','Tarde') para un estudiante
        en un rango de fechas opcional.
        :return: Diccionario {estado: conteo}
        """
        conn, cursor = conectar_db()
        try:
            params = [id_estudiante]
            sql = (
                "SELECT estado_asistencia, COUNT(*) "
                "FROM asistencia WHERE id_estudiante = %s"
            )
            if fecha_inicio:
                sql += " AND fecha >= %s"
                params.append(fecha_inicio)
            if fecha_fin:
                sql += " AND fecha <= %s"
                params.append(fecha_fin)
            sql += " GROUP BY estado_asistencia"
            cursor.execute(sql, tuple(params))
            return {row[0]: row[1] for row in cursor.fetchall()}
        finally:
            conn.close()

    @staticmethod
    def reporte_asistencia_por_curso(id_curso: int, fecha_inicio: date = None, fecha_fin: date = None):
        """
        Retorna resumen de asistencia por curso (agrupado por estado).
        :return: Diccionario {estado: conteo}
        """
        conn, cursor = conectar_db()
        try:
            params = [id_curso]
            sql = (
                "SELECT a.estado_asistencia, COUNT(*) "
                "FROM asistencia a "
                "JOIN estudiante e ON a.id_estudiante = e.id_estudiante "
                "WHERE e.id_curso = %s"
            )
            if fecha_inicio:
                sql += " AND a.fecha >= %s"
                params.append(fecha_inicio)
            if fecha_fin:
                sql += " AND a.fecha <= %s"
                params.append(fecha_fin)
            sql += " GROUP BY a.estado_asistencia"
            cursor.execute(sql, tuple(params))
            return {row[0]: row[1] for row in cursor.fetchall()}
        finally:
            conn.close()

    @staticmethod
    def reporte_promedio_notas_por_estudiante(id_estudiante: int):
        """
        Retorna el promedio de notas de un estudiante por materia.
        :return: Lista de tuplas (id_materia, promedio_nota)
        """
        conn, cursor = conectar_db()
        try:
            sql = (
                "SELECT n.id_materia, AVG(n.nota) "
                "FROM notas n "
                "WHERE n.id_estudiante = %s "
                "GROUP BY n.id_materia"
            )
            cursor.execute(sql, (id_estudiante,))
            return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def reporte_promedio_notas_por_materia(id_materia: int):
        """
        Retorna el promedio de notas de todos los estudiantes en una materia.
        :return: Float promedio
        """
        conn, cursor = conectar_db()
        try:
            sql = "SELECT AVG(nota) FROM notas WHERE id_materia = %s"
            cursor.execute(sql, (id_materia,))
            return cursor.fetchone()[0]
        finally:
            conn.close()

    @staticmethod
    def reporte_estadisticas_notas_por_curso(id_curso: int):
        """
        Retorna promedio, nota máxima y mínima por curso.
        :return: Lista de tuplas (id_materia, avg, min, max)
        """
        conn, cursor = conectar_db()
        try:
            sql = (
                "SELECT n.id_materia, AVG(n.nota), MIN(n.nota), MAX(n.nota) "
                "FROM notas n "
                "JOIN estudiante e ON n.id_estudiante = e.id_estudiante "
                "WHERE e.id_curso = %s "
                "GROUP BY n.id_materia"
            )
            cursor.execute(sql, (id_curso,))
            return cursor.fetchall()
        finally:
            conn.close()


class Asistencia:
    """
    Clase para gestionar la asistencia de estudiantes.
    """
    @staticmethod
    def registrar_asistencia(id_estudiante, fecha, estado) -> None:
        """
        Registra la asistencia de un estudiante en una fecha dada.

        :param id_estudiante: ID del estudiante
        :param fecha: Fecha de la asistencia (objeto datetime.date)
        :param estado: Uno de 'Presente', 'Ausente', 'Tarde'
        """
        conn, cursor = conectar_db()
        try:
            sql = (
                "INSERT INTO asistencia (id_estudiante, fecha, estado_asistencia) "
                "VALUES (%s, %s, %s)"
            )
            cursor.execute(sql, (id_estudiante, fecha, estado))
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error al registrar asistencia: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def obtener_asistencia_por_estudiante_y_fecha(id_estudiante: int, fecha: date):
        conn, cursor = conectar_db()
        try:
            sql = "SELECT id_asistencia, estado_asistencia FROM asistencia WHERE id_estudiante = %s AND fecha = %s"
            cursor.execute(sql, (id_estudiante, fecha))
            return cursor.fetchone() # Retorna (id_asistencia, estado) o None
        finally:
            conn.close()

    @staticmethod
    def obtener_asistencias_por_estudiante(id_estudiante: int):
        """
        Obtiene todas las asistencias de un estudiante.

        :param id_estudiante: ID del estudiante
        :return: Lista de tuplas (id_asistencia, id_estudiante, fecha, estado_asistencia)
        """
        conn, cursor = conectar_db()
        try:
            sql = "SELECT id_asistencia, id_estudiante, fecha, estado_asistencia FROM asistencia WHERE id_estudiante = %s"
            cursor.execute(sql, (id_estudiante,))
            resultados = cursor.fetchall()
            return resultados
        finally:
            conn.close()

    @staticmethod
    def actualizar_asistencia(id_asistencia: int, estado: str) -> None:
        """
        Actualiza el estado de asistencia de un registro existente.

        :param id_asistencia: ID del registro de asistencia
        :param estado: Nuevo estado ('Presente', 'Ausente', 'Tarde')
        """
        conn, cursor = conectar_db()
        try:
            sql = "UPDATE asistencia SET estado_asistencia = %s WHERE id_asistencia = %s"
            cursor.execute(sql, (estado, id_asistencia))
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error al actualizar asistencia: {e}")
        finally:
            conn.close()

    @staticmethod
    def eliminar_asistencia(id_asistencia: int) -> None:
        """
        Elimina un registro de asistencia.

        :param id_asistencia: ID del registro de asistencia
        """
        conn, cursor = conectar_db()
        try:
            sql = "DELETE FROM asistencia WHERE id_asistencia = %s"
            cursor.execute(sql, (id_asistencia,))
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error al eliminar asistencia: {e}")
        finally:
            conn.close()


class Nota:
    """
    Clase para gestionar las notas de los estudiantes en distintas materias.
    """
    @staticmethod
    def registrar_nota(id_estudiante: int, id_materia: int, nota: float, fecha) -> None:
        """
        Registra una nueva nota para un estudiante en una materia.

        :param id_estudiante: ID del estudiante
        :param id_materia: ID de la materia
        :param nota: Calificación (decimal)
        :param fecha: Fecha de la nota (objeto datetime.date)
        """
        conn, cursor = conectar_db()
        try:
            sql = (
                "INSERT INTO notas (id_estudiante, id_materia, nota, fecha) "
                "VALUES (%s, %s, %s, %s)"
            )
            cursor.execute(sql, (id_estudiante, id_materia, nota, fecha))
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error al registrar nota: {e}")
        finally:
            conn.close()

    @staticmethod
    def obtener_notas_por_estudiante(id_estudiante: int):
        """
        Obtiene todas las notas de un estudiante.

        :param id_estudiante: ID del estudiante
        :return: Lista de tuplas (id_nota, id_estudiante, id_materia, nota, fecha)
        """
        conn, cursor = conectar_db()
        try:
            sql = "SELECT id_nota, id_estudiante, id_materia, nota, fecha FROM notas WHERE id_estudiante = %s"
            cursor.execute(sql, (id_estudiante,))
            resultados = cursor.fetchall()
            return resultados
        finally:
            conn.close()

    @staticmethod
    def actualizar_nota(id_nota: int, nueva_nota: float) -> None:
        """
        Actualiza el valor de una nota existente.

        :param id_nota: ID del registro de nota
        :param nueva_nota: Nuevo valor de la calificación
        """
        conn, cursor = conectar_db()
        try:
            sql = "UPDATE notas SET nota = %s WHERE id_nota = %s"
            cursor.execute(sql, (nueva_nota, id_nota))
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error al actualizar nota: {e}")
        finally:
            conn.close()

    @staticmethod
    def eliminar_nota(id_nota: int) -> None:
        """
        Elimina un registro de nota.

        :param id_nota: ID del registro de nota
        """
        conn, cursor = conectar_db()
        try:
            sql = "DELETE FROM notas WHERE id_nota = %s"
            cursor.execute(sql, (id_nota,))
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error al eliminar nota: {e}")
        finally:
            conn.close()



class MateriaProfesor:
    def __init__(self):
        pass

    @staticmethod
    def asociar_materia_a_profesor(id_profesor, id_materia):
        """
        Asocia una materia a un profesor.

        :param id_profesor: ID del profesor
        :param id_materia: ID de la materia
        """
        conn, cursor = conectar_db()
        
        try:
            query = "INSERT INTO profesor_materia (id_profesor, id_materia) VALUES (%s, %s)"
            cursor.execute(query, (id_profesor, id_materia))
            conn.commit()
        except mysql.connector.IntegrityError as e:
            print(f"No se pudo asociar: {e}")
        finally:
            conn.close()

    @staticmethod
    def obtener_materias_por_profesor(id_profesor):
        conn, cursor = conectar_db()
        
        query = """
            SELECT m.id_materia, m.nombre_materia
            FROM materia m
            INNER JOIN profesor_materia pm ON m.id_materia = pm.id_materia
            WHERE pm.id_profesor = %s
        """
        
        cursor.execute(query, (id_profesor,))
        materias = cursor.fetchall()
        
        conn.close()
        
        # Retorna lista de diccionarios (opcional) [{"id": m[0], "nombre": m[1]} for m in materias]
        return materias
    

    @staticmethod
    def eliminar_materias_de_profesor(id_profesor, ids_materias):
        """
        Elimina una o varias materias asociadas a un profesor.
        
        :param id_profesor: ID del profesor
        :param ids_materias: Lista de IDs de materias a eliminar
        """
        conn, cursor = conectar_db()
        
        query = """
            DELETE FROM profesor_materia
            WHERE id_profesor = %s AND id_materia = %s
        """
        
        for id_materia in ids_materias:
            cursor.execute(query, (id_profesor, id_materia))
        
        conn.commit()
        conn.close()


"""
-- Tabla profesor
CREATE TABLE profesor (
    id_profesor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefono VARCHAR(20)
);
"""
class Profesor:
    def __init__(self, nombre, apellido, email = None, telefono = None, id_profesor = None):
        self.id_profesor = id_profesor
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        
    @staticmethod
    def obtener_nombre_completo_profesor(id_profesor):
        """
        Retorna el nombre y apellido de un profesor dado su ID.

        :param id_profesor: ID del profesor
        :return: Tupla (nombre, apellido) o None si no existe
        """
        conn, cursor = conectar_db()
        
        try:
            query = "SELECT nombre, apellido FROM profesor WHERE id_profesor = %s"
            cursor.execute(query, (id_profesor,))
            resultado = cursor.fetchone()
            nombre_completo = f"{resultado[0]} {resultado[1]}"
            return nombre_completo
        finally:
            conn.close()

    def guardar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "INSERT INTO profesor (nombre, apellido, email, telefono) VALUES (%s, %s, %s, %s)"
            valores = (self.nombre, self.apellido, self.email, self.telefono)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    def actualizar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "UPDATE profesor SET nombre=%s, apellido=%s, email=%s, telefono=%s WHERE id_profesor=%s"
            valores = (self.nombre, self.apellido, self.email, self.telefono, self.id_profesor)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    def eliminar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "DELETE FROM profesor WHERE id_profesor=%s"
            valores = (self.id_profesor,)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    @staticmethod
    def obtener_todos():
        conn, cursor = conectar_db()
        if conn:
            cursor.execute("SELECT * FROM profesor")
            resultados = cursor.fetchall()
        return resultados


"""
-- Tabla estudiante
CREATE TABLE estudiante (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    email VARCHAR(100),
    id_curso INT,
    FOREIGN KEY (id_curso) REFERENCES curso(id_curso)
);
"""

class Estudiante:
    def __init__(self, nombre, apellido, id_curso, fecha_nacimiento = None, direccion = None, telefono = None, email = None, id_estudiante = None):
        self.id_estudiante = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.id_curso = id_curso


    def guardar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "INSERT INTO estudiante (nombre, apellido, fecha_nacimiento, direccion, telefono, email, id_curso) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores = (self.nombre, self.apellido, self.fecha_nacimiento, self.direccion, self.telefono, self.email, self.id_curso)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    def actualizar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "UPDATE estudiante SET nombre=%s, apellido=%s, fecha_nacimiento=%s, direccion=%s, telefono=%s, email=%s, id_curso=%s WHERE id_estudiante=%s"
            valores = (self.nombre, self.apellido, self.fecha_nacimiento, self.direccion, self.telefono, self.email, self.id_curso, self.id_estudiante)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    def eliminar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "DELETE FROM estudiante WHERE id_estudiante=%s"
            valores = (self.id_estudiante,)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    @staticmethod
    def obtener_todos():
        conn, cursor = conectar_db()
        estudiantes = []
        if conn:
            cursor.execute("SELECT * FROM estudiante")
            resultados = cursor.fetchall()
            for row in resultados:
                estudiantes.append(Estudiante(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[0]))
            conn.close()
        return resultados

    @staticmethod
    def obtener_por_id_curso(id_curso):
        """
        Objetivo:Filtrar estudiantes por curso.

        Args:
            (id_curso).

        Returns:
            Lista: de estudiantes.
        """
        conn, cursor = conectar_db()

        sql = "SELECT * FROM estudiante WHERE id_curso=%s"
        valores = (id_curso,)
        cursor.execute(sql, valores)
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    
    @staticmethod
    def obtener_nombre_completo(id_estudiante: int) -> str:
        """Obtiene nombre completo de un estudiante por su ID"""
        conn, cursor = conectar_db()
        try:
            cursor.execute(
                "SELECT nombre, apellido FROM estudiante WHERE id_estudiante = %s",
                (id_estudiante,)
            )
            if resultado := cursor.fetchone():
                return f"{resultado[0]} {resultado[1]}"
            return None
        finally:
            conn.close()

"""
-- Tabla materia
CREATE TABLE materia (
    id_materia INT AUTO_INCREMENT PRIMARY KEY,
    nombre_materia VARCHAR(100) NOT NULL,
    descripcion TEXT
);
"""

class Materia:
    def __init__(self,nombre,descripcion,id_materia=None):
        self.id_materia = id_materia
        self.nombre = nombre
        self.descripcion = descripcion

    @staticmethod
    def obtener_nombre_materia(id_materia):
        """
        Retorna el nombre de la materia dado su ID.

        :param id_materia: ID de la materia
        :return: Nombre de la materia o None si no existe
        """
        conn, cursor = conectar_db()
        
        try:
            query = "SELECT nombre_materia FROM materia WHERE id_materia = %s"
            cursor.execute(query, (id_materia,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        finally:
            conn.close()

    def guardar_registro(self):
        conn, cursor = conectar_db()#La funcion retorna dos instancias
        sql = "INSERT INTO materia (nombre_materia,descripcion) VALUES (%s, %s)"
        valores = (self.nombre,self.descripcion)
        cursor.execute(sql,valores)
        conn.commit()
        conn.close()

    def actualizar_registro(self):
        if self.id_materia is None:
            raise ValueError("ID requerido para actualizar")
        conn, cursor = conectar_db()
        sql = "UPDATE materia SET nombre_materia = %s, descripcion = %s WHERE id_materia = %s"
        valores = (self.nombre, self.descripcion, self.id_materia)

        cursor.execute(sql,valores)
        conn.commit()
        conn.close()
    
    def eliminar_registro(self):
        if self.id_materia is None:
            raise ValueError("ID requerido para eliminar")
        conn, cursor = conectar_db()
        cursor.execute("DELETE FROM materia WHERE id_materia = %s", (self.id_materia,))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_todos():
        conn, cursor = conectar_db()
        cursor.execute("SELECT * FROM materia")
        datos = cursor.fetchall()
        conn.close()

        return datos
    
"""
CREATE TABLE curso (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);
"""

class Curso:
    def __init__(self, nombre, descripcion, id_curso=None):
        self.id_curso = id_curso
        self.nombre = nombre
        self.descripcion = descripcion

    def guardar_registro(self):
        conn, cursor = conectar_db()
        sql = "INSERT INTO curso (nombre, descripcion) VALUES (%s, %s)"
        valores = (self.nombre, self.descripcion)
        cursor.execute(sql, valores)
        conn.commit()
        conn.close()

    def actualizar_registro(self):
        if self.id_curso is None:
            raise ValueError("ID requerido para actualizar")
        conn, cursor = conectar_db()
        sql = "UPDATE curso SET nombre = %s, descripcion = %s WHERE id_curso = %s"
        valores = (self.nombre, self.descripcion, self.id_curso)
        cursor.execute(sql, valores)
        conn.commit()
        conn.close()

    def eliminar_registro(self):
        if self.id_curso is None:
            raise ValueError("ID requerido para eliminar")
        conn, cursor = conectar_db()
        cursor.execute("DELETE FROM curso WHERE id_curso = %s", (self.id_curso,))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_todos():
        conn, cursor = conectar_db()
        cursor.execute("SELECT id_curso, nombre, descripcion FROM curso")
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def obtener_por_id(id_curso):
        conn, cursor = conectar_db()
        cursor.execute("SELECT id_curso, nombre, descripcion FROM curso WHERE id_curso = %s", (id_curso,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Curso(id_curso=row[0], nombre=row[1], descripcion=row[2])
        return None


