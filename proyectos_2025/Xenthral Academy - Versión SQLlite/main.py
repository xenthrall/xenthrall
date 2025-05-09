import flet as ft
from models.conexion_sqlite import inicializar_db_colegio

# VIEWS - Asegúrate de que estas importaciones funcionen según tu estructura de proyecto.
from views.inicio import inicio 
from views.cursos import cursos
from views.materias import materias
from views.estudiantes import estudiantes
from views.profesores import profesores
from views.notas_view import notas_view
from views.asistencias_view import asistencias_view
from views.reportes import reportes_view
# Asegúrate que views/acerca_de.py contiene la versión flet_acerca_de_stateful_v3
from views.acerca_de import acerca_de_view 

# Lista de opciones del menú lateral
def menu_lateral():
    return [
        ft.NavigationRailDestination(
            icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Inicio" # Corregido
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.SCHOOL_OUTLINED, selected_icon=ft.Icons.SCHOOL, label="Cursos" # Corregido
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.BOOK_OUTLINED, selected_icon=ft.Icons.BOOK, label="Materias" # Corregido
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.PEOPLE_OUTLINE, selected_icon=ft.Icons.PEOPLE, label="Estudiantes" # Corregido
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Profesores" # Corregido
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.EVENT_NOTE_OUTLINED, selected_icon=ft.Icons.EVENT_NOTE, label="Asistencia" # Corregido
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.GRADE_OUTLINED, selected_icon=ft.Icons.GRADE, label="Notas" # Corregido
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.INSIGHTS_OUTLINED, selected_icon=ft.Icons.INSIGHTS, label="Reportes" # Corregido
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.INFO_OUTLINE, selected_icon=ft.Icons.INFO, label="Acerca de" # Corregido
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.EXIT_TO_APP_OUTLINED, selected_icon=ft.Icons.EXIT_TO_APP, label="Salir" # Corregido
        ),
    ]

def main(page: ft.Page):
    inicializar_db_colegio()
    page.title = "Xenthrall - Academy"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREY_100 # Corregido

    # Estado global de la aplicación
    app_state = {
        "audio_control": ft.Audio( # ft.Audio está obsoleto, considerar migrar a flet_audio
            src="assets/song.mp3", 
            autoplay=False,
        ),
        "is_music_playing": False,
        "acerca_de_view_is_active": False,
        "acerca_de_animation_task": None,
        "acerca_de_image_control": None,
        "acerca_de_play_button": None,
        "acerca_de_pause_button": None,
        "current_view_index": -1, 
    }

    if app_state["audio_control"] not in page.overlay:
        page.overlay.append(app_state["audio_control"])

    contenido_principal = ft.Column([], expand=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def close_app_action(): # Renombrada en versiones anteriores, puedes usar close_app si prefieres
        if app_state.get("is_music_playing"): # Usar .get() para seguridad
            audio_ctrl = app_state.get("audio_control")
            if audio_ctrl:
                audio_ctrl.pause()
        
        animation_task = app_state.get("acerca_de_animation_task")
        if animation_task and not animation_task.done():
            animation_task.cancel()
        page.window_close()

    def cambiar_vista(index):
        # --- Limpieza de la vista anterior (específicamente para "Acerca de") ---
        if app_state.get("current_view_index") == 8: 
            app_state["acerca_de_view_is_active"] = False 
            
            animation_task = app_state.get("acerca_de_animation_task")
            if animation_task and not animation_task.done():
                animation_task.cancel()
                app_state["acerca_de_animation_task"] = None 
            
            image_control = app_state.get("acerca_de_image_control")
            if image_control:
                image_control.scale = ft.transform.Scale(1.0)
                # No actualizar page aquí, el control ya no es visible directamente.
            
            app_state["acerca_de_image_control"] = None
            app_state["acerca_de_play_button"] = None
            app_state["acerca_de_pause_button"] = None
        
        app_state["current_view_index"] = index 
        contenido_principal.controls.clear()

        # --- Cargar la nueva vista ---
        if index == 0:
            contenido_principal.controls.append(inicio()) # Asumiendo que inicio() no necesita app_state
        elif index == 1:
            contenido_principal.controls.append(cursos(page)) # Asumiendo que cursos() no necesita app_state
        elif index == 2:
            contenido_principal.controls.append(materias(page)) # Asumiendo que materias() no necesita app_state
        elif index == 3:
            contenido_principal.controls.append(estudiantes(page)) # Asumiendo que estudiantes() no necesita app_state
        elif index == 4:
            contenido_principal.controls.append(profesores(page)) # Asumiendo que profesores() no necesita app_state
        elif index == 5:
            contenido_principal.controls.append(asistencias_view(page)) # Asumiendo que asistencias_view() no necesita app_state
        elif index == 6:
            contenido_principal.controls.append(notas_view(page)) # Asumiendo que notas_view() no necesita app_state
        elif index == 7:
            contenido_principal.controls.append(reportes_view(page)) # Asumiendo que reportes_view() no necesita app_state
        elif index == 8: # Vista "Acerca de"
            app_state["acerca_de_view_is_active"] = True 
            contenido_principal.controls.append(acerca_de_view(page, app_state))
        elif index == 9: # Salir
            close_app_action() # Usar el nombre corregido de la función
            return 
        else:
            contenido_principal.controls.append(ft.Text("Contenido no disponible"))

        page.update()

    nav = ft.NavigationRail(
        selected_index=0, 
        width=120,
        destinations=menu_lateral(),
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=ft.Colors.TEAL_200, # Corregido
        extended=False,
        on_change=lambda e: cambiar_vista(e.control.selected_index),
    )
    
    cambiar_vista(0) 

    layout = ft.Row(
        [
            nav,
            ft.VerticalDivider(width=1),
            ft.Container(
                content=contenido_principal,
                expand=True,
                padding=ft.padding.all(1), 
                alignment=ft.alignment.center
            ),
        ],
        expand=True,
    )

    page.add(layout) 


ft.app(target=main)