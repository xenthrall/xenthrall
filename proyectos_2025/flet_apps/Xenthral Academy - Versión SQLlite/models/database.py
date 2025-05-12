import sqlite3
from models.conexion_sqlite import conectar_db
from datetime import date # Asegúrate de que date esté importado

import sys
import os

def resource_path(relative_path):
    try:
        # PyInstaller usa una carpeta temporal
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Reportes:
    """
    Clase para generar diferentes reportes del sistema escolar.
    """
    @staticmethod
    def reporte_inscripcion_cursos():
        """
        Retorna el número de estudiantes inscritos en cada curso.
        :return: Lista de tuplas (id_curso, nombre_curso, total_estudiantes) o None si hay error.
        """
        conn, cursor = conectar_db()
        if not conn:
            return None
        try:
            sql = (
                "SELECT c.id_curso, c.nombre, COUNT(e.id_estudiante) "
                "FROM curso c "
                "LEFT JOIN estudiante e ON c.id_curso = e.id_curso "
                "GROUP BY c.id_curso, c.nombre"
            )
            cursor.execute(sql)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error en reporte_inscripcion_cursos: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def reporte_asistencia_por_estudiante(id_estudiante: int, fecha_inicio: date = None, fecha_fin: date = None):
        """
        Retorna conteo de estados de asistencia ('Presente','Ausente','Tarde') para un estudiante
        en un rango de fechas opcional.
        :return: Diccionario {estado: conteo} o None si hay error.
        """
        conn, cursor = conectar_db()
        if not conn:
            return None
        try:
            params = [id_estudiante]
            sql = (
                "SELECT estado_asistencia, COUNT(*) "
                "FROM asistencia WHERE id_estudiante = ?"
            )
            if fecha_inicio:
                sql += " AND fecha >= ?"
                params.append(str(fecha_inicio)) # SQLite espera fechas como strings ISO
            if fecha_fin:
                sql += " AND fecha <= ?"
                params.append(str(fecha_fin)) # SQLite espera fechas como strings ISO
            sql += " GROUP BY estado_asistencia"
            cursor.execute(sql, tuple(params))
            return {row[0]: row[1] for row in cursor.fetchall()}
        except sqlite3.Error as e:
            print(f"Error en reporte_asistencia_por_estudiante: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def reporte_asistencia_por_curso(id_curso: int, fecha_inicio: date = None, fecha_fin: date = None):
        """
        Retorna resumen de asistencia por curso (agrupado por estado).
        :return: Diccionario {estado: conteo} o None si hay error.
        """
        conn, cursor = conectar_db()
        if not conn:
            return None
        try:
            params = [id_curso]
            sql = (
                "SELECT a.estado_asistencia, COUNT(*) "
                "FROM asistencia a "
                "JOIN estudiante e ON a.id_estudiante = e.id_estudiante "
                "WHERE e.id_curso = ?"
            )
            if fecha_inicio:
                sql += " AND a.fecha >= ?"
                params.append(str(fecha_inicio))
            if fecha_fin:
                sql += " AND a.fecha <= ?"
                params.append(str(fecha_fin))
            sql += " GROUP BY a.estado_asistencia"
            cursor.execute(sql, tuple(params))
            return {row[0]: row[1] for row in cursor.fetchall()}
        except sqlite3.Error as e:
            print(f"Error en reporte_asistencia_por_curso: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def reporte_promedio_notas_por_estudiante(id_estudiante: int):
        """
        Retorna el promedio de notas de un estudiante por materia.
        :return: Lista de tuplas (id_materia, promedio_nota) o None si hay error.
        """
        conn, cursor = conectar_db()
        if not conn:
            return None
        try:
            sql = (
                "SELECT n.id_materia, AVG(n.nota) "
                "FROM notas n "
                "WHERE n.id_estudiante = ? "
                "GROUP BY n.id_materia"
            )
            cursor.execute(sql, (id_estudiante,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error en reporte_promedio_notas_por_estudiante: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def reporte_promedio_notas_por_materia(id_materia: int):
        """
        Retorna el promedio de notas de todos los estudiantes en una materia.
        :return: Float promedio o None si hay error o no hay notas.
        """
        conn, cursor = conectar_db()
        if not conn:
            return None
        try:
            sql = "SELECT AVG(nota) FROM notas WHERE id_materia = ?"
            cursor.execute(sql, (id_materia,))
            result = cursor.fetchone()
            return result[0] if result and result[0] is not None else None
        except sqlite3.Error as e:
            print(f"Error en reporte_promedio_notas_por_materia: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def reporte_estadisticas_notas_por_curso(id_curso: int):
        """
        Retorna promedio, nota máxima y mínima por materia para un curso.
        :return: Lista de tuplas (id_materia, avg, min, max) o None si hay error.
        """
        conn, cursor = conectar_db()
        if not conn:
            return None
        try:
            sql = (
                "SELECT n.id_materia, AVG(n.nota), MIN(n.nota), MAX(n.nota) "
                "FROM notas n "
                "JOIN estudiante e ON n.id_estudiante = e.id_estudiante "
                "WHERE e.id_curso = ? "
                "GROUP BY n.id_materia"
            )
            cursor.execute(sql, (id_curso,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error en reporte_estadisticas_notas_por_curso: {e}")
            return None
        finally:
            if conn:
                conn.close()


class Asistencia:
    """
    Clase para gestionar la asistencia de estudiantes.
    """
    @staticmethod
    def registrar_asistencia(id_estudiante: int, fecha_asistencia: date, estado: str) -> bool:
        """
        Registra la asistencia de un estudiante en una fecha dada.
        :param id_estudiante: ID del estudiante
        :param fecha_asistencia: Fecha de la asistencia (objeto datetime.date)
        :param estado: Uno de 'Presente', 'Ausente', 'Tarde'
        :return: True si fue exitoso, False en caso contrario.
        """
        conn, cursor = conectar_db()
        if not conn:
            return False
        try:
            sql = (
                "INSERT INTO asistencia (id_estudiante, fecha, estado_asistencia) "
                "VALUES (?, ?, ?)"
            )
            cursor.execute(sql, (id_estudiante, str(fecha_asistencia), estado))
            conn.commit()
            return True
        except sqlite3.Error as e: # sqlite3.IntegrityError es una subclase de sqlite3.Error
            print(f"Error al registrar asistencia: {e}")
            return False
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def obtener_asistencia_por_estudiante_y_fecha(id_estudiante: int, fecha_asistencia: date):
        """
        Obtiene un registro de asistencia específico.
        :return: Tupla (id_asistencia, estado_asistencia) o None.
        """
        conn, cursor = conectar_db()
        if not conn:
            return None
        try:
            sql = "SELECT id_asistencia, estado_asistencia FROM asistencia WHERE id_estudiante = ? AND fecha = ?"
            cursor.execute(sql, (id_estudiante, str(fecha_asistencia)))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error en obtener_asistencia_por_estudiante_y_fecha: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def obtener_asistencias_por_estudiante(id_estudiante: int):
        """
        Obtiene todas las asistencias de un estudiante.
        :param id_estudiante: ID del estudiante
        :return: Lista de tuplas (id_asistencia, id_estudiante, fecha, estado_asistencia) o None.
        """
        conn, cursor = conectar_db()
        if not conn:
            return None
        try:
            sql = "SELECT id_asistencia, id_estudiante, fecha, estado_asistencia FROM asistencia WHERE id_estudiante = ?"
            cursor.execute(sql, (id_estudiante,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error en obtener_asistencias_por_estudiante: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def actualizar_asistencia(id_asistencia: int, estado: str) -> bool:
        """
        Actualiza el estado de asistencia de un registro existente.
        :param id_asistencia: ID del registro de asistencia
        :param estado: Nuevo estado ('Presente', 'Ausente', 'Tarde')
        :return: True si fue exitoso, False en caso contrario.
        """
        conn, cursor = conectar_db()
        if not conn:
            return False
        try:
            sql = "UPDATE asistencia SET estado_asistencia = ? WHERE id_asistencia = ?"
            cursor.execute(sql, (estado, id_asistencia))
            conn.commit()
            return cursor.rowcount > 0 # Verifica si alguna fila fue afectada
        except sqlite3.Error as e:
            print(f"Error al actualizar asistencia: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def eliminar_asistencia(id_asistencia: int) -> bool:
        """
        Elimina un registro de asistencia.
        :param id_asistencia: ID del registro de asistencia
        :return: True si fue exitoso, False en caso contrario.
        """
        conn, cursor = conectar_db()
        if not conn:
            return False
        try:
            sql = "DELETE FROM asistencia WHERE id_asistencia = ?"
            cursor.execute(sql, (id_asistencia,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar asistencia: {e}")
            return False
        finally:
            if conn:
                conn.close()


class Nota:
    """
    Clase para gestionar las notas de los estudiantes en distintas materias.
    """
    @staticmethod
    def registrar_nota(id_estudiante: int, id_materia: int, valor_nota: float, fecha_nota: date) -> bool:
        """
        Registra una nueva nota para un estudiante en una materia.
        :param id_estudiante: ID del estudiante
        :param id_materia: ID de la materia
        :param valor_nota: Calificación (decimal)
        :param fecha_nota: Fecha de la nota (objeto datetime.date)
        :return: True si fue exitoso, False en caso contrario.
        """
        conn, cursor = conectar_db()
        if not conn:
            return False
        try:
            sql = (
                "INSERT INTO notas (id_estudiante, id_materia, nota, fecha) "
                "VALUES (?, ?, ?, ?)"
            )
            cursor.execute(sql, (id_estudiante, id_materia, valor_nota, str(fecha_nota)))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al registrar nota: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def obtener_notas_por_estudiante(id_estudiante: int):
        """
        Obtiene todas las notas de un estudiante.
        :param id_estudiante: ID del estudiante
        :return: Lista de tuplas (id_nota, id_estudiante, id_materia, nota, fecha) o None.
        """
        conn, cursor = conectar_db()
        if not conn:
            return None
        try:
            sql = "SELECT id_nota, id_estudiante, id_materia, nota, fecha FROM notas WHERE id_estudiante = ?"
            cursor.execute(sql, (id_estudiante,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error en obtener_notas_por_estudiante: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def actualizar_nota(id_nota: int, nueva_nota: float) -> bool:
        """
        Actualiza el valor de una nota existente.
        :param id_nota: ID del registro de nota
        :param nueva_nota: Nuevo valor de la calificación
        :return: True si fue exitoso, False en caso contrario.
        """
        conn, cursor = conectar_db()
        if not conn:
            return False
        try:
            sql = "UPDATE notas SET nota = ? WHERE id_nota = ?"
            cursor.execute(sql, (nueva_nota, id_nota))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al actualizar nota: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def eliminar_nota(id_nota: int) -> bool:
        """
        Elimina un registro de nota.
        :param id_nota: ID del registro de nota
        :return: True si fue exitoso, False en caso contrario.
        """
        conn, cursor = conectar_db()
        if not conn:
            return False
        try:
            sql = "DELETE FROM notas WHERE id_nota = ?"
            cursor.execute(sql, (id_nota,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar nota: {e}")
            return False
        finally:
            if conn:
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
        query = "INSERT INTO profesor_materia (id_profesor, id_materia) VALUES (?, ?)"
        cursor.execute(query, (id_profesor, id_materia))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_materias_por_profesor(id_profesor):
        conn, cursor = conectar_db()
        
        query = """
            SELECT m.id_materia, m.nombre_materia
            FROM materia m
            INNER JOIN profesor_materia pm ON m.id_materia = pm.id_materia
            WHERE pm.id_profesor = ?
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
            WHERE id_profesor = ? AND id_materia = ?
        """
        
        for id_materia in ids_materias:
            cursor.execute(query, (id_profesor, id_materia))
        
        conn.commit()
        conn.close()



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
            query = "SELECT nombre, apellido FROM profesor WHERE id_profesor = ?"
            cursor.execute(query, (id_profesor,))
            resultado = cursor.fetchone()
            nombre_completo = f"{resultado[0]} {resultado[1]}"
            return nombre_completo
        finally:
            conn.close()

    def guardar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "INSERT INTO profesor (nombre, apellido, email, telefono) VALUES (?, ?, ?, ?)"
            valores = (self.nombre, self.apellido, self.email, self.telefono)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    def actualizar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "UPDATE profesor SET nombre=?, apellido=?, email=?, telefono=? WHERE id_profesor=?"
            valores = (self.nombre, self.apellido, self.email, self.telefono, self.id_profesor)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    def eliminar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "DELETE FROM profesor WHERE id_profesor=?"
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
            sql = "INSERT INTO estudiante (nombre, apellido, fecha_nacimiento, direccion, telefono, email, id_curso) VALUES (?, ?, ?, ?, ?, ?, ?)"
            valores = (self.nombre, self.apellido, self.fecha_nacimiento, self.direccion, self.telefono, self.email, self.id_curso)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    def actualizar_registro(self):
        conn, cursor = conectar_db()
        if conn:
            sql = "UPDATE estudiante SET nombre=?, apellido=?, fecha_nacimiento=?, direccion=?, telefono=?, email=?, id_curso=? WHERE id_estudiante=?"
            valores = (self.nombre, self.apellido, self.fecha_nacimiento, self.direccion, self.telefono, self.email, self.id_curso, self.id_estudiante)
            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

    @staticmethod
    def eliminar_registro(id_estudiante):
        conn, cursor = conectar_db()
        if conn:
            sql = "DELETE FROM estudiante WHERE id_estudiante=?"
            valores = (id_estudiante,)
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

        sql = "SELECT * FROM estudiante WHERE id_curso=?"
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
                "SELECT nombre, apellido FROM estudiante WHERE id_estudiante = ?",
                (id_estudiante,)
            )
            if resultado := cursor.fetchone():
                return f"{resultado[0]} {resultado[1]}"
            return None
        finally:
            conn.close()


class Materia:
    def __init__(self, nombre: str, descripcion: str = None, id_materia: int = None):
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
            query = "SELECT nombre_materia FROM materia WHERE id_materia = ?"
            cursor.execute(query, (id_materia,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        finally:
            conn.close()

    def guardar_registro(self):
        conn, cursor = conectar_db()#La funcion retorna dos instancias
        sql = "INSERT INTO materia (nombre_materia,descripcion) VALUES (?, ?)"
        valores = (self.nombre,self.descripcion)
        cursor.execute(sql,valores)
        conn.commit()
        conn.close()

    def actualizar_registro(self):
        if self.id_materia is None:
            raise ValueError("ID requerido para actualizar")
        conn, cursor = conectar_db()
        sql = "UPDATE materia SET nombre_materia = ?, descripcion = ? WHERE id_materia = ?"
        valores = (self.nombre, self.descripcion, self.id_materia)

        cursor.execute(sql,valores)
        conn.commit()
        conn.close()
    
    def eliminar_registro(self):
        if self.id_materia is None:
            raise ValueError("ID requerido para eliminar")
        conn, cursor = conectar_db()
        cursor.execute("DELETE FROM materia WHERE id_materia = ?", (self.id_materia,))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_todos():
        conn, cursor = conectar_db()
        cursor.execute("SELECT * FROM materia")
        datos = cursor.fetchall()
        conn.close()

        return datos


class Curso:
    def __init__(self, nombre: str, descripcion: str = None, id_curso: int = None):
        self.id_curso = id_curso
        self.nombre = nombre
        self.descripcion = descripcion

    def guardar_registro(self):
        conn, cursor = conectar_db()
        sql = "INSERT INTO curso (nombre, descripcion) VALUES (?, ?)"
        valores = (self.nombre, self.descripcion)
        cursor.execute(sql, valores)
        conn.commit()
        conn.close()

    def actualizar_registro(self):
        if self.id_curso is None:
            raise ValueError("ID requerido para actualizar")
        conn, cursor = conectar_db()
        sql = "UPDATE curso SET nombre = ?, descripcion = ? WHERE id_curso = ?"
        valores = (self.nombre, self.descripcion, self.id_curso)
        cursor.execute(sql, valores)
        conn.commit()
        conn.close()

    def eliminar_registro(self):
        if self.id_curso is None:
            raise ValueError("ID requerido para eliminar")
        conn, cursor = conectar_db()
        cursor.execute("DELETE FROM curso WHERE id_curso = ?", (self.id_curso,))
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
        cursor.execute("SELECT id_curso, nombre, descripcion FROM curso WHERE id_curso = ?", (id_curso,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Curso(id_curso=row[0], nombre=row[1], descripcion=row[2])
        return None

