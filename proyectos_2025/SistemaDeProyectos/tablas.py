import flet as ft
from database import Proyecto, Empleados, Tarea


class TablaTareas:
    
    def __init__(self, page: ft.Page):
        """
        Inicializa la tabla de empleados.

        Args:
            page (ft.Page): La página de Flet en la que se mostrará la tabla.
        """
        self.page = page
        self.dlg_modal = ft.AlertDialog(modal=True)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("ID")),
                ft.DataColumn(label=ft.Text("Tarea")),
                ft.DataColumn(label=ft.Text("estado")),
                ft.DataColumn(label=ft.Text("fecha_inicio")),
                ft.DataColumn(label=ft.Text("fecha_fin")),
                ft.DataColumn(label=ft.Text("empleado")),
                ft.DataColumn(label=ft.Text("proyecto")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            border=ft.border.all(1, ft.Colors.GREY),
        )
        self.actualizar_tabla() # Carga inicial de la tabla


    def actualizar_tabla(self):
        data = Tarea.obtener_todos()
        self._actualizar_filas(data)

    def _actualizar_filas(self, data):
        new_rows = []
        for e in data:
            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(e[0]))),
                        ft.DataCell(ft.Text(f"{e[1]}")),
                        ft.DataCell(ft.Text(f"{e[2]}")),
                        ft.DataCell(ft.Text(e[3])),
                        ft.DataCell(ft.Text(e[4])),
                        ft.DataCell(ft.Text(e[5])),
                        ft.DataCell(ft.Text(e[5])),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar Empleado",
                                on_click=lambda ev, id=e[0]: self.eliminar_registro(ev, id),
                            )
                        )
                    ]
                )
            )
        self.table.rows = new_rows
        self.page.update()

  

    def eliminar_registro(self, e, id):
        """
        Elimina pryecto de la base de datos y actualiza la tabla.

        """
        Empleados.eliminar_registro(id)
        self.actualizar_tabla()  # Llamada para actualizar la tabla

    
    def construir_tabla(self):
       
        return ft.Container(content=self.table,expand=1)
    


class TablaEmpleados:
    
    def __init__(self, page: ft.Page):
        """
        Inicializa la tabla de empleados.

        Args:
            page (ft.Page): La página de Flet en la que se mostrará la tabla.
        """
        self.page = page
        self.dlg_modal = ft.AlertDialog(modal=True)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("ID")),
                ft.DataColumn(label=ft.Text("Empleado")),
                ft.DataColumn(label=ft.Text("Correo")),
                ft.DataColumn(label=ft.Text("telefono")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            border=ft.border.all(1, ft.Colors.GREY),
        )
        self.actualizar_tabla() # Carga inicial de la tabla


    def actualizar_tabla(self):
        data = Empleados.obtener_todos()
        self._actualizar_filas(data)

    def _actualizar_filas(self, data):
        new_rows = []
        for e in data:
            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(e[0]))),
                        ft.DataCell(ft.Text(f"{e[1]}")),
                        ft.DataCell(ft.Text(f"{e[2]}")),
                        ft.DataCell(ft.Text(e[3])),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar Empleado",
                                on_click=lambda ev, id=e[0]: self.eliminar_registro(ev, id),
                            )
                        )
                    ]
                )
            )
        self.table.rows = new_rows
        self.page.update()

  

    def eliminar_registro(self, e, id):
        """
        Elimina pryecto de la base de datos y actualiza la tabla.

        """
        Empleados.eliminar_registro(id)
        self.actualizar_tabla()  # Llamada para actualizar la tabla

    
    def construir_tabla(self):
       
        return ft.Container(content=self.table,expand=1)
    

class TablaProyectos:
    
    def __init__(self, page: ft.Page):
        """
        Inicializa la tabla de proyectos.

        Args:
            page (ft.Page): La página de Flet en la que se mostrará la tabla.
        """
        self.page = page
        self.dlg_modal = ft.AlertDialog(modal=True)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("ID")),
                ft.DataColumn(label=ft.Text("Proyecto")),
                ft.DataColumn(label=ft.Text("Descripcion")),
                ft.DataColumn(label=ft.Text("fecha inicio")),
                ft.DataColumn(label=ft.Text("fecha fin")),
                ft.DataColumn(label=ft.Text("Acciones")),
            ],
            border=ft.border.all(1, ft.Colors.GREY),
        )
        self.actualizar_tabla() # Carga inicial de la tabla


    def actualizar_tabla(self):
        data = Proyecto.obtener_todos()
        self._actualizar_filas(data)

    def _actualizar_filas(self, data):
        new_rows = []
        for e in data:
            new_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(e[0]))),
                        ft.DataCell(ft.Text(f"{e[1]}")),
                        ft.DataCell(ft.Text(f"{e[2]}")),
                        ft.DataCell(ft.Text(e[3])),
                        ft.DataCell(ft.Text(e[4])),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar Proyecto",
                                on_click=lambda ev, id=e[0]: self.eliminar_registro(ev, id),
                            )
                        )
                    ]
                )
            )
        self.table.rows = new_rows
        self.page.update()

  

    def eliminar_registro(self, e, id):
        """
        Elimina pryecto de la base de datos y actualiza la tabla.

        """
        Proyecto.eliminar_registro(id)
        self.actualizar_tabla()  # Llamada para actualizar la tabla

    
    def construir_tabla(self):
       
        return ft.Container(content=self.table,expand=1)
    



def main(page:ft.Page):
    tabla = TablaTareas(page)
    
    page.add(tabla.construir_tabla())
if __name__ == "__main__":
    ft.app(target=main)