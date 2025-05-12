import flet as ft

def inicio():
    logo = ft.Image(
        src="assets/logo_xenthrall.png",
        width=200,
        height=200,
        border_radius=ft.border_radius.all(100),
    )

    title = ft.Text(
        "Xenthrall Academy",
        size=30,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        color=ft.colors.BLUE_GREY_900,
    )

    column = ft.Column(
        controls=[logo, title],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30
    )

    view = ft.Card(
        content=ft.Container(
            content=column,
            border=ft.border.all(1, ft.colors.BLUE_GREY_200),
            padding=40,
            width=400,
            height=400,
            alignment=ft.alignment.center
        ),
        elevation=20,
    )

    return ft.Container(
        content=view,
        alignment=ft.alignment.center,
        expand=True  # Expande para centrar vertical y horizontal
    )
