import flet as ft
from models.database import Materia
import asyncio

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
                ft.DataColumn(label=ft.Text("Descripción")),
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
        Recarga los datos de la base de datos y actualiza la tabla de materias.

        Este método puede ser llamado desde otros módulos para reflejar
        los cambios en la base de datos en la interfaz de usuario.
        """
        data = Materia.obtener_todos()
        new_rows = []
        for materia_id, nombre, descripcion in data:
            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(materia_id))),
                        ft.DataCell(ft.Text(nombre)),
                        ft.DataCell(ft.Text(descripcion)),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar Materia",
                                on_click=lambda ev, mid=materia_id, nom=nombre, desc=descripcion: self.seleccionar_materia(ev, mid, nom, desc),
                            )
                        ),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar Materia",
                                on_click=lambda ev, mid=materia_id, nom=nombre, desc=descripcion: self.eliminar_materia(ev, mid, nom, desc),
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

    def eliminar_materia(self, e, materia_id: int, nombre: str, descripcion: str):
        """
        Elimina la materia de la base de datos y actualiza la tabla.

        Args:
            e (ft.ControlEvent): El evento que desencadenó la acción.
            materia_id (int): El ID de la materia a eliminar.
            nombre (str): El nombre de la materia a eliminar (puede no ser necesario).
            descripcion (str): La descripción de la materia a eliminar (puede no ser necesario).
        """
        materia = Materia(nombre=nombre,descripcion=descripcion,id_materia=materia_id)
        materia.eliminar_registro()
        self.actualizar_tabla()  # Llamada para actualizar la tabla

    def seleccionar_materia(self, e, materia_id: int, materia_nombre: str, materia_descripcion: str):
        """
        Configura y abre el diálogo modal para editar una materia específica.

        Args:
            e (ft.ControlEvent): El evento que desencadenó la acción.
            materia_id (int): El ID de la materia a editar.
            materia_nombre (str): El nombre actual de la materia.
            materia_descripcion (str): La descripción actual de la materia.
        """
        # Controles nuevos por cada invocación
        tf_nombre = ft.TextField(label="Nombre", value=materia_nombre)
        tf_descripcion = ft.TextField(label="Descripción", value=materia_descripcion)

        self.dlg_modal.title = ft.Text("Editar Materia", weight=ft.FontWeight.BOLD)
        self.dlg_modal.content = ft.Column(
            [
                ft.Text(f"ID: {materia_id}", size=14),
                tf_nombre,
                tf_descripcion,
            ],
            tight=True,
        )
        self.dlg_modal.actions = [
            ft.TextButton(
                "Guardar",
                on_click=lambda ev: self.actualizar_datos(ev, materia_id, tf_nombre.value, tf_descripcion.value),
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

def formulario_registro(page: ft.Page, tabla_materias: TablaMaterias):
    """
    Crea y devuelve el formulario para registrar nuevas materias.

    Args:
        page (ft.Page): La página de Flet en la que se mostrará el formulario.
        tabla_materias (TablaMaterias): Una instancia de la clase TablaMaterias
                                       para poder actualizar la tabla después del registro.

    Returns:
        ft.Row: Una fila que contiene el formulario de registro centrado.
    """
    # Campos del formulario
    nombre = ft.TextField(label="Nombre de la Materia")
    descripcion = ft.TextField(label="Descripción")
    estado_registro = ft.Text(value="", color=ft.colors.GREEN_600)

    # Función para insertar materia
    async def insertar_dato(e):
        """Guarda la nueva materia en la base de datos y actualiza la tabla."""
        if not nombre.value.strip() or not descripcion.value.strip():
            estado_registro.value = "Todos los campos son obligatorios"
            estado_registro.color = ft.colors.RED
            page.update()
            await asyncio.sleep(2)
            estado_registro.value = ""
        else:
            try:
                materia = Materia(nombre.value.strip(), descripcion.value.strip())
                materia.guardar_registro()
                estado_registro.value = "Materia registrada exitosamente"
                estado_registro.color = ft.colors.GREEN
                page.update()

                tabla_materias.actualizar_tabla() # Actualiza la tabla después de guardar

                await asyncio.sleep(2)
                estado_registro.value = ""

                nombre.value = ""
                descripcion.value = ""
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
            width=400,
            padding=ft.padding.all(24),
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Registrar Materia", size=24, weight="bold"),
                    nombre,
                    descripcion,
                    boton_guardar,
                    estado_registro,
                ],
            ),
        ),
    )

    return ft.Row(controls=[formulario], alignment=ft.MainAxisAlignment.CENTER)

def materias(page: ft.Page):
    """
    Función principal para la gestión de materias, mostrando pestañas
    para registrar y ver las materias.

    Args:
        page (ft.Page): La página de Flet en la que se mostrará la interfaz.
    """
    # Instancia de la tabla de materias
    tabla_materias = TablaMaterias(page)

    return ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=True,
        tabs=[
            ft.Tab(
                text="Registrar",
                icon=ft.icons.NOTE_ADD,
                content=ft.Container(
                    content=formulario_registro(page, tabla_materias),
                    alignment=ft.alignment.center,
                    padding=30,
                ),
            ),
            ft.Tab(
                text="Ver Materias",
                icon=ft.icons.LIST_ALT,
                content=ft.Container(
                    content=tabla_materias.construir_tabla(),
                    alignment=ft.alignment.center,
                    padding=30,
                ),
            ),
        ],
    )

