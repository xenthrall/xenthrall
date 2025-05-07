import flet as ft
import asyncio

from database import Proyecto, Empleados, Tarea
from tablas import TablaProyectos, TablaEmpleados, TablaTareas

def formulario_registro_tarea(page: ft.Page, tabla_tareas: TablaTareas):
    
    """
    PARAMS:
        page: ft.Page,  
        def __init__(self,id_proyecto, id_empleado, fecha_inicio, fecha_fin, descripcion = None, estado = None, id_tarea = None):
    """

    estado = ft.TextField(label="Estado",expand=1)
    descripcion = ft.TextField(label="Descripcion*",expand=1)

    id_proyecto = ft.TextField(label="ID PROYECTO",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2)
    id_empleado = ft.TextField(label="ID EMPLEADO",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2)

    #Campos fecha inicio de la tarea
    año_inicio = ft.TextField(label="Año",expand=2,input_filter=ft.NumbersOnlyInputFilter(),max_length=4)
    mes_inicio = ft.TextField(label="Mes",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2)
    dia_inicio = ft.TextField(label="Dia",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2)

    contenedor_fecha_inicio = ft.Container(
        content=ft.Row([año_inicio,mes_inicio,dia_inicio]),
        expand=1
        )

    #Campos fecha fin del proyecto
    año_fin = ft.TextField(label="Año",expand=2,input_filter=ft.NumbersOnlyInputFilter(),max_length=4)
    mes_fin = ft.TextField(label="Mes",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2)
    dia_fin = ft.TextField(label="Dia",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2)

    contenedor_fecha_final = ft.Container(
        content=ft.Row([año_fin,mes_fin,dia_fin]),
        expand=1
        )
    

    estado_registro = ft.Text(value="", color=ft.colors.GREEN_600)

    id_tarea_actualizar = ft.TextField(label="ID tarea actualizar",expand=1)

    informacion_para_actualizar = ft.Row([ft.Text("Digitar ID para Actualizar: ",expand=2), id_tarea_actualizar,estado])

    
    async def actualizar_proyecto(e):
        if  not id_tarea_actualizar.value.strip():
            estado_registro.value = "ID de la tarea Obligatorio"
            estado_registro.color = ft.colors.RED
            page.update()
            await asyncio.sleep(2)
            estado_registro.value = ""
        else:
            try:
                    #Una pequeña verificacion de si se quiere actualizar la fecha fin del proyecto
                    if año_fin.value.strip() and año_fin.value.strip() and dia_fin.value.strip():
                        fecha_fin = f"{año_fin.value.zfill(4)}-{mes_fin.value.zfill(2)}-{mes_fin.value.zfill(2)}"

                    else:
                        fecha_fin = None

                    Tarea.actualizar_registro(estado.value,fecha_fin,id_tarea_actualizar.value)



                    

                    tabla_tareas.actualizar_tabla()

                    estado_registro.value = "Tarea actualizada exitosamente"
                    estado_registro.color = ft.colors.GREEN
                    page.update()

                    await asyncio.sleep(2)
                    estado_registro.value = ""

                    estado.value = ""
                    descripcion.value = ""

                    año_inicio.value = ""
                    mes_inicio.value = ""
                    dia_inicio.value = ""

                    año_fin.value = ""
                    mes_fin.value = ""
                    dia_fin.value = ""
                        
                        

                   

            except Exception as ex:
                estado_registro.value = f"Error: {ex}"

        page.update()


    # Función para insertar tarea
    async def insertar_dato(e):
        """Guarda el nuevo proyecto en la base de datos """


        if not id_proyecto.value or not id_empleado.value:
            estado_registro.value = "IDs proyecto y empleado  Obligatorio"
            estado_registro.color = ft.colors.RED
            page.update()
            await asyncio.sleep(2)
            estado_registro.value = ""
        else:
            try:
                if not año_inicio.value or not mes_inicio.value or not dia_inicio.value:
                    estado_registro.value = "Fecha inicio obligatoria"
                    estado_registro.color = ft.colors.RED
                    page.update()
                    await asyncio.sleep(2)
                    estado_registro.value = ""
                else:
                    #Una pequeña verificacion de si se quiere registrar la fecha fin del proyecto
                    if año_fin.value.strip() and año_fin.value.strip() and dia_fin.value.strip():
                        fecha_fin = f"{año_fin.value.zfill(4)}-{mes_fin.value.zfill(2)}-{mes_fin.value.zfill(2)}"

                    else:
                        fecha_fin = None


                    fecha_inicio = f"{año_inicio.value.zfill(4)}-{mes_inicio.value.zfill(2)}-{dia_inicio.value.zfill(2)}"

                    nueva_tarea = Tarea(id_proyecto.value, id_empleado.value, fecha_inicio, fecha_fin, descripcion.value, estado="En curso")
                    

                    nueva_tarea.guardar_registro()
                    tabla_tareas.actualizar_tabla()

                    estado_registro.value = "Tarea asignada exitosamente"
                    estado_registro.color = ft.colors.GREEN
                    page.update()

                    await asyncio.sleep(2)
                    estado_registro.value = ""

                    estado.value = ""
                    descripcion.value = ""

                    id_empleado.value = ""
                    id_proyecto.value = ""

                    año_inicio.value = ""
                    mes_inicio.value = ""
                    dia_inicio.value = ""

                    año_fin.value = ""
                    mes_fin.value = ""
                    dia_fin.value = ""
                    id_tarea_actualizar.value = ""
                        
                        

                   

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

    boton_actualizar =ft.ElevatedButton(
        text="Actualizar",
        icon=ft.icons.UPDATE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=actualizar_proyecto,
    )

    

    # Card con diseño del formulario
    formulario = ft.Container(
        expand=1,
            padding=ft.padding.all(24),
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Asignar Tarea", size=24, weight="bold"),

                    ft.Container(content=ft.Row([id_proyecto, id_empleado])),

                    ft.Container(descripcion),
                    
                    ft.Container(content=ft.Row([ft.Text("Fecha de inicio:",expand=1), ft.Text("Fecha de Fin:",expand=1)])),
                    ft.Container(content=ft.Row([contenedor_fecha_inicio,contenedor_fecha_final])),
                    boton_guardar,
                    estado_registro,
                    informacion_para_actualizar,
                    boton_actualizar,
                    
                ],
            ),
        )

    return ft.Column(controls=[formulario], alignment=ft.MainAxisAlignment.CENTER,expand=1)

