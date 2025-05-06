# views/dashboard.py
import flet as ft

#VIEWS
from views.inicio import inicio
from views.cursos import cursos
from views.materias import materias

from views.estudiantes import estudiantes
from views.profesores import profesores


# Lista de opciones del menú lateral
def menu_lateral():
    return [
        # Vista principal / logoooo
        ft.NavigationRailDestination(
            icon=ft.Icons.HOME_OUTLINED,
            selected_icon=ft.Icons.HOME,
            label="Inicio",
        ),

        # Gestión de cursos
        ft.NavigationRailDestination(
            icon=ft.Icons.SCHOOL_OUTLINED,
            selected_icon=ft.Icons.SCHOOL,
            label="Cursos",
        ),

        # Gestión de materias
        ft.NavigationRailDestination(
            icon=ft.Icons.BOOK_OUTLINED,
            selected_icon=ft.Icons.BOOK,
            label="Materias",
        ),

        # Gestión de estudiantes
        ft.NavigationRailDestination(
            icon=ft.Icons.PEOPLE_OUTLINE,
            selected_icon=ft.Icons.PEOPLE,
            label="Estudiantes",
        ),

        # Gestión de profesores
        ft.NavigationRailDestination(
            icon=ft.Icons.PERSON_OUTLINE,
            selected_icon=ft.Icons.PERSON,
            label="Profesores",
        ),

        # Registro de asistencia
        ft.NavigationRailDestination(
            icon=ft.Icons.EVENT_NOTE,
            selected_icon=ft.Icons.EVENT,
            label="Asistencia",
        ),

        # Registro de calificaciones
        ft.NavigationRailDestination(
            icon=ft.Icons.GRADE_OUTLINED,
            selected_icon=ft.Icons.GRADE,
            label="Notas",
        ),

        # Reportes y estadísticas
        ft.NavigationRailDestination(
            icon=ft.Icons.INSIGHTS_OUTLINED,
            selected_icon=ft.Icons.INSIGHTS,
            label="Reportes",
        ),

        # Información de la aplicación
        ft.NavigationRailDestination(
            icon=ft.Icons.INFO_OUTLINE,
            selected_icon=ft.Icons.INFO,
            label="Acerca de",
        ),

        # Configuración general
        ft.NavigationRailDestination(
            icon=ft.Icons.EXIT_TO_APP_OUTLINED,
            selected_icon=ft.Icons.EXIT_TO_APP,
            label="Salir",
            
        ),
    ]


def main(page: ft.Page):
    page.title = "Colegio"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.GREY_100

    # Estado actual de la vista seleccionada
    contenido_principal = ft.Column([], expand=True)  # Aquí se cargara vistas completas

    #Cerrar sesion
    def close_app():
        page.window.close()
    
    # Mostrar contenido según la navegación lateral
    def cambiar_vista(index):
        contenido_principal.controls.clear()

        if index == 0:
            contenido_principal.controls.append(inicio())  #Inicio
        elif index == 1:
            contenido_principal.controls.append(cursos(page))  # Vista de cursos

        elif index == 2:
            contenido_principal.controls.append(materias(page)) #Vista del modulo materias

        elif index == 3:
            contenido_principal.controls.append(estudiantes(page)) #Vista del modulo estudiantes

        elif index == 4:
            contenido_principal.controls.append(profesores(page)) #Vista del modulo profesores


        elif index == 8:
            contenido_principal.controls.append(ft.Text("Desarrollado por la empresa XENTHRALL 👽🚀"))
        elif index == 9:
            close_app()
        else:
            contenido_principal.controls.append(ft.Text("Contenido no disponible"))

        page.update()

        
    # Menú lateral (NavigationRail)
    nav = ft.NavigationRail(
        selected_index=0,
        width=120,
        destinations=menu_lateral(),#Obtenemos las secciones
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor=ft.Colors.TEAL_200,
        extended=False,
        on_change=lambda e: cambiar_vista(e.control.selected_index),
    )
    contenido_principal.controls.append(inicio())

    # Layout principal: menú lateral + contenido
    layout = ft.Row(
        [
            nav,
            ft.VerticalDivider(width=1),
            ft.Container(
                content=contenido_principal,
                expand=True,
            ),
        ],
        expand=True,
    )

    # Layout principal: sidebar + contenido
    page.controls = [layout]
    page.update()



    page.add()

ft.app(target=main)