import flet as ft
from datetime import date
from models.database import Nota, Estudiante, Materia # Asegúrate que Estudiante y Materia estén aquí

def notas_view(page: ft.Page):
    """
    Retorna la vista para gestionar notas usando Flet,
    con visualización de nombres y validación para el botón registrar.
    """
    error_text = ft.Text(value="", color=ft.Colors.RED)

    # --- Función para actualizar el display de nombres ---
    def actualizar_display_nombre(id_field, nombre_display_control, funcion_obtener_nombre, entidad_nombre="Entidad"):
        # Esta función ya no llama a page.update() directamente.
        # La llamada a page.update() se hará desde el manejador de evento que la invoca.
        try:
            if id_field.value.strip():
                item_id = int(id_field.value)
                nombre = funcion_obtener_nombre(item_id)
                if nombre:
                    nombre_display_control.value = str(nombre)
                    nombre_display_control.color = ft.Colors.BLUE_ACCENT_700
                else:
                    nombre_display_control.value = f"⚠️ {entidad_nombre} ID no encontrado"
                    nombre_display_control.color = ft.Colors.ORANGE_ACCENT_700
            else:
                nombre_display_control.value = ""
        except ValueError:
            nombre_display_control.value = f"⚠️ ID de {entidad_nombre} inválido"
            nombre_display_control.color = ft.Colors.RED_ACCENT_700
        except Exception as ex:
            print(f"Error al obtener nombre de {entidad_nombre}: {ex}")
            nombre_display_control.value = f"⚠️ Error al buscar {entidad_nombre}"
            nombre_display_control.color = ft.Colors.RED_ACCENT_700

    # --- Botones de acción ---
    btn_registrar = ft.ElevatedButton(text="Registrar", icon=ft.icons.ADD_CIRCLE_OUTLINE, disabled=True) # Inicia deshabilitado
    btn_listar = ft.ElevatedButton(text="Listar Notas Est.", icon=ft.icons.LIST_ALT)
    btn_actualizar = ft.ElevatedButton(text="Actualizar Nota", icon=ft.icons.EDIT)
    btn_eliminar = ft.ElevatedButton(text="Eliminar Nota", icon=ft.icons.DELETE_OUTLINE, color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_ACCENT_700)

    # --- Función para actualizar el estado del botón Registrar ---
    def actualizar_estado_boton_registrar():
        # Habilitar btn_registrar solo si id_mat_field tiene un valor
        # y materia_nombre_display no indica un error o "ID no encontrado".
        # Adicionalmente, se podría requerir que id_est_field también sea válido.
        
        materia_id_ingresado = id_mat_field.value and id_mat_field.value.strip() != ""
        materia_valida = materia_id_ingresado and materia_nombre_display.value != "" and not materia_nombre_display.value.startswith("⚠️")
        
        # Opcional: verificar también si el estudiante es válido
        # estudiante_id_ingresado = id_est_field.value and id_est_field.value.strip() != ""
        # estudiante_valido = estudiante_id_ingresado and estudiante_nombre_display.value != "" and not estudiante_nombre_display.value.startswith("⚠️")
        # if materia_valida and estudiante_valido: # Si se requiere que ambos sean válidos

        if materia_valida:
            btn_registrar.disabled = False
        else:
            btn_registrar.disabled = True
        # page.update() se llamará desde el manejador que invoca esta función

    # --- Campos de entrada ---
    id_nota_field = ft.TextField(label="ID Nota", width=100, disabled=True, hint_text="Automático o para editar")
    
    id_est_field = ft.TextField(label="ID Estudiante", width=150)
    estudiante_nombre_display = ft.Text(value="", color=ft.Colors.BLUE_ACCENT_700, weight=ft.FontWeight.BOLD, size=12)
    
    id_mat_field = ft.TextField(label="ID Materia", width=150)
    materia_nombre_display = ft.Text(value="", color=ft.Colors.BLUE_ACCENT_700, weight=ft.FontWeight.BOLD, size=12)

    nota_field = ft.TextField(label="Nota", width=100)
    fecha_field = ft.TextField(label="Fecha (YYYY-MM-DD)", width=150, value=date.today().isoformat())

    # --- Manejadores de eventos on_change para campos de ID ---
    def on_id_est_change(e):
        actualizar_display_nombre(id_est_field, estudiante_nombre_display, Estudiante.obtener_nombre_completo, "Estudiante")
        # Opcional: Si la validez del estudiante también debe afectar btn_registrar, llamar aquí:
        # actualizar_estado_boton_registrar() 
        page.update()

    def on_id_mat_change(e):
        actualizar_display_nombre(id_mat_field, materia_nombre_display, Materia.obtener_nombre_materia, "Materia")
        actualizar_estado_boton_registrar() # Actualiza el estado del botón registrar
        page.update()

    id_est_field.on_change = on_id_est_change
    id_mat_field.on_change = on_id_mat_change
    
    # --- Tabla de notas ---
    table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("Cargando..."))], 
        rows=[],
        visible=False,
        expand=True,
        column_spacing=20,
    )
    
    # --- Funciones CRUD y auxiliares (modificadas para llamar a actualizar_estado_boton_registrar donde sea pertinente) ---
    def limpiar_campos_entrada(reset_id_nota=True):
        if reset_id_nota:
             id_nota_field.value = ""
        # Considerar si se debe limpiar id_est_field o no
        # id_est_field.value = ""
        # estudiante_nombre_display.value = ""
        id_mat_field.value = ""
        materia_nombre_display.value = "" # Limpiar también el display
        nota_field.value = ""
        fecha_field.value = date.today().isoformat()
        
        actualizar_estado_boton_registrar() # El botón se deshabilitará porque id_mat_field está vacío
        
        id_mat_field.focus()
        page.update()

    def poblar_campos_desde_fila(datos_fila):
        id_nota_field.value = str(datos_fila[0])
        id_est_field.value = str(datos_fila[1]) 
        id_mat_field.value = str(datos_fila[2])
        nota_field.value = str(datos_fila[3])
        fecha_field.value = str(datos_fila[4])
        
        actualizar_display_nombre(id_est_field, estudiante_nombre_display, Estudiante.obtener_nombre_completo, "Estudiante")
        actualizar_display_nombre(id_mat_field, materia_nombre_display, Materia.obtener_nombre_materia, "Materia")
        actualizar_estado_boton_registrar() # Actualizar estado del botón después de poblar campos
        
        id_nota_field.disabled = False 
        page.update()

    # ... (Las funciones listar_notas, registrar_nota, actualizar_nota, eliminar_nota como en la versión anterior,
    #    asegurándose que llamar a limpiar_campos_entrada o actualizar_estado_boton_registrar donde sea necesario)

    # Modificación en registrar_nota para que llame a limpiar_campos_entrada
    def registrar_nota(_):
        try:
            error_text.value = ""
            if not all([id_est_field.value, id_mat_field.value, nota_field.value, fecha_field.value]):
                error_text.value = "Todos los campos (excepto ID Nota) son requeridos para registrar."
                page.update()
                return
            
            id_est = int(id_est_field.value)
            id_mat = int(id_mat_field.value)
            val_nota = float(nota_field.value)
            if not (0 <= val_nota <= 5):
                 error_text.value = "La nota debe estar entre 0 y 5."
                 page.update()
                 return

            fecha = fecha_field.value
            
            Nota.registrar_nota(id_est, id_mat, val_nota, fecha)
            error_text.value = "Nota registrada exitosamente."
            error_text.color = ft.Colors.GREEN_ACCENT_700
            limpiar_campos_entrada(reset_id_nota=True) # Esto ya llama a actualizar_estado_boton_registrar
            listar_notas(None)
            id_nota_field.disabled = True

        except ValueError as ve:
            error_text.value = f"Error en los datos ingresados: {ve}. Asegúrese que IDs y nota sean números."
            error_text.color = ft.Colors.RED_ACCENT_700
            page.update()
        except Exception as e:
            error_text.value = f"Error al registrar la nota: {e}"
            error_text.color = ft.Colors.RED_ACCENT_700
            page.update()
            
    # Similarmente, asegurar que actualizar_nota y eliminar_nota llamen a limpiar_campos_entrada
    def actualizar_nota(_):
        try:
            error_text.value = ""
            if not id_nota_field.value or not nota_field.value:
                error_text.value = "ID Nota y el nuevo valor de la Nota son requeridos para actualizar."
                page.update()
                return

            id_nota = int(id_nota_field.value)
            nuevo_valor_nota = float(nota_field.value)
            if not (0 <= nuevo_valor_nota <= 5):
                 error_text.value = "La nota debe estar entre 0 y 5."
                 page.update()
                 return
            
            Nota.actualizar_nota(id_nota, nuevo_valor_nota)
            error_text.value = "Nota actualizada exitosamente."
            error_text.color = ft.Colors.GREEN_ACCENT_700
            limpiar_campos_entrada(reset_id_nota=True) # Llama a actualizar_estado_boton_registrar
            listar_notas(None)
            id_nota_field.disabled = True

        except ValueError as ve:
            error_text.value = f"Error en los datos: {ve}. ID Nota y Nota deben ser números."
            error_text.color = ft.Colors.RED_ACCENT_700
            page.update()
        except Exception as e:
            error_text.value = f"Error al actualizar nota: {e}"
            error_text.color = ft.Colors.RED_ACCENT_700
            page.update()

    def eliminar_nota(_):
        try:
            error_text.value = ""
            if not id_nota_field.value:
                error_text.value = "ID Nota es requerido para eliminar."
                page.update()
                return

            id_nota = int(id_nota_field.value)
            Nota.eliminar_nota(id_nota)
            error_text.value = "Nota eliminada exitosamente."
            error_text.color = ft.Colors.GREEN_ACCENT_700
            limpiar_campos_entrada(reset_id_nota=True) # Llama a actualizar_estado_boton_registrar
            listar_notas(None)
            id_nota_field.disabled = True

        except ValueError as ve:
            error_text.value = f"Error en los datos: {ve}. ID Nota debe ser un número."
            error_text.color = ft.Colors.RED_ACCENT_700
            page.update()
        except Exception as e:
            error_text.value = f"Error al eliminar nota: {e}"
            error_text.color = ft.Colors.RED_ACCENT_700
            page.update()
            
    def listar_notas(_): # Copiada de la respuesta anterior, con mejoras
        try:
            if not id_est_field.value or not id_est_field.value.strip().isdigit():
                error_text.value = "Por favor, ingrese un ID de Estudiante válido para listar."
                error_text.color = ft.Colors.RED_ACCENT_700 
                table.visible = False
                if not table.columns:
                    table.columns.append(ft.DataColumn(ft.Text("")))
                page.update()
                return
            
            est_id = int(id_est_field.value)
            data = Nota.obtener_notas_por_estudiante(est_id) 
            
            table.columns.clear() 
            table.rows.clear()

            if not data: 
                table.visible = False 
                nombre_est_valido = ""
                if estudiante_nombre_display.value and not estudiante_nombre_display.value.startswith("⚠️"):
                    nombre_est_valido = f" ({estudiante_nombre_display.value.strip()})"
                
                error_text.value = f"El estudiante ID {est_id}{nombre_est_valido} no tiene notas registradas."
                error_text.color = ft.Colors.BLUE_700 
                table.columns.append(ft.DataColumn(ft.Text("No hay notas para mostrar")))
            else:
                error_text.value = "" 
                table.columns = [
                    ft.DataColumn(ft.Text("ID Nota")), ft.DataColumn(ft.Text("Materia")), 
                    ft.DataColumn(ft.Text("Nota")), ft.DataColumn(ft.Text("Fecha")),
                    ft.DataColumn(ft.Text("Acciones")), 
                ]
                for r in data: 
                    nombre_materia = Materia.obtener_nombre_materia(r[2]) or f"ID Mat: {r[2]}"
                    def crear_handler_seleccionar_para_editar(datos_fila_capturada):
                        return lambda e: poblar_campos_desde_fila(datos_fila_capturada)
                    table.rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(str(r[0]))), ft.DataCell(ft.Text(nombre_materia)),
                            ft.DataCell(ft.Text(str(r[3]))), ft.DataCell(ft.Text(str(r[4]))),
                            ft.DataCell(ft.IconButton(
                                icon=ft.icons.EDIT_NOTE, tooltip="Cargar esta nota para editar",
                                on_click=crear_handler_seleccionar_para_editar(r)
                            ))]))
                table.visible = True
            page.update()
        except Exception as e:
            error_text.value = f"Error al listar notas: {e}"
            error_text.color = ft.Colors.RED_ACCENT_700
            table.visible = False
            if not table.columns:
                 table.columns.append(ft.DataColumn(ft.Text("Error al cargar")))
            page.update()
            
    # Asignar eventos a botones
    btn_listar.on_click = listar_notas
    btn_registrar.on_click = registrar_nota
    btn_actualizar.on_click = actualizar_nota
    btn_eliminar.on_click = eliminar_nota
    
    # --- Layout de la vista ---
    input_fields_row = ft.Row(
        [
            ft.Column([id_est_field, estudiante_nombre_display], spacing=1, width=200),
            ft.Column([id_mat_field, materia_nombre_display], spacing=1, width=200),
            ft.Column([nota_field], width=110),
            ft.Column([fecha_field], width=160),
            ft.Column([id_nota_field], width=110)
        ],
        wrap=False, spacing=15, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START
    )
    action_buttons_row = ft.Row(
        [btn_registrar, btn_listar, btn_actualizar, btn_eliminar],
        spacing=10, alignment=ft.MainAxisAlignment.START
    )
    container = ft.Column(
        [input_fields_row, action_buttons_row, error_text, ft.Divider(),
         ft.Text("Notas Registradas:", weight=ft.FontWeight.BOLD), table],
        expand=True, spacing=15, scroll=ft.ScrollMode.ADAPTIVE
    )

    # Establecer estado inicial del botón registrar al cargar la vista
    actualizar_estado_boton_registrar()

    return container
