# Xenthrall Academy - Versión SQLite

**Xenthrall Academy** es una aplicación de gestión escolar desarrollada en [Python](https://www.python.org/) utilizando el framework [Flet](https://flet.dev/) para la interfaz gráfica de usuario.  
Esta versión utiliza **SQLite** como motor de base de datos local, lo que la hace liviana, portátil y fácil de configurar.

---

## 🧰 Requisitos

Para ejecutar esta aplicación, necesitas tener lo siguiente instalado en tu sistema:

- Python 3.8 o superior
- Librería Flet (`pip install flet`)

---

## 📦 Instalación

### 1. Clona el repositorio

```bash
git https://github.com/xenthrall/xenthrall.git
cd xenthrall-academy

2. Instala las dependencias
pip install flet==0.28.2


3. Ejecuta la aplicación
python main.py


🧾 Notas importantes
Esta versión no requiere configuración adicional de bases de datos externas.

Todos los datos se almacenan localmente en un archivo .db mediante SQLite.

Puedes modificar la conexión en models/conexion_sqlite.py si deseas cambiar la ruta o nombre del archivo de base de datos.

📁 Estructura del proyecto

xenthrall-academy-version-sqlite/
│
├── assets/                     # Archivos multimedia (logos, audio)
│   ├── logo.png
│   ├── logo_xenthrall.png
│   └── song.mp3
│
├── models/                     # Conexiones y lógica de base de datos
│   ├── conexion_sqlite.py
│   └── database.py
│
├── views/                      # Vistas modulares de la aplicación
│   ├── acerca_de.py
│   ├── asistencias_view.py
│   ├── cursos.py
│   ├── estudiantes.py
│   ├── inicio.py
│   ├── materias.py
│   ├── notas_view.py
│   ├── profesores.py
│   └── reportes.py
│
├── main.py                     # Punto de entrada de la aplicación
└── readme.md                   # Este archivo


🚀 Funcionalidades principales

Gestión de estudiantes, profesores y materias.

Registro y visualización de asistencias.

Administración de notas y reportes.

Interfaz moderna y responsiva con Flet.

Base de datos local sin necesidad de servidor externo.

