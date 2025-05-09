import flet as ft
from models.database import Profesor, Materia, MateriaProfesor
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
                ft.DataColumn(label=ft.Text("Profesor")),
                ft.DataColumn(label=ft.Text("Email")),
                ft.DataColumn(label=ft.Text("Telefono")),
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

    def actualizar_tabla(self):
        """
        Recarga los datos de la base de datos y actualiza la tabla de estudiantes.

        Este método puede ser llamado desde otros módulos para reflejar
        los cambios en la base de datos en la interfaz de usuario.
        """
        data = Profesor.obtener_todos()
        new_rows = []
        for e in data:
            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(e[0]))),
                        ft.DataCell(ft.Text(f"{e[1]} {e[2]}")),
                        ft.DataCell(ft.Text(e[3])),
                        ft.DataCell(ft.Text(e[4])),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar Profesor",
                                on_click=lambda ev, id=e[0], nombre=e[1], apellido=e[2], email=e[3], telefono=e[4]: self.seleccionar_estudiante(ev, id, nombre, apellido, email, telefono),
                            )
                        ),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar Estudiante",
                                on_click=lambda ev, id=e[0], nombre=e[1], apellido=e[2], email=e[3], telefono=e[4]: self.eliminar_estudiante(ev, id, nombre, apellido, email, telefono),
                            )
                        )
                    ]
                )
            )
        self.table.rows = new_rows
        self.page.update()

    def actualizar_datos(self,e,nombre,apellido,email,telefono,id):
        """
        Persiste los datos editados de los estudiantes en la base de datos
        y luego actualiza la tabla.
        """
        profesor = Profesor(nombre, apellido, email, telefono,id)
        profesor.actualizar_registro()
        self.cerrar_dialogo(e)
        self.actualizar_tabla()  # Llamada para actualizar la tabla

    def eliminar_estudiante(self, e, id,nombre,apellido,email,telefono):
        """
        Elimina al estudiante de la base de datos y actualiza la tabla.

        """
        profesor = Profesor(nombre, apellido, email, telefono,id)
        profesor.eliminar_registro()
        self.actualizar_tabla()  # Llamada para actualizar la tabla

    def seleccionar_estudiante(self, e, id,nombre,apellido,email,telefono):
        """
        Configura y abre el diálogo modal para editar un profesor específico.

        Args:
            
        """

        # Controles nuevos por cada invocación
        tf_nombre = ft.TextField(label="Nombres*",expand=1, value=nombre)
        tf_apellido = ft.TextField(label="Apellidos*",expand=1, value=apellido)


        tf_telefono = ft.TextField(label="Telefono",expand=1, value=telefono)
        tf_email = ft.TextField(label="Email",expand=1, value=email)


        contenido = ft.Card(
        elevation=8,
        shape=ft.RoundedRectangleBorder(radius=16),
        content=ft.Container(
            width=800,
            padding=ft.padding.all(24),
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Editar Profesor", size=24, weight="bold"),
                    ft.Container(content=ft.Row([tf_nombre, tf_apellido])),
                    ft.Container(content=ft.Row([tf_email, tf_telefono])),
                    
                ],
            ),
        )
        )

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
                on_click=lambda ev: self.actualizar_datos(ev,tf_nombre.value, tf_apellido.value, tf_email.value, tf_telefono.value, id),
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


