import flet as ft
from models.database import Curso,Estudiante
import asyncio

class TablaEstudiantes:
    """
    Clase que gestiona la visualización y manipulación de la tabla de estudiantes.

    Permite mostrar, editar y eliminar estudiantes, y proporciona un método
    para actualizar la tabla desde otros módulos.
    """
    def __init__(self, page: ft.Page):
        """
        Inicializa la tabla de estudiantes.

        Args:
            page (ft.Page): La página de Flet en la que se mostrará la tabla.
        """
        self.page = page
        self.dlg_modal = ft.AlertDialog(modal=True)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("ID")),
                ft.DataColumn(label=ft.Text("Estudiante")),
                ft.DataColumn(label=ft.Text("Telefono")),
                ft.DataColumn(label=ft.Text("feccha de nacimiento")),
                ft.DataColumn(label=ft.Text("Acciones")),
                ft.DataColumn(label=ft.Text("")), # Columna para el botón de eliminar
            ],
            border=ft.border.all(1, ft.Colors.GREY),
        )
        self.actualizar_tabla() # Carga inicial de la tabla

    def cerrar_dialogo(self, e):
        """Cierra el diálogo modal."""
        self.dlg_modal.open = False
        self.page.update()

    def actualizar_tabla_id_curso(self, id_curso: int):
        data = Estudiante.obtener_por_id_curso(id_curso)
        self._actualizar_filas(data)


    def actualizar_tabla(self):
        data = Estudiante.obtener_todos()
        self._actualizar_filas(data)

    def _actualizar_filas(self, data):
        new_rows = []
        for e in data:
            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(e[0]))),
                        ft.DataCell(ft.Text(f"{e[1]} {e[2]}")),
                        ft.DataCell(ft.Text(e[5])),
                        ft.DataCell(ft.Text(e[3])),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar Estudiante",
                                on_click=lambda ev, id=e[0], nombre=e[1], apellido=e[2], 
                                fecha_nacimiento=e[3], direccion=e[4], telefono=e[5], 
                                email=e[6], id_curso=e[7]: self.seleccionar_estudiante(
                                    ev, id, nombre, apellido, fecha_nacimiento, 
                                    direccion, telefono, email, id_curso),
                            )
                        ),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar Estudiante",
                                on_click=lambda ev, id=e[0] : self.eliminar_estudiante(ev, id),
                            )
                        )
                    ]
                )
            )
        self.table.rows = new_rows
        self.page.update()

    def actualizar_datos(self,e,id,nombre,apellido,fecha_nacimiento,direccion,telefono,email,id_curso):
        """
        Persiste los datos editados de los estudiantes en la base de datos
        y luego actualiza la tabla.
        """
        estudiante = Estudiante(nombre, apellido, id_curso, fecha_nacimiento, direccion, telefono, email, id_estudiante = id)
        estudiante.actualizar_registro()
        self.cerrar_dialogo(e)
        self.actualizar_tabla()  # Llamada para actualizar la tabla

    def eliminar_estudiante(self, e, id):
        """
        Elimina al estudiante de la base de datos y actualiza la tabla.

        """
        Estudiante.eliminar_registro(id)
        self.actualizar_tabla()  # Llamada para actualizar la tabla

    def seleccionar_estudiante(self, e, id,nombre,apellido,fecha_nacimiento,direccion,telefono,email,id_curso):
        """
        Configura y abre el diálogo modal para editar un estudiante específico.

        Args:
            
        """
        if fecha_nacimiento:
            fecha = f"{fecha_nacimiento}"
        else:
            fecha = f"0000-00-00"

        def extraer_dato(a, fecha):
            """
            Extrae año, mes o día de una cadena de fecha en formato 'YYYY-MM-DD'.

            Parámetros:
                hola mundito
                a (str): puede ser 'año', 'mes' o 'dia'
                fecha (str): cadena con formato 'YYYY-MM-DD'

            Retorna:
                str: el valor correspondiente (año, mes o día)
            """
            if a == "año":
                return fecha[:4]
            elif a == "mes":
                return fecha[5:7]
            elif a == "dia":
                return fecha[8:]
            else:
                raise ValueError("Parámetro 'a' debe ser 'año', 'mes' o 'dia'")
            
        # Controles nuevos por cada invocación
        tf_nombre = ft.TextField(label="Nombres*",expand=1, value=nombre)
        tf_apellido = ft.TextField(label="Apellidos*",expand=1, value=apellido)

        tf_año = ft.TextField(label="Año",expand=2,input_filter=ft.NumbersOnlyInputFilter(),max_length=4,value=extraer_dato("año",fecha))
        tf_mes = ft.TextField(label="Mes",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2,value=extraer_dato("mes",fecha))
        tf_dia = ft.TextField(label="Dia",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2,value=extraer_dato("dia",fecha))

        tf_direccion = ft.TextField(label="Dirección",expand=1,value=direccion)
        tf_telefono = ft.TextField(label="Telefono",expand=1,value=telefono)
        tf_email = ft.TextField(label="Email",expand=1,value=email)


        contenido = ft.Card(
        elevation=8,
        shape=ft.RoundedRectangleBorder(radius=16),
        content=ft.Container(
            width=800,
            padding=ft.padding.all(24),
            bgcolor=ft.Colors.WHITE,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Editar Estudiante", size=24, weight="bold"),
                    ft.Container(content=ft.Row([tf_nombre,tf_apellido])),
                    ft.Container(content=ft.Row([tf_direccion,tf_telefono])),

                    ft.Container(content=ft.Row([ft.Container(content=ft.Text("Fecha de nacimiento: "),expand=1,alignment=ft.alignment.center),ft.Container(content=ft.Text(""),expand=1)])),

                    ft.Container(content=ft.Row([ft.Container(content=ft.Row([tf_año,tf_mes,tf_dia]),expand=1), tf_email])),
                    
                ],
            ),
        )
        )
        def obtener_fecha():
            if tf_año.value.strip() and tf_mes.value.strip() and tf_dia.value.strip():
                fecha_nacimiento = f"{tf_año.value.zfill(4)}-{tf_mes.value.zfill(2)}-{tf_dia.value.zfill(2)}"
            else:
                fecha_nacimiento = None
            return fecha_nacimiento

        self.dlg_modal.title = ft.Text(f"{nombre} {apellido}", weight=ft.FontWeight.BOLD)
        self.dlg_modal.content = ft.Column(
            [
                ft.Text(f"ID: {id}", size=14),
                contenido,
            ],
            tight=True,
        )
        self.dlg_modal.actions = [
            ft.TextButton(
                "Guardar",
                #def actualizar_datos(self,e,id,nombre,apellido,fecha_nacimiento,direccion,telefono,email,id_curso):
                on_click=lambda ev: self.actualizar_datos(ev, id, tf_nombre.value, tf_apellido.value,obtener_fecha(), tf_direccion.value, tf_telefono.value,tf_email.value,id_curso),
            ),
            ft.TextButton("Cerrar", on_click=self.cerrar_dialogo),
        ]
        self.dlg_modal.actions_alignment = ft.MainAxisAlignment.END

        if self.dlg_modal not in self.page.overlay:
            self.page.overlay.append(self.dlg_modal)

        self.dlg_modal.open = True
        self.page.update()

    def construir_tabla(self):
        """
        Retorna el control de la tabla (ft.Column que contiene el ft.DataTable)
        para ser añadido a la página.

        Returns:
            ft.Column: Un control de columna que contiene la tabla de materias.
        """
        return ft.Column([self.table], scroll=True)

