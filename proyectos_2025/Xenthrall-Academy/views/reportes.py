import flet as ft
from datetime import date
from models.database import Reportes, Estudiante, Curso, Materia # Asegúrate que esta línea sea correcta para tu estructura

def reportes_view(page: ft.Page):
    # Control para seleccionar el tipo de reporte
    tipo_reporte = ft.Dropdown(
        label="Seleccione tipo de reporte",
        options=[
            ft.dropdown.Option("Inscripción por cursos"),
            ft.dropdown.Option("Asistencia por estudiante"),
            ft.dropdown.Option("Asistencia por curso"),
            ft.dropdown.Option("Promedio notas por estudiante"),
            ft.dropdown.Option("Promedio notas por materia"),
            ft.dropdown.Option("Estadísticas notas por curso"),
        ],
        width=400
    )

    # Texto de ayuda
    info_text = ft.Text(value="", italic=True, color=ft.Colors.GREY_600) # ACTUALIZADO

    # Campos dinámicos
    id_est_field = ft.TextField(
        label="ID Estudiante",
        width=200,
        on_change=lambda e: actualizar_nombre(e, id_est_field, estudiante_nombre, Estudiante.obtener_nombre_completo)
    )
    estudiante_nombre = ft.Text(color=ft.Colors.BLUE_800) # ACTUALIZADO
    
    id_curso_field = ft.TextField(
        label="ID Curso",
        width=200,
        on_change=lambda e: actualizar_nombre(e, id_curso_field, curso_nombre, lambda id_val: (curso := Curso.obtener_por_id(id_val)) and curso.nombre if Curso.obtener_por_id(id_val) else None)
    )
    curso_nombre = ft.Text(color=ft.Colors.BLUE_800) # ACTUALIZADO
    
    id_mat_field = ft.TextField(
        label="ID Materia",
        width=200,
        on_change=lambda e: actualizar_nombre(e, id_mat_field, materia_nombre, Materia.obtener_nombre_materia)
    )
    materia_nombre = ft.Text(color=ft.Colors.BLUE_800) # ACTUALIZADO
    
    fecha_inicio = ft.TextField(
        label="Fecha inicio (YYYY-MM-DD)",
        width=220,
        hint_text="Ej: 2024-01-01"
    )
    fecha_fin = ft.TextField(
        label="Fecha fin (YYYY-MM-DD)",
        width=220,
        hint_text="Ej: 2024-12-31"
    )

    btn_generar = ft.ElevatedButton(
        text="Generar Reporte",
        icon=ft.Icons.INSERT_CHART, # ACTUALIZADO
        color=ft.Colors.WHITE,      # ACTUALIZADO
        bgcolor=ft.Colors.BLUE_600  # ACTUALIZADO
    )

    # Tabla de resultados
    # CORRECCIÓN: Inicializar con una columna por defecto
    table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(""))], 
        rows=[], 
        visible=False
    )

    def actualizar_nombre(e, control_id, control_nombre, funcion_obtener):
        """Actualiza el campo de nombre cuando cambia un ID"""
        try:
            if control_id.value.strip():
                nombre = funcion_obtener(int(control_id.value))
                control_nombre.value = nombre or "⚠️ ID no encontrado"
                control_nombre.color = ft.Colors.BLUE_800 if nombre else ft.Colors.RED # ACTUALIZADO
            else:
                control_nombre.value = ""
            page.update()
        except ValueError:
            control_nombre.value = "⚠️ ID inválido"
            control_nombre.color = ft.Colors.RED # ACTUALIZADO
            page.update()

    def actualizar_campos(e):
        """Muestra/oculta campos según el tipo de reporte"""
        # Resetear todos los campos
        for campo in [id_est_field, id_curso_field, id_mat_field, fecha_inicio, fecha_fin]:
            campo.visible = False
            campo.value = ""
        
        for nombre_display in [estudiante_nombre, curso_nombre, materia_nombre]: # Renombrada la variable para evitar confusión
            nombre_display.value = ""
        
        table.visible = False
        table.rows.clear()
        table.columns.clear()
        # CORRECCIÓN: Asegurar que la tabla tenga al menos una columna después de limpiarla
        table.columns.append(ft.DataColumn(ft.Text(""))) 

        # Configurar campos según reporte
        descripcion = ""
        if tipo_reporte.value == "Inscripción por cursos":
            descripcion = "Muestra cantidad de estudiantes inscritos en cada curso."
        
        elif tipo_reporte.value == "Asistencia por estudiante":
            id_est_field.visible = True
            fecha_inicio.visible = True
            fecha_fin.visible = True
            descripcion = "Asistencia de un estudiante específico. Fechas son opcionales."
        
        elif tipo_reporte.value == "Asistencia por curso":
            id_curso_field.visible = True
            fecha_inicio.visible = True
            fecha_fin.visible = True
            descripcion = "Asistencia general de un curso. Fechas son opcionales."
        
        elif tipo_reporte.value == "Promedio notas por estudiante":
            id_est_field.visible = True
            descripcion = "Promedio de notas por materia para un estudiante."
        
        elif tipo_reporte.value == "Promedio notas por materia":
            id_mat_field.visible = True
            descripcion = "Promedio general de todos los estudiantes en una materia."
        
        elif tipo_reporte.value == "Estadísticas notas por curso":
            id_curso_field.visible = True
            descripcion = "Estadísticas detalladas de notas por materia en un curso."

        info_text.value = descripcion
        page.update()

    tipo_reporte.on_change = actualizar_campos

    def formatear_fecha(fecha_str):
        """Intenta formatear fechas de texto a objeto date"""
        try:
            return date.fromisoformat(fecha_str) if fecha_str else None
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")

    def generar_reporte(e):
        try:
            table.rows.clear()
            table.columns.clear() # Limpiar columnas (incluyendo la de placeholder)

            report_generated = False # Flag para saber si se generaron columnas

            if tipo_reporte.value == "Inscripción por cursos":
                data = Reportes.reporte_inscripcion_cursos()
                table.columns = [
                    ft.DataColumn(ft.Text("Curso")),
                    ft.DataColumn(ft.Text("Estudiantes", text_align=ft.TextAlign.RIGHT))
                ]
                table.rows = [
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(row[1])),  # Nombre del curso
                        ft.DataCell(ft.Text(str(row[2]), text_align=ft.TextAlign.RIGHT))
                    ]) for row in data
                ]
                report_generated = True

            elif tipo_reporte.value == "Asistencia por estudiante":
                id_est = int(id_est_field.value)
                fi = formatear_fecha(fecha_inicio.value)
                ff = formatear_fecha(fecha_fin.value)
                data = Reportes.reporte_asistencia_por_estudiante(id_est, fi, ff)
                
                table.columns = [
                    ft.DataColumn(ft.Text("Estado")),
                    ft.DataColumn(ft.Text("Cantidad", text_align=ft.TextAlign.RIGHT))
                ]
                table.rows = [
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(k)),
                        ft.DataCell(ft.Text(str(v))), 
                    ]) for k, v in data.items()
                ]
                report_generated = True
            
            elif tipo_reporte.value == "Asistencia por curso":
                id_curso = int(id_curso_field.value)
                fi = formatear_fecha(fecha_inicio.value)
                ff = formatear_fecha(fecha_fin.value)
                data = Reportes.reporte_asistencia_por_curso(id_curso, fi, ff)
                
                table.columns = [
                    ft.DataColumn(ft.Text("Estado")),
                    ft.DataColumn(ft.Text("Cantidad", text_align=ft.TextAlign.RIGHT))
                ]
                table.rows = [
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(k)),
                        ft.DataCell(ft.Text(str(v))), 
                    ]) for k, v in data.items()
                ]
                report_generated = True

            elif tipo_reporte.value == "Promedio notas por estudiante":
                id_est = int(id_est_field.value)
                data = Reportes.reporte_promedio_notas_por_estudiante(id_est)
                
                table.columns = [
                    ft.DataColumn(ft.Text("Materia")),
                    ft.DataColumn(ft.Text("Promedio", text_align=ft.TextAlign.RIGHT))
                ]
                rows = []
                for materia_id, promedio in data:
                    nombre_materia = Materia.obtener_nombre_materia(materia_id) or f"Materia {materia_id}"
                    rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(nombre_materia)),
                            ft.DataCell(ft.Text(f"{promedio:.2f}")),
                        ]))
                table.rows = rows
                report_generated = True

            elif tipo_reporte.value == "Promedio notas por materia":
                id_mat = int(id_mat_field.value)
                promedio = Reportes.reporte_promedio_notas_por_materia(id_mat)
                
                table.columns = [
                    ft.DataColumn(ft.Text("Materia")),
                    ft.DataColumn(ft.Text("Promedio General", text_align=ft.TextAlign.RIGHT))
                ]
                nombre_materia = Materia.obtener_nombre_materia(id_mat) or f"Materia {id_mat}"
                table.rows = [
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(nombre_materia)),
                        ft.DataCell(ft.Text(f"{promedio:.2f}")),
                    ])
                ]
                report_generated = True

            elif tipo_reporte.value == "Estadísticas notas por curso":
                id_curso = int(id_curso_field.value)
                data = Reportes.reporte_estadisticas_notas_por_curso(id_curso)
                
                table.columns = [
                    ft.DataColumn(ft.Text("Materia")),
                    ft.DataColumn(ft.Text("Promedio", text_align=ft.TextAlign.RIGHT)),
                    ft.DataColumn(ft.Text("Mínima", text_align=ft.TextAlign.RIGHT)),
                    ft.DataColumn(ft.Text("Máxima", text_align=ft.TextAlign.RIGHT))
                ]
                rows = []
                for materia_id, avg, min_val, max_val in data:
                    nombre_materia = Materia.obtener_nombre_materia(materia_id) or f"Materia {materia_id}"
                    rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(nombre_materia)),
                            ft.DataCell(ft.Text(f"{avg:.2f}")),
                            ft.DataCell(ft.Text(f"{min_val:.2f}")),
                            ft.DataCell(ft.Text(f"{max_val:.2f}")),
                        ]))
                table.rows = rows
                report_generated = True

            if not report_generated or not table.columns:
                # Si por alguna razón no se generaron columnas (ej. tipo_reporte.value es None o no coincide)
                # o los datos resultaron en no columnas, añadir una columna por defecto.
                table.columns = [ft.DataColumn(ft.Text("No hay datos para mostrar o tipo de reporte no seleccionado."))]
                table.rows = []
            
            table.visible = True
            page.update()

        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Error", color=ft.Colors.RED), # ACTUALIZADO
                content=ft.Text(str(ex))
            )
            page.dialog.open = True
            # Opcional: resetear la tabla a un estado seguro si es necesario
            # table.columns = [ft.DataColumn(ft.Text(""))]
            # table.rows.clear()
            # table.visible = False
            page.update()

    btn_generar.on_click = generar_reporte
    
    # Llamar a actualizar_campos al inicio para configurar la visibilidad inicial de los campos
    # y asegurar que la tabla esté correctamente inicializada para la primera vista.
    actualizar_campos(None) # Pasar None o un objeto evento simulado si es necesario

    # Layout
    return ft.Column(
        controls=[
            ft.Container(
                content=ft.Column([
                    tipo_reporte,
                    info_text,
                    ft.Row([
                        ft.Column([id_est_field, estudiante_nombre]),
                        ft.Column([id_curso_field, curso_nombre]),
                        ft.Column([id_mat_field, materia_nombre]),
                    ], spacing=20, visible=True), # Asegurar que el Row que contiene los campos ID sea visible
                                                  # La visibilidad de los campos individuales se maneja en actualizar_campos
                    ft.Row([fecha_inicio, fecha_fin], spacing=20, visible=True), # Idem
                    ft.Container(btn_generar, padding=10),
                    ft.Divider(),
                    table
                ], spacing=15),
                padding=30,
                expand=True
            )
        ],
        expand=True
    )


def main(page: ft.Page):
    page.title = "Sistema de Reportes Escolares"
    page.theme_mode = ft.ThemeMode.LIGHT # O ft.ThemeMode.DARK o ft.ThemeMode.SYSTEM
 
    page.add(reportes_view(page))

if __name__ == "__main__":
    ft.app(target=main)