def formulario_registro_empleados(page: ft.Page, tabla_empleado: TablaEmpleados):

    """
    Crea y devuelve el formulario para registrar nuevos PROYECTOS.
    def __init__(self, nombre, descripcion, fecha_inicio, fecha_fin, id_proyecto = None):

    Args:
        
    Returns:
        ft.Row: Una fila que contiene el formulario de registro centrado.
    """
    # Campos del formulario
    nombre = ft.TextField(label="Nombres*",expand=1)
    correo = ft.TextField(label="Correo",expand=1)
    telefono = ft.TextField(label="Telefono",expand=1)


    estado_registro = ft.Text(value="", color=ft.colors.GREEN_600)

    id_empleado_actualizar = ft.TextField(label="ID empleado actualizar",expand=1)

    informacion_para_actualizar = ft.Row([ft.Text("Digitar ID para Actualizar: ",expand=2), id_empleado_actualizar])

    
    async def actualizar_proyecto(e):
        if not nombre.value.strip() or not id_empleado_actualizar.value.strip():
            estado_registro.value = "Nombre y ID del empleado Obligatorio"
            estado_registro.color = ft.colors.RED
            page.update()
            await asyncio.sleep(2)
            estado_registro.value = ""
        else:
            try:


                    empleado = Empleados(nombre.value, correo.value, telefono.value, id_empleado=id_empleado_actualizar.value)
                    

                    empleado.actualizar_registro()
                    tabla_empleado.actualizar_tabla()

                    estado_registro.value = "Empleado actualizado exitosamente"
                    estado_registro.color = ft.colors.GREEN
                    page.update()

                    await asyncio.sleep(2)
                    estado_registro.value = ""

                    nombre.value = ""
                    correo.value = ""

                    telefono.value = ""
                    
                    id_empleado_actualizar.value = ""
                        
                        

                   

            except Exception as ex:
                estado_registro.value = f"Error: {ex}"

        page.update()


    # Función para insertar proyecto
    async def insertar_dato(e):
        """Guarda el nuevo empleado en la base de datos """


        if not nombre.value.strip():
            estado_registro.value = "Nombre del empleado Obligatorio"
            estado_registro.color = ft.colors.RED
            page.update()
            await asyncio.sleep(2)
            estado_registro.value = ""
        else:
            try:

                    nuevo_empleado = Empleados(nombre.value, correo.value, telefono.value)
                    

                    nuevo_empleado.guardar_registro()
                    tabla_empleado.actualizar_tabla()

                    estado_registro.value = "Empleado registrado exitosamente"
                    estado_registro.color = ft.colors.GREEN
                    page.update()

                    await asyncio.sleep(2)
                    estado_registro.value = ""

                    nombre.value = ""
                    correo.value = ""

                    telefono.value = ""
                    
                    id_empleado_actualizar.value = ""
                        
                        

                   

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

    boton_actualizar =ft.ElevatedButton(
        text="Actualizar",
        icon=ft.icons.UPDATE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=actualizar_proyecto,
    )

    

    # Card con diseño del formulario
    formulario = ft.Container(
        expand=1,
            padding=ft.padding.all(24),
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Registrar Empleado", size=24, weight="bold"),
                    ft.Container(content=ft.Row([nombre])),
                    ft.Container(content=ft.Row([correo,telefono])),
                    boton_guardar,
                    estado_registro,
                    informacion_para_actualizar,
                    boton_actualizar,
                    
                ],
            ),
        )

    return ft.Column(controls=[formulario], alignment=ft.MainAxisAlignment.CENTER,expand=1)