#----------------------------------------------------------------------------------------------------------------
# Módulo para el formulario de registro de materias
#----------------------------------------------------------------------------------------------------------------

def autocompletado_cursos(tabla_estudiantes: TablaEstudiantes):
    def actualizar_curso(e):
        try:
            id_curso = int(e.selection.key.split()[0])
            tabla_estudiantes.actualizar_tabla_id_curso(id_curso)
        except (IndexError, ValueError):
            pass

    def obtener_sugerencias():
        return [
            ft.AutoCompleteSuggestion(
                key=f"{id} {nombre}",
                value=f"{nombre} - {descripcion}"
            ) for id, nombre, descripcion in Curso.obtener_todos()
        ]

    return ft.Container(
        content=ft.AutoComplete(
            suggestions=obtener_sugerencias(),
            on_select=actualizar_curso
        ),
        width=400,
        border=ft.border.all(1, ft.Colors.GREY),
        border_radius=ft.border_radius.all(5),
        padding=5
    )


def formulario_registro(page: ft.Page, tabla_materias: TablaEstudiantes):

    """
    Crea y devuelve el formulario para registrar nuevos estudiantes.
    def __init__(self, nombre, apellido, fecha_nacimiento, direccion, telefono, email, id_curso, id_estudiante = None):
    Args:
        page (ft.Page): La página de Flet en la que se mostrará el formulario.
        tabla_materias (TablaMaterias): Una instancia de la clase TablaMaterias
                                       para poder actualizar la tabla después del registro.

    Returns:
        ft.Row: Una fila que contiene el formulario de registro centrado.
    """
    # Campos del formulario
    nombre = ft.TextField(label="Nombres*",expand=1)
    apellido = ft.TextField(label="Apellidos*",expand=1)

    año = ft.TextField(label="Año",expand=2,input_filter=ft.NumbersOnlyInputFilter(),max_length=4)
    mes = ft.TextField(label="Mes",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2)
    dia = ft.TextField(label="Dia",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2)
    id_curso = ""



    def actualizar_id_curso(a):
        nonlocal id_curso 
        id_curso = a.key[:2]
       


    #Apartado del Input con sugerencias curso
    def refrescar_datos_curso():
        return Curso.obtener_todos()

    def obtener_sugenerencias_curso():
        items = []
        refrescar_datos_curso()
        for id, nombre, descripcion in refrescar_datos_curso():
            items.append(ft.AutoCompleteSuggestion(key=f"{id} {nombre}", value=f"{nombre} - {descripcion}"))
        return items

    auto_complete = ft.AutoComplete(
                suggestions=obtener_sugenerencias_curso(),
                on_select=lambda e: actualizar_id_curso(e.selection),
            )
    curso = ft.Container(
        content=auto_complete,
        expand=1,
        border=ft.border.all(1, ft.Colors.GREY),
        border_radius= ft.border_radius.all(5),
        padding=5,
    )
    

    direccion = ft.TextField(label="Dirección",expand=1)
    telefono = ft.TextField(label="Telefono",expand=1)
    email = ft.TextField(label="Email",expand=1)

    

    estado_registro = ft.Text(value="", color=ft.Colors.GREEN_600)

    
    

    # Función para insertar materia
    async def insertar_dato(e):
        """Guarda la nueva materia en la base de datos y actualiza la tabla."""
        if not id_curso:
            estado_registro.value = "Selecciona un curso"
            estado_registro.color = ft.Colors.RED
            page.update()
            await asyncio.sleep(2)


        else:
            if not nombre.value.strip() or not apellido.value.strip():
                print(id_curso)
                estado_registro.value = "Los campos nombres y apellidos son obligatorios"
                estado_registro.color = ft.Colors.RED
                page.update()
                await asyncio.sleep(2)
                estado_registro.value = ""
            else:
                try:
                    if año.value.strip() and mes.value.strip() and dia.value.strip():
                        fecha_nacimiento = f"{año.value.zfill(4)}-{mes.value.zfill(2)}-{dia.value.zfill(2)}"
                    else:
                        fecha_nacimiento = None

                    nuevo_estudiante = Estudiante(nombre.value, apellido.value, id_curso, fecha_nacimiento, direccion.value, telefono.value, email.value)
                    nuevo_estudiante.guardar_registro()
                    tabla_materias.actualizar_tabla()
                    estado_registro.value = "Estudiante registrado exitosamente"
                    estado_registro.color = ft.Colors.GREEN
                    page.update()

                    await asyncio.sleep(2)
                    estado_registro.value = ""

                    nombre.value = ""
                    apellido.value = ""

                    año.value = ""
                    mes.value = ""
                    dia.value = ""

                    direccion.value = ""
                    telefono.value = ""
                    email.value = ""

                        
                        

                   

                except Exception as ex:
                    estado_registro.value = f"Error: {ex}"

        page.update()

    # Botón de guardar
    boton_guardar = ft.ElevatedButton(
        text="Guardar",
        icon=ft.Icons.SAVE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=insertar_dato,
    )

    # Card con diseño del formulario
    formulario = ft.Card(
        elevation=8,
        shape=ft.RoundedRectangleBorder(radius=16),
        content=ft.Container(
            width=800,
            padding=ft.padding.all(24),
            bgcolor=ft.Colors.WHITE,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Registrar Estudiante", size=24, weight="bold"),
                    ft.Container(content=ft.Row([nombre,direccion])),
                    ft.Container(content=ft.Row([apellido,telefono])),
                    ft.Container(content=ft.Row([curso,email])),
                    ft.Text("Fecha de nacimiento:"),
                    ft.Container(content=ft.Row([año,mes,dia]),width=300),
                    boton_guardar,
                    estado_registro,
                    
                ],
            ),
        ),
    )

    return ft.Row(controls=[formulario], alignment=ft.MainAxisAlignment.CENTER)



def estudiantes(page: ft.Page):
    """
    Función principal para la gestión de materias, mostrando pestañas
    para registrar y ver las materias.

    Args:
        page (ft.Page): La página de Flet en la que se mostrará la interfaz.
    """
    # Instancia de la tabla de materias
    tabla_estudiantes = TablaEstudiantes(page)


    #Autocpmpletado

    auto = ft.Row([ft.Text("Seleccionar curso: "),autocompletado_cursos(tabla_estudiantes)])
    auto2 = ft.Container(content=autocompletado_cursos(tabla_estudiantes),width=300)

    return ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=True,
        tabs=[
            ft.Tab(
                text="Registrar",
                icon=ft.Icons.NOTE_ADD,
                content=ft.Container(
                    content=formulario_registro(page, tabla_estudiantes),
                    alignment=ft.alignment.center,
                    padding=30,
                ),
            ),
            ft.Tab(
                text="Ver Estudiantes",
                icon=ft.Icons.LIST_ALT,
                content=ft.Container(
                    content=ft.Column([
                    auto2,
                    tabla_estudiantes.construir_tabla()
                ], scroll=True),
                    alignment=ft.alignment.center,
                    padding=30,
                ),
            ),
        ],
    )



