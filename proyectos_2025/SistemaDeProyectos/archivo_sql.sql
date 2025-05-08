
--Consulta para obtener empleados asignados a un proyecto especifico.
SELECT DISTINCT e.id_empleado, e.nombre, e.correo, e.telefono
FROM empleados e
JOIN tareas t ON e.id_empleado = t.id_empleado
WHERE t.id_proyecto = 1;


CREATE DATABASE IF NOT EXISTS sistemadeproyectos;
USE sistemadeproyectos;

-- Tabla Proyectos
CREATE TABLE proyectos (
    id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE
);

-- Tabla empleados
CREATE TABLE empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100),
    telefono VARCHAR(20)
);

CREATE TABLE tareas (
    id_tarea INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT,
    estado VARCHAR(30),
    fecha_inicio DATE,
    fecha_fin DATE,
    id_proyecto INT,
    id_empleado INT,
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE SET NULL
);