def formulario_registro_proyecto(page: ft.Page, tabla_proyecto: TablaProyectos):

    """
    Crea y devuelve el formulario para registrar nuevos PROYECTOS.
    def __init__(self, nombre, descripcion, fecha_inicio, fecha_fin, id_proyecto = None):

    Args:
        
    Returns:
        ft.Row: Una fila que contiene el formulario de registro centrado.
    """
    # Campos del formulario
    nombre = ft.TextField(label="Nombres*",expand=1)
    descripcion = ft.TextField(label="Descripcion*",expand=1)

    #Campos fecha inicio del proyecto
    año_inicio = ft.TextField(label="Año",expand=2,input_filter=ft.NumbersOnlyInputFilter(),max_length=4)
    mes_inicio = ft.TextField(label="Mes",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2)
    dia_inicio = ft.TextField(label="Dia",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2)

    contenedor_fecha_inicio = ft.Container(
        content=ft.Row([año_inicio,mes_inicio,dia_inicio]),
        expand=1
        )

    #Campos fecha fin del proyecto
    año_fin = ft.TextField(label="Año",expand=2,input_filter=ft.NumbersOnlyInputFilter(),max_length=4)
    mes_fin = ft.TextField(label="Mes",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2)
    dia_fin = ft.TextField(label="Dia",expand=1,input_filter=ft.NumbersOnlyInputFilter(),max_length=2)

    contenedor_fecha_final = ft.Container(
        content=ft.Row([año_fin,mes_fin,dia_fin]),
        expand=1
        )
    

    estado_registro = ft.Text(value="", color=ft.colors.GREEN_600)

    id_proyecto_actualizar = ft.TextField(label="ID proyecto actualizar",expand=1)

    informacion_para_actualizar = ft.Row([ft.Text("Digitar ID para Actualizar: ",expand=2), id_proyecto_actualizar])

    
    async def actualizar_proyecto(e):
        if not nombre.value.strip() or not id_proyecto_actualizar.value.strip():
            estado_registro.value = "Nombre, Descripcion y ID del proyecto Obligatorio"
            estado_registro.color = ft.colors.RED
            page.update()
            await asyncio.sleep(2)
            estado_registro.value = ""
        else:
            try:
                if not año_inicio.value or not mes_inicio.value or not dia_inicio.value:
                    estado_registro.value = "Fecha inicio obligatoria"
                    estado_registro.color = ft.colors.RED
                    page.update()
                    await asyncio.sleep(2)
                    estado_registro.value = ""
                else:
                    #Una pequeña verificacion de si se quiere registrar la fecha fin del proyecto
                    if año_fin.value.strip() and año_fin.value.strip() and dia_fin.value.strip():
                        fecha_fin = f"{año_fin.value.zfill(4)}-{mes_fin.value.zfill(2)}-{mes_fin.value.zfill(2)}"

                    else:
                        fecha_fin = None


                    fecha_inicio = f"{año_inicio.value.zfill(4)}-{mes_inicio.value.zfill(2)}-{dia_inicio.value.zfill(2)}"

                    nuevo_proyecto = Proyecto(nombre.value, descripcion.value, fecha_inicio, fecha_fin, id_proyecto=id_proyecto_actualizar.value)
                    

                    nuevo_proyecto.actualizar_registro()
                    tabla_proyecto.actualizar_tabla()

                    estado_registro.value = "Proyecto actualizado exitosamente"
                    estado_registro.color = ft.colors.GREEN
                    page.update()

                    await asyncio.sleep(2)
                    estado_registro.value = ""

                    nombre.value = ""
                    descripcion.value = ""

                    año_inicio.value = ""
                    mes_inicio.value = ""
                    dia_inicio.value = ""

                    año_fin.value = ""
                    mes_fin.value = ""
                    dia_fin.value = ""
                        
                        

                   

            except Exception as ex:
                estado_registro.value = f"Error: {ex}"

        page.update()


    # Función para insertar proyecto
    async def insertar_dato(e):
        """Guarda el nuevo proyecto en la base de datos """


        if not nombre.value.strip():
            estado_registro.value = "Nombre del proyecto Obligatorio"
            estado_registro.color = ft.colors.RED
            page.update()
            await asyncio.sleep(2)
            estado_registro.value = ""
        else:
            try:
                if not año_inicio.value or not mes_inicio.value or not dia_inicio.value:
                    estado_registro.value = "Fecha inicio obligatoria"
                    estado_registro.color = ft.colors.RED
                    page.update()
                    await asyncio.sleep(2)
                    estado_registro.value = ""
                else:
                    #Una pequeña verificacion de si se quiere registrar la fecha fin del proyecto
                    if año_fin.value.strip() and año_fin.value.strip() and dia_fin.value.strip():
                        fecha_fin = f"{año_fin.value.zfill(4)}-{mes_fin.value.zfill(2)}-{mes_fin.value.zfill(2)}"

                    else:
                        fecha_fin = None


                    fecha_inicio = f"{año_inicio.value.zfill(4)}-{mes_inicio.value.zfill(2)}-{dia_inicio.value.zfill(2)}"

                    nuevo_proyecto = Proyecto(nombre.value, descripcion.value, fecha_inicio, fecha_fin)
                    

                    nuevo_proyecto.guardar_registro()
                    tabla_proyecto.actualizar_tabla()

                    estado_registro.value = "Proyecto registrado exitosamente"
                    estado_registro.color = ft.colors.GREEN
                    page.update()

                    await asyncio.sleep(2)
                    estado_registro.value = ""

                    nombre.value = ""
                    descripcion.value = ""

                    año_inicio.value = ""
                    mes_inicio.value = ""
                    dia_inicio.value = ""

                    año_fin.value = ""
                    mes_fin.value = ""
                    dia_fin.value = ""
                    id_proyecto_actualizar.value = ""
                        
                        

                   

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

    boton_actualizar =ft.ElevatedButton(
        text="Actualizar",
        icon=ft.icons.UPDATE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=actualizar_proyecto,
    )

    

    # Card con diseño del formulario
    formulario = ft.Container(
        expand=1,
            padding=ft.padding.all(24),
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text("Registrar Proyecto", size=24, weight="bold"),
                    ft.Container(content=ft.Row([nombre,descripcion])),
                    
                    ft.Container(content=ft.Row([ft.Text("Fecha de inicio:",expand=1), ft.Text("Fecha de Fin:",expand=1)])),
                    ft.Container(content=ft.Row([contenedor_fecha_inicio,contenedor_fecha_final])),
                    boton_guardar,
                    estado_registro,
                    informacion_para_actualizar,
                    boton_actualizar,
                    
                ],
            ),
        )

    return ft.Column(controls=[formulario], alignment=ft.MainAxisAlignment.CENTER,expand=1)


