import flet as ft
import asyncio


from models.database import resource_path

# La definición de la función ACEPTA 'page' y 'app_state'
def acerca_de_view(page: ft.Page, app_state: dict):
    """
    Construye la vista "Acerca de".
    Utiliza app_state para gestionar el estado del audio y la animación de forma global.
    """

    # Imagen animada. Su referencia se guardará en app_state.
    # Asegúrate de que 'assets/logo.png' exista en tu directorio de assets.
    image = ft.Image(
        src=resource_path("assets/logo.png"),
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
        scale=ft.Scale(1.0), # Escala inicial
        animate_scale=ft.Animation(300, curve=ft.AnimationCurve.EASE_IN_OUT),
    )
    # Guardar la referencia de la imagen en el estado global para que dashboard.py pueda acceder a ella
    app_state["acerca_de_image_control"] = image 

    async def beat_animation_loop():
        """Bucle principal de la animación de latido para la imagen."""
        try:
            # La animación solo se ejecuta si la música está sonando Y esta vista ("Acerca de") está activa.
            while app_state.get("is_music_playing") and app_state.get("acerca_de_view_is_active"):
                # Verificar si el control de imagen todavía existe y está asignado en app_state
                current_image_control = app_state.get("acerca_de_image_control")
                if not current_image_control: 
                    break 
                
                current_image_control.scale = ft.Scale(1.15)
                # Actualizar solo si el control de imagen tiene una página (está visible)
                if page and current_image_control.page: 
                    page.update(current_image_control)
                await asyncio.sleep(0.3)

                # Volver a comprobar condiciones, podrían haber cambiado durante el sleep
                if not (app_state.get("is_music_playing") and app_state.get("acerca_de_view_is_active")):
                    break
                
                current_image_control = app_state.get("acerca_de_image_control") # Re-obtener por si cambió
                if not current_image_control:
                    break

                current_image_control.scale = ft.Scale(1.0)
                if page and current_image_control.page:
                    page.update(current_image_control)
                await asyncio.sleep(0.3)
        except asyncio.CancelledError:
            # La tarea fue cancelada (ej. al pausar o cambiar de vista). Es un comportamiento esperado.
            pass 
        finally:
            # Asegurar que la imagen siempre vuelva a su escala original.
            final_image_control = app_state.get("acerca_de_image_control")
            if final_image_control:
                final_image_control.scale = ft.Scale(1.0)
                if page and final_image_control.page:
                    try:
                        page.update(final_image_control)
                    except Exception:
                        # Podría fallar si la página o el control ya no son válidos al momento de la limpieza.
                        pass
            
            # Limpiar la referencia a la tarea en app_state si esta tarea es la que está registrada.
            current_task = asyncio.current_task()
            if app_state.get("acerca_de_animation_task") == current_task:
                app_state["acerca_de_animation_task"] = None


    def play_action(e):
        """Acción al presionar el botón de reproducir."""
        app_state["is_music_playing"] = True
        # Usar el control de audio global desde app_state
        if app_state.get("audio_control"):
            app_state["audio_control"].play() 
        
        # Cancelar cualquier tarea de animación anterior para esta vista
        if app_state.get("acerca_de_animation_task") and not app_state["acerca_de_animation_task"].done():
            app_state["acerca_de_animation_task"].cancel()
        
        # Iniciar la nueva tarea de animación (solo si esta vista está activa)
        if app_state.get("acerca_de_view_is_active"):
            # page.run_task es preferible para tareas gestionadas por Flet.
            app_state["acerca_de_animation_task"] = page.run_task(beat_animation_loop)
        
        # Actualizar estado de los botones (si existen y están en la página)
        current_play_button = app_state.get("acerca_de_play_button")
        current_pause_button = app_state.get("acerca_de_pause_button")
        if current_play_button and current_play_button.page: 
            current_play_button.disabled = True
        if current_pause_button and current_pause_button.page:
            current_pause_button.disabled = False
        if current_play_button and current_play_button.page and current_pause_button and current_pause_button.page:
            page.update(current_play_button, current_pause_button)

    def pause_action(e):
        """Acción al presionar el botón de pausar."""
        app_state["is_music_playing"] = False # La música se detiene globalmente
        if app_state.get("audio_control"):
            app_state["audio_control"].pause()

        # Cancelar la tarea de animación si está en ejecución.
        if app_state.get("acerca_de_animation_task") and not app_state["acerca_de_animation_task"].done():
            app_state["acerca_de_animation_task"].cancel()
            # El bloque 'finally' en beat_animation_loop se encargará de resetear la imagen.
        else: 
            # Si no había tarea o ya terminó, resetear explícitamente la imagen por si acaso.
            current_image_control = app_state.get("acerca_de_image_control")
            if current_image_control and current_image_control.page:
                current_image_control.scale = ft.Scale(1.0)
                page.update(current_image_control)
        
        # Actualizar estado de los botones (si existen y están en la página)
        current_play_button = app_state.get("acerca_de_play_button")
        current_pause_button = app_state.get("acerca_de_pause_button")
        if current_play_button and current_play_button.page:
            current_play_button.disabled = False
        if current_pause_button and current_pause_button.page:
            current_pause_button.disabled = True
        if current_play_button and current_play_button.page and current_pause_button and current_pause_button.page:
            page.update(current_play_button, current_pause_button)

    play_button = ft.ElevatedButton("▶️ Reproducir", on_click=play_action)
    pause_button = ft.ElevatedButton("⏸️ Pausar", on_click=pause_action) # Inicia habilitado o deshabilitado según estado global
    
    # Guardar referencias a los botones en app_state para que dashboard.py pueda actualizarlos si es necesario
    # y para que esta propia vista pueda configurarlos al inicio.
    app_state["acerca_de_play_button"] = play_button
    app_state["acerca_de_pause_button"] = pause_button

    # --- Configuración inicial al cargar/re-cargar la vista ---
    if app_state.get("is_music_playing"):
        play_button.disabled = True
        pause_button.disabled = False
        # Si la música ya está sonando Y esta vista está activa, iniciar/reanudar la animación.
        if app_state.get("acerca_de_view_is_active"):
            # Cancelar tarea anterior por si acaso (ej. recarga rápida de vista)
            if app_state.get("acerca_de_animation_task") and not app_state["acerca_de_animation_task"].done():
                app_state["acerca_de_animation_task"].cancel() 
            app_state["acerca_de_animation_task"] = page.run_task(beat_animation_loop)
    else:
        play_button.disabled = False
        pause_button.disabled = True
        # Asegurar que la imagen esté reseteada si no hay música al entrar a la vista
        image.scale = ft.Scale(1.0) 

    # Contenido de la vista "Acerca de"
    music = ft.Container(
        content=ft.Column(
            controls=[
                image,
                ft.Row(
                    [play_button, pause_button], 
                    alignment=ft.MainAxisAlignment.CENTER, 
                    spacing=20 # Espaciado entre botones
                ),
                ft.Text("App desarrollada por la empresa XENTHRALL 👽🚀", text_align=ft.TextAlign.CENTER)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30 # Espaciado entre elementos de la columna
        ),
        alignment=ft.alignment.center,
        expand=True,
        padding=20,
        bgcolor=ft.Colors.BLACK12
    )


    return music
