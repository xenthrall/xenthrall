Requisitos para correr el sistema.

1-Tener creada la base de datos, en el asrchivo_sql.sql tenemos las operaciones necesarias.

2-Actualizar credenciales en el archivo database.py. 

db_name = "nombre de la base de datos"
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
        password="cambiar_pasword", #Contraseña de tu usuario
        database=db_name
    )
   
    cursor = conn.cursor()
    conn.commit()

    return conn, cursor


3-Instalar el framwork flet:
 ejemplo: pip install flet 