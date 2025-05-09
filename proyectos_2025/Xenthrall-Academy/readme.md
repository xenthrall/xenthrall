# Xenthrall-Academy

**Xenthrall-Academy** es una aplicación de gestión escolar desarrollada en [Python](https://www.python.org/) utilizando el framework [Flet](https://flet.dev/) para la interfaz de usuario.  
Se conecta a una base de datos MySQL y permite gestionar estudiantes, cursos, calificaciones, asistencia y más.

---

## 🧰 Requisitos

Para ejecutar esta aplicación, necesitas tener lo siguiente instalado en tu sistema:

- Python 3.8 o superior
- Servidor MySQL (ejecutándose en localhost)
- Librería Flet para Python


---

## 📦 Instalación

### 1. Instalar dependencias

Primero, instala la librería Flet usando `pip`:

```bash
pip install flet



2. Crear la base de datos
Debes crear una base de datos MySQL llamada colegio en tu servidor local.

Si lo necesitas, se incluye un script SQL completo en la siguiente ruta:


models/script_crear_dbs.sql
Puedes ejecutar este script desde la línea de comandos de MySQL.

3. Configurar las credenciales de conexión
En el archivo database.py, ubica la función conectar_db() y modifica los parámetros si es necesario:

def conectar_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="xenthrall1@",  # Cambiar si es necesario
        database=db_name
    )
    cursor = conn.cursor()
    return conn, cursor
Asegúrate de que estas credenciales coincidan con las configuradas en tu servidor MySQL.

🚀 Ejecutar la aplicación
Simplemente ejecuta el archivo main.py con Python:

python main.py
Esto abrirá la ventana de la aplicación utilizando Flet.

🧾 Notas
Asegúrate de que el servidor MySQL esté en ejecución antes de iniciar la aplicación.

Puedes personalizar el nombre de la base de datos, usuario y contraseña tanto en el script SQL como en el código.

Si encuentras errores relacionados con la base de datos, verifica que el servicio de MySQL esté activo y que las credenciales sean correctas.



📁 Estructura del proyecto


xenthrall-academy/
│
├── main.py                     # Archivo principal de ejecución
├── models/
│   └── script_crear_dbs.sql    # Script SQL para crear la base de datos
|   |
|   └── database.py             # Lógica de conexión a la base de datos
|
├── views/
│    | #Vistas o modulos que se visualizan desde el menu contextual
└── ...              