def main(page: ft.Page):
    page.title = "Sistema de Proyectos"
    page.theme_mode = ft.ThemeMode.LIGHT

    tabla_empleados = TablaEmpleados(page)
    tabla_proyecto = TablaProyectos(page)

    tabla_tareas = TablaTareas(page)

    ventanas =  ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=True,
        tabs=[
            ft.Tab(
                text="Proyecto",
                icon=ft.icons.WORK_HISTORY,
                content=ft.Container(
                    content=ft.Row(
                        [
                            formulario_registro_proyecto(page,tabla_proyecto),
                            tabla_proyecto.construir_tabla()
                            ]),
                    alignment=ft.alignment.center,
                    padding=30,
                ),
            ),
            ft.Tab(
                text="Empleados",
                icon=ft.icons.PEOPLE,
                content=ft.Container(
                    content=ft.Row(
                        [
                            formulario_registro_empleados(page,tabla_empleados),
                            tabla_empleados.construir_tabla()
                            ]),
                    alignment=ft.alignment.center,
                    padding=30,
                ),
            ),

            ft.Tab(
                text="Asignar Tareas",
                icon=ft.icons.BOOK,
                content=ft.Container(
                    content=formulario_registro_tarea(page,tabla_tareas),
                    alignment=ft.alignment.center,
                    padding=30,
                ),
            ),

            ft.Tab(
                text="ver Tareas",
                icon=ft.icons.BOOK,
                content=ft.Container(
                    content=tabla_tareas.construir_tabla(),
                    alignment=ft.alignment.center,
                    padding=30,
                ),
            ),
        ],
    )
    page.add(ventanas)


ft.app(target=main)