def formulario_registro(page: ft.Page, tabla_materias: TablaEstudiantes):

    """
    Crea y devuelve el formulario para registrar nuevos estudiantes.
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
       
    

    telefono = ft.TextField(label="Telefono",expand=1)
    email = ft.TextField(label="Email",expand=1)

    

    estado_registro = ft.Text(value="", color=ft.colors.GREEN_600)

    
    

    # Función para insertar materia
    async def insertar_dato(e):
        """Guarda la nueva materia en la base de datos y actualiza la tabla."""
        
        if not nombre.value.strip() or not apellido.value.strip():
                estado_registro.value = "Los campos nombres y apellidos son obligatorios"
                estado_registro.color = ft.colors.RED
                page.update()
                await asyncio.sleep(2)
                estado_registro.value = ""
        else:
                try:

                    nuevo_estudiante = Profesor(nombre.value, apellido.value, email.value, telefono.value)
                    nuevo_estudiante.guardar_registro()
                    tabla_materias.actualizar_tabla()
                    estado_registro.value = "Profesor registrado exitosamente"
                    estado_registro.color = ft.colors.GREEN
                    page.update()

                    await asyncio.sleep(2)
                    estado_registro.value = ""

                    nombre.value = ""
                    apellido.value = ""

                    telefono.value = ""
                    email.value = ""

                        
                        

                   

                except Exception as ex:
                    estado_registro.value = f"Error: {ex}"

        page.update()

    # Botón de guardar
    boton_guardar = ft.ElevatedButton(
        text="Guardar",
        icon=ft.icons.SAVE,
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
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Registrar Profesor", size=24, weight="bold"),
                    ft.Container(content=ft.Row([nombre,apellido])),
                    ft.Container(content=ft.Row([email,telefono])),
                    boton_guardar,
                    estado_registro,
                    
                ],
            ),
        ),
    )

    return ft.Row(controls=[formulario], alignment=ft.MainAxisAlignment.CENTER)


#--------------------ids para asociar materias etc --------------------------#
valor_id_profesor = None
valor_id_materia = None

#Informacion del profesor y materia selccionados
infromacion_profesor = ft.Text(f"Profesor: {valor_id_profesor}", expand=1,size=16,color=ft.colors.BLUE_900)
infromacion_materia = ft.Text(f"Materia: {valor_id_materia}", expand=1,size=16, color=ft.Colors.BLUE_900)




#----------------------- tabla materias ---------------------------------------------#


class TablaMaterias:
    """
    Clase que gestiona la visualización y manipulación de la tabla de materias.

    Permite mostrar, editar y eliminar materias, y proporciona un método
    para actualizar la tabla desde otros módulos.
    """
    def __init__(self, page: ft.Page):
        """
        Inicializa la tabla de materias.

        Args:
            page (ft.Page): La página de Flet en la que se mostrará la tabla.
        """
        self.page = page
        self.dlg_modal = ft.AlertDialog(modal=True)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("ID")),
                ft.DataColumn(label=ft.Text("Materia")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            border=ft.border.all(1, ft.Colors.GREY),
        )
        self.actualizar_tabla() # Carga inicial de la tabla

    def cerrar_dialogo(self, e):
        """Cierra el diálogo modal."""
        self.dlg_modal.open = False
        self.page.update()

    def actualizar_tabla(self):
        """
        Recarga los datos de la base de datos y actualiza la tabla de materias.

        Este método puede ser llamado desde otros módulos para reflejar
        los cambios en la base de datos en la interfaz de usuario.
        """
        data = MateriaProfesor.obtener_materias_por_profesor(valor_id_profesor)
        new_rows = []
        for materia_id, nombre in data:
            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(materia_id))),
                        ft.DataCell(ft.Text(nombre)),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar Materia",
                                on_click=lambda ev, mid=materia_id, nom=nombre: self.eliminar_materia(ev, mid, nom),
                            )
                        )
                    ]
                )
            )
        self.table.rows = new_rows
        self.page.update()

    def actualizar_datos(self, e, materia_id: int, nombre: str, descripcion: str):
        """
        Persiste los datos editados de la materia en la base de datos
        y luego actualiza la tabla.

        Args:
            e (ft.ControlEvent): El evento que desencadenó la acción.
            materia_id (int): El ID de la materia a actualizar.
            nombre (str): El nuevo nombre de la materia.
            descripcion (str): La nueva descripción de la materia.
        """
        materia = Materia(nombre=nombre, descripcion=descripcion, id_materia=materia_id)
        materia.actualizar_registro()
        self.cerrar_dialogo(e)
        self.actualizar_tabla()  # Llamada para actualizar la tabla

    def eliminar_materia(self, e, materia_id, nombre):
        """
        Elimina la materia de la base de datos y actualiza la tabla.

        Args:
            e (ft.ControlEvent): El evento que desencadenó la acción.
            materia_id (int): El ID de la materia a eliminar.
            nombre (str): El nombre de la materia a eliminar (puede no ser necesario).
            descripcion (str): La descripción de la materia a eliminar (puede no ser necesario).
        """

       
        MateriaProfesor.eliminar_materias_de_profesor(valor_id_profesor,[materia_id])
        self.actualizar_tabla()  # Llamada para actualizar la tabla


    def construir_tabla(self):
        """
        Retorna el control de la tabla (ft.Column que contiene el ft.DataTable)
        para ser añadido a la página.

        Returns:
            ft.Column: Un control de columna que contiene la tabla de materias.
        """
        return ft.Column([self.table], scroll=True)



#-----------------------------Autocompletado-----------------------------------------#

def actualizar_informacion_profesor(page: ft.Page):
    infromacion_profesor.value = f"Profesor: {Profesor.obtener_nombre_completo_profesor(valor_id_profesor)}"
    page.update()

def actualizar_informacion_materia(page: ft.Page):
    infromacion_materia.value = f"Materia: {Materia.obtener_nombre_materia(valor_id_materia)}"
    page.update()

def autocompletado_profesores(page: ft.Page, tabla_materias:TablaMaterias):
    def actualizar_id(id):
        global valor_id_profesor
        valor_id_profesor = id
    
    def seleccionar_profesor(e):
        try:
            id_profesor = int(e.selection.key.split()[0])
            print(id_profesor)
            actualizar_id(id_profesor)
            actualizar_informacion_profesor(page)
            tabla_materias.actualizar_tabla()
            #tabla_estudiantes.actualizar_tabla_id_curso(id_curso)
        except (IndexError, ValueError):
            pass
            
    def obtener_sugerencias():
        items = []
        for p in Profesor.obtener_todos():
            items.append(ft.AutoCompleteSuggestion(
              key = f"{p[0]} {p[1]}",
              value= f"{p[1]} {p[2]}" 
            ))

        return items

    return ft.Container(
        content=ft.AutoComplete(
            suggestions=obtener_sugerencias(),
            on_select=seleccionar_profesor
        ),
        expand=4,
        border=ft.border.all(1, ft.Colors.GREY),
        border_radius=ft.border_radius.all(5),
        padding=5
    )

def autocompletado_materias(page: ft.Page):

    def actualizar_id(id):
        global valor_id_materia
        valor_id_materia = id

    def seleccionar_materia(e):
        try:
            id_materia = int(e.selection.key.split()[0])
            actualizar_id(id_materia)
            actualizar_informacion_materia(page)

        except (IndexError, ValueError):
            pass

    def obtener_sugerencias():
        return [
            ft.AutoCompleteSuggestion(
                key=f"{id} {nombre}",
                value=f"{nombre} - {descripcion}"
            ) for id, nombre, descripcion in Materia.obtener_todos()
        ]

    return ft.Container(
        content=ft.AutoComplete(
            suggestions=obtener_sugerencias(),
            on_select=seleccionar_materia
        ),
        expand=4,
        border=ft.border.all(1, ft.Colors.GREY),
        border_radius=ft.border_radius.all(5),
        padding=5
    )




def modulo_asignar_materias(page: ft.Page):

    tabla_materias = TablaMaterias(page)
    

    


    #-----------Autocompletado profesores-----------#
    auto_profesores = ft.Row([ft.Text("Profesor: ",expand=1), autocompletado_profesores(page,tabla_materias)])

    #--------Autocompletado materias-------------#
    auto_materias = ft.Row([ft.Text("Materia:  ",expand=1), autocompletado_materias(page)])

    
    #Informacion del profesor y materia selccionados

    encabezado = ft.Row([infromacion_profesor, infromacion_materia])

    #Esta de asignacion
    estado_asignacion = ft.Text("")


    #Asignar
    async def asignar(e):
        if not valor_id_materia  or not valor_id_profesor:
            estado_asignacion.value = "Obligatorio seleccionar un profesor y una materia"
            estado_asignacion.color = ft.Colors.RED
            page.update()
            await asyncio.sleep(2)
        else:
            MateriaProfesor.asociar_materia_a_profesor(valor_id_profesor,valor_id_materia)
            tabla_materias.actualizar_tabla()
            estado_asignacion.value = "Exito"
            estado_asignacion.color = ft.Colors.GREEN
            page.update()
            await asyncio.sleep(1)

        estado_asignacion.value = ""
        page.update()


    btn_asignar = ft.ElevatedButton("Asignar",on_click=asignar)

    formulario_asignacion_materias = ft.Container(
        content=ft.Column(
            spacing=20,
            controls=[
                encabezado,
                ft.Divider(),
                auto_profesores,
                auto_materias,
                btn_asignar,
                estado_asignacion
                ]
        ),
        expand=1,
        
    )

    listado_materias = ft.Container(
        content=tabla_materias.construir_tabla(),
        alignment= ft.alignment.center,
        expand=1
    )

    contenido = ft.Container(
        content=ft.Row([
            formulario_asignacion_materias,
            ft.VerticalDivider(),
            listado_materias,
            ]),
        expand=True
    )
    return contenido

def profesores(page: ft.Page):
    """
    Función principal para la gestión de materias, mostrando pestañas
    para registrar y ver las materias.

    Args:
        page (ft.Page): La página de Flet en la que se mostrará la interfaz.
    """
    # Instancia de la tabla de materias
    tabla_estudiantes = TablaEstudiantes(page)

    return ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=True,
        tabs=[
            ft.Tab(
                text="Registrar",
                icon=ft.icons.NOTE_ADD,
                content=ft.Container(
                    content=formulario_registro(page, tabla_estudiantes),
                    alignment=ft.alignment.center,
                    padding=30,
                ),
            ),
            ft.Tab(
                text="Ver Profesores",
                icon=ft.icons.LIST_ALT,
                content=ft.Container(
                    content=tabla_estudiantes.construir_tabla(),
                    alignment=ft.alignment.center,
                    padding=30,
                ),
            ),

            ft.Tab(
                text="Asignar Materias",
                icon=ft.icons.BOOK,
                content=ft.Container(
                    content=modulo_asignar_materias(page),
                    alignment=ft.alignment.center,
                    padding=30,
                ),
            ),
        ],
    )



def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(profesores(page))

if __name__ == "__main__":
    ft.app(target=main)