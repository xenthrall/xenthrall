import flet as ft
from models.database import Curso
import asyncio

class TablaCursos:
    def __init__(self, page: ft.Page):
        self.page = page
        self.dlg_modal = ft.AlertDialog(modal=True)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("ID")),
                ft.DataColumn(label=ft.Text("Nombre del Curso")),
                ft.DataColumn(label=ft.Text("Descripción")),
                ft.DataColumn(label=ft.Text("Acciones")),
                ft.DataColumn(label=ft.Text("")),
            ],
            border=ft.border.all(1, ft.Colors.GREY),
        )
        self.actualizar_tabla() # Carga inicial de la tabla

    def cerrar_dialogo(self, e):
        """Cierra el diálogo modal."""
        self.dlg_modal.open = False
        self.page.update()

    def actualizar_tabla(self):
        """Recarga los datos de la base de datos y actualiza la tabla."""
        data = Curso.obtener_todos()
        new_rows = []
        for curso_id, nombre, descripcion in data:
            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(curso_id))),
                        ft.DataCell(ft.Text(nombre)),
                        ft.DataCell(ft.Text(descripcion)),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar curso",
                                on_click=lambda ev, cid=curso_id, nom=nombre, desc=descripcion: self.seleccionar_curso(ev, cid, nom, desc),
                            )
                        ),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar curso",
                                on_click=lambda ev, cid=curso_id, nom=nombre, desc=descripcion: self.eliminar_curso(ev, cid, nom, desc),
                            )
                        )
                    ]
                )
            )
        self.table.rows = new_rows
        self.page.update()

    def actualizar_datos(self, e, curso_id: int, nombre: str, descripcion: str):
        """
        Persiste los datos editados del curso de vuelta a la base de datos
        y luego actualiza la tabla.
        """
        curso = Curso(nombre=nombre, descripcion=descripcion, id_curso=curso_id)
        curso.actualizar_registro()
        self.cerrar_dialogo(e)
        self.actualizar_tabla()  # Llamada para actualizar la tabla
    
    def eliminar_curso(self, e, curso_id: int, nombre: str, descripcion: str):
        """
        Persiste los datos editados del curso de vuelta a la base de datos
        y luego actualiza la tabla.
        """
        curso = Curso(nombre=nombre, descripcion=descripcion, id_curso=curso_id)
        curso.eliminar_registro()
        self.actualizar_tabla()  # Llamada para actualizar la tabla

    def seleccionar_curso(self, e, curso_id: int, curso_nombre: str, curso_descripcion: str):
        """
        Configura y abre el diálogo modal para editar un curso específico.
        """
        # Controles nuevos por cada invocación
        tf_nombre = ft.TextField(label="Nombre", value=curso_nombre)
        tf_descripcion = ft.TextField(label="Descripción", value=curso_descripcion)

        self.dlg_modal.title = ft.Text("Editar Curso", weight=ft.FontWeight.BOLD)
        self.dlg_modal.content = ft.Column(
            [
                ft.Text(f"ID: {curso_id}", size=14),
                tf_nombre,
                tf_descripcion,
            ],
            tight=True,
        )
        self.dlg_modal.actions = [
            ft.TextButton(
                "Guardar",
                on_click=lambda ev: self.actualizar_datos(ev, curso_id, tf_nombre.value, tf_descripcion.value),
            ),
            ft.TextButton("Cerrar", on_click=self.cerrar_dialogo),
        ]
        self.dlg_modal.actions_alignment = ft.MainAxisAlignment.END

        if self.dlg_modal not in self.page.overlay:
            self.page.overlay.append(self.dlg_modal)

        self.dlg_modal.open = True
        self.page.update()

    def construir_tabla(self):
        """Retorna el control de la tabla para ser añadido a la página."""
        return ft.Column([self.table], scroll=True)




"""

#----------------------------------------------------------------------------------------------------------------

"""


def formulario_registro(page: ft.Page,tabla_cursos):
    # Campos del formulario
    nombre = ft.TextField(label="Nombre del curso")
    descripcion = ft.TextField(label="Descripción")
    estado_registro = ft.Text(value="", color=ft.Colors.GREEN_600)

    # Función para insertar curso
    async def insertar_dato(e):
        if not nombre.value.strip() or not descripcion.value.strip():
            estado_registro.value = "Todos los campos son obligatorios"
            estado_registro.color = ft.Colors.RED
            page.update()
            await asyncio.sleep(2)
            estado_registro.value = ""
        else:
            try:
                curso = Curso(nombre.value.strip(), descripcion.value.strip())
                curso.guardar_registro()
                estado_registro.value = "Curso registrado exitosamente"
                estado_registro.color = ft.Colors.GREEN
                page.update()
                
                tabla_cursos.actualizar_tabla()

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
        icon=ft.Icons.SAVE,
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
            bgcolor=ft.Colors.WHITE,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Registrar Curso", size=24, weight="bold"),
                    nombre,
                    descripcion,
                    boton_guardar,
                    estado_registro,
                ],
            ),
        ),
    )

    return ft.Row(controls=[formulario], alignment=ft.MainAxisAlignment.CENTER)

def cursos(page: ft.Page):
    # Tabs de la interfaz
    tabla_cursos = TablaCursos(page)

    return ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=True,
        tabs=[
            ft.Tab(
                text="Registrar",
                icon=ft.Icons.NOTE_ADD,
                content=ft.Container(
                    content=formulario_registro(page,tabla_cursos),
                    alignment=ft.alignment.center,
                    padding=30,
                ),
            ),
            ft.Tab(
                text="Ver cursos",
                icon=ft.Icons.LIST_ALT,
                content=ft.Container(
                    content=tabla_cursos.construir_tabla(),
                    alignment=ft.alignment.center,
                    padding=30,
                ),
            ),
        ],
    )
