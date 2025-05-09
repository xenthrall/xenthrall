import flet as ft
from datetime import date, datetime
# Asegúrate que la ruta a models.database es correcta según tu estructura de proyecto
# Ejemplo: from ..models.database import Curso, Estudiante, Asistencia
# Si asistencias_view.py está en una carpeta 'views' y 'models' está al mismo nivel:
from models.database import Curso, Estudiante, Asistencia # Asegúrate que esto funciona

# Estados de asistencia posibles
ESTADOS_ASISTENCIA = ["Presente", "Ausente", "Tarde"]

def asistencias_view(page: ft.Page):
    """
    Crea la vista para la gestión de asistencias de estudiantes.
    """

    # --- Controles de Selección ---
    cursos_dropdown = ft.Dropdown(
        label="Seleccione un Curso",
        hint_text="Elija un curso para ver sus estudiantes",
        options=[], # Se llenarán dinámicamente
        width=400,
        on_change=lambda e: cargar_estudiantes_asistencia() # Recargar al cambiar curso
    )

    def abrir_dialogo_datepicker(dp: ft.DatePicker):
        dp.open = True
        page.update()

    def datepicker_on_change(e):
        """Actualiza el botón de fecha y recarga los estudiantes."""
        if fecha_asistencia_picker.value: # El valor ya es un datetime
            fecha_seleccionada = fecha_asistencia_picker.value.date() # Convertir datetime a date
            fecha_display_button.text = f"Fecha: {fecha_seleccionada.strftime('%Y-%m-%d')}"
            cargar_estudiantes_asistencia() # Asegúrate que esto no cause un bucle si on_change se dispara al abrir
        else: # Si el usuario cancela el DatePicker, value podría ser None
            # Mantener la fecha anterior o la fecha de hoy si es la primera vez
            current_picker_date_obj = fecha_asistencia_picker.value
            if current_picker_date_obj:
                 fecha_display_button.text = f"Fecha: {current_picker_date_obj.date().strftime('%Y-%m-%d')}"
            else:
                 fecha_display_button.text = f"Fecha: {date.today().strftime('%Y-%m-%d')}"


        page.update()


    fecha_asistencia_picker = ft.DatePicker(
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
        # current_date no se actualiza solo, se pone al inicio. El valor se obtiene de 'value'
        # value=datetime.combine(date.today(), datetime.min.time()), # Establecer valor inicial
        help_text="Seleccione la fecha de asistencia",
        on_change=datepicker_on_change,
        # on_dismiss=lambda e: print("DatePicker dismissed"), # Para debug si es necesario
    )
    # El DatePicker necesita estar en overlay para mostrarse correctamente.
    if fecha_asistencia_picker not in page.overlay:
        page.overlay.append(fecha_asistencia_picker)


    fecha_display_button = ft.ElevatedButton(
        f"Fecha: {date.today().strftime('%Y-%m-%d')}",
        icon=ft.Icons.CALENDAR_MONTH, # CORREGIDO
        on_click=lambda _: abrir_dialogo_datepicker(fecha_asistencia_picker), # CORREGIDO
        width=200
    )
    # Establecer el valor inicial del DatePicker para que on_change funcione consistentemente
    # y para que el botón refleje la fecha con la que el picker inicia.
    fecha_asistencia_picker.value = datetime.combine(date.today(), datetime.min.time())


    # --- Área de Lista de Estudiantes ---
    estudiantes_list_view = ft.ListView(expand=True, spacing=10)

    # --- Indicador de Carga ---
    progreso_carga = ft.ProgressRing(visible=False, width=20, height=20)

    # --- Botón de Acción Principal ---
    btn_guardar_asistencia = ft.ElevatedButton(
        text="Guardar Asistencia",
        icon=ft.Icons.SAVE, # CORREGIDO
        on_click=lambda e: guardar_asistencias_click(),
        bgcolor=ft.Colors.BLUE_600, # CORREGIDO
        color=ft.Colors.WHITE, # CORREGIDO
        visible=False # Solo visible cuando hay estudiantes cargados
    )

    # --- Mensajes de Feedback ---
    feedback_text = ft.Text("", italic=True, color=ft.Colors.GREEN_700) # CORREGIDO

    # --- Almacenamiento temporal de datos ---
    estudiantes_data_actual = {}


    def cargar_cursos():
        """Carga los cursos en el Dropdown."""
        try:
            cursos = Curso.obtener_todos()
            if cursos:
                cursos_dropdown.options = [
                    ft.dropdown.Option(key=curso[0], text=curso[1]) for curso in cursos
                ]
            else:
                cursos_dropdown.options = []
                cursos_dropdown.hint_text = "No hay cursos disponibles"
        except Exception as e:
            mostrar_feedback(f"Error al cargar cursos: {e}", error=True)
            cursos_dropdown.options = []
        page.update()

    def mostrar_feedback(mensaje: str, error: bool = False, duracion_ms: int = 3000):
        """Muestra un mensaje de feedback al usuario."""
        feedback_text.value = mensaje
        feedback_text.color = ft.Colors.RED_600 if error else ft.Colors.GREEN_700 # CORREGIDO
        feedback_text.visible = True
        page.update()
        # Opcional: ocultar después de un tiempo si es necesario
        # import time
        # time.sleep(duracion_ms / 1000)
        # feedback_text.visible = False
        # page.update()


    def cargar_estudiantes_asistencia():
        """Carga los estudiantes del curso y fecha seleccionados, y su asistencia si existe."""
        id_curso_seleccionado = cursos_dropdown.value
        fecha_seleccionada_dt = fecha_asistencia_picker.value

        estudiantes_list_view.controls.clear()
        estudiantes_data_actual.clear()
        btn_guardar_asistencia.visible = False
        feedback_text.visible = False
        progreso_carga.visible = True
        page.update()

        if not id_curso_seleccionado:
            progreso_carga.visible = False
            mostrar_feedback("Por favor, seleccione un curso.", error=True)
            page.update()
            return

        if not fecha_seleccionada_dt: # Si DatePicker.value es None
            progreso_carga.visible = False
            mostrar_feedback("Por favor, seleccione una fecha.", error=True)
            page.update()
            return

        fecha_seleccionada = fecha_seleccionada_dt.date()

        try:
            estudiantes = Estudiante.obtener_por_id_curso(int(id_curso_seleccionado))

            if not estudiantes:
                estudiantes_list_view.controls.append(ft.Text("No hay estudiantes en este curso."))
                progreso_carga.visible = False
                page.update()
                return

            for est_row in estudiantes:
                id_estudiante = est_row[0]
                nombre_completo = f"{est_row[1]} {est_row[2]}"

                asistencia_existente = Asistencia.obtener_asistencia_por_estudiante_y_fecha(id_estudiante, fecha_seleccionada)

                estado_actual = None
                id_asistencia_db = None

                if asistencia_existente:
                    id_asistencia_db = asistencia_existente[0]
                    estado_actual = asistencia_existente[1]

                radios_estado = [
                    ft.Radio(value=estado, label=estado) for estado in ESTADOS_ASISTENCIA
                ]
                grupo_estado = ft.RadioGroup(
                    content=ft.Row(controls=radios_estado, spacing=15),
                    value=estado_actual
                )

                estudiantes_data_actual[id_estudiante] = {
                    'control_estado': grupo_estado,
                    'id_asistencia_existente': id_asistencia_db,
                    'nombre': nombre_completo
                }

                estudiante_card = ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Row(
                            controls=[
                                ft.Text(nombre_completo, weight=ft.FontWeight.BOLD, expand=1),
                                grupo_estado
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    )
                )
                estudiantes_list_view.controls.append(estudiante_card)

            btn_guardar_asistencia.visible = True if estudiantes else False

        except Exception as e:
            mostrar_feedback(f"Error al cargar estudiantes: {e}", error=True)
            print(f"Error detallado cargando estudiantes: {e}") # Para debugging en consola
        finally:
            progreso_carga.visible = False
            page.update()

    def guardar_asistencias_click():
        """Maneja el evento de clic del botón Guardar Asistencia."""
        id_curso_seleccionado = cursos_dropdown.value
        fecha_seleccionada_dt = fecha_asistencia_picker.value

        if not id_curso_seleccionado or not fecha_seleccionada_dt:
            mostrar_feedback("Curso o fecha no seleccionados.", error=True)
            return

        fecha_seleccionada = fecha_seleccionada_dt.date()
        progreso_carga.visible = True
        btn_guardar_asistencia.disabled = True
        page.update()

        registros_guardados = 0
        registros_actualizados = 0
        errores = 0

        try:
            for id_estudiante, data in estudiantes_data_actual.items():
                estado_seleccionado = data['control_estado'].value
                id_asistencia_existente = data['id_asistencia_existente']

                if not estado_seleccionado:
                    continue

                try:
                    if id_asistencia_existente:
                        Asistencia.actualizar_asistencia(id_asistencia_existente, estado_seleccionado)
                        registros_actualizados += 1
                    else:
                        Asistencia.registrar_asistencia(id_estudiante, fecha_seleccionada, estado_seleccionado)
                        registros_guardados += 1
                except Exception as e_detalle:
                    errores += 1
                    print(f"Error guardando asistencia para ID {id_estudiante}: {e_detalle}")

            if errores > 0:
                mensaje = f"Guardado con {errores} error(es)."
                if registros_guardados > 0:
                    mensaje += f" {registros_guardados} nuevo(s)."
                if registros_actualizados > 0:
                    mensaje += f" {registros_actualizados} actualizado(s)."
                mostrar_feedback(mensaje, error=True)
            else:
                mensaje = "Asistencia guardada exitosamente."
                if registros_guardados > 0:
                    mensaje += f" ({registros_guardados} nuevo(s))"
                if registros_actualizados > 0:
                    mensaje += f" ({registros_actualizados} actualizado(s))"
                mostrar_feedback(mensaje)

            cargar_estudiantes_asistencia() # Recargar para reflejar los cambios y nuevos IDs de asistencia

        except Exception as e:
            mostrar_feedback(f"Error general al guardar: {e}", error=True)
            print(f"Error general detallado guardando: {e}")
        finally:
            progreso_carga.visible = False
            btn_guardar_asistencia.disabled = False
            page.update()

    # --- Carga Inicial ---
    cargar_cursos()

    # --- Layout de la Vista ---
    return ft.Column(
        expand=True,
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Gestión de Asistencia", size=24, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [cursos_dropdown, fecha_display_button, progreso_carga],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    ),
                    ft.Divider(),
                    feedback_text,
                ]),
                padding=ft.padding.only(bottom=10)
            ),
            estudiantes_list_view,
            ft.Container(
                content=btn_guardar_asistencia,
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(vertical=10)
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        spacing=10
    )