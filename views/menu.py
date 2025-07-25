import flet as ft
import time

def criar_menu_lateral(page: ft.Page, callback_navegacao):
    container_lateral = ft.Container(height=page.height)  # será preenchido abaixo
    
     # Estado do submenu
    submenu_visivel = ft.Column(visible=False, spacing=10)

    def animar_menu(e):
        menu_botao.scale = 0.8
        container_lateral.update()
        time.sleep(0.05)
        menu_botao.scale = 1

        if container_lateral.content.width == 60:
            container_lateral.content.width = 200
            divider.width = 200
        else:
            container_lateral.content.width = 60
            divider.width = 60

        container_lateral.update()

    def toggle_submenu(e):
        submenu_visivel.visible = not submenu_visivel.visible
        container_lateral.update()    

    menu_botao = ft.Container(
        width=30,
        height=30,
        bgcolor=ft.Colors.BLUE_ACCENT,
        border_radius=8,
        scale=1,
        animate_scale=ft.Animation(duration=50, curve=ft.AnimationCurve.BOUNCE_IN),
        on_click=animar_menu,
    )

    divider = ft.Container(
        width=60,
        height=1,
        animate=ft.Animation(curve=ft.AnimationCurve.LINEAR, duration=50),
        bgcolor="#545c5b",
    )
    
     # Submenu Cadastros
    submenu_visivel.controls = [
        ft.Container(
            ink=True,
            on_click=lambda _: callback_navegacao("Listar Clientes"),
            border_radius=12,
            padding=5,
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=18),
                    ft.Text("Clientes", color=ft.Colors.WHITE, size=12),
                ]
            )
        ),
        ft.Container(
            ink=True,
            on_click=lambda _: callback_navegacao("Listar Produtos"),
            border_radius=12,
            padding=5,
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.INVENTORY_2, color=ft.Colors.WHITE, size=18),
                    ft.Text("Produtos", color=ft.Colors.WHITE, size=12),
                ]
            )
        ),
    ]
    
    # Submenu Nostas fiscais
    ft.Container(
            ink=True,
            on_click=lambda _: callback_navegacao("Emitir NF-e"),
            border_radius=12,
            padding=5,
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.PRINT_ROUNDED, color=ft.Colors.WHITE, size=18),
                    ft.Text("Emitir NF-e", color=ft.Colors.WHITE, size=12),
                ]
            )
        ),
    
    # Preenchendo o container_lateral com o conteúdo agora que temos os controles acima
    container_lateral.content = ft.Container(
        width=60,
        padding=10,
        bgcolor=ft.Colors.BLUE,
        border_radius=0,
        scale=1,
        animate_scale=ft.Animation(duration=400, curve=ft.AnimationCurve.LINEAR),
        expand=True,
        content=ft.Column(
            horizontal_alignment="center",
            spacing=20,
            controls=[
                menu_botao,
                ft.Container(
                    ink=True,
                    on_click=toggle_submenu,
                    border_radius=12,
                    content=ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.Icons.APP_REGISTRATION, icon_color=ft.Colors.WHITE),
                            ft.Text("Cadastros", color=ft.Colors.WHITE),
                        ]
                    )
                ),

                # Submenu: clientes e produtos
                submenu_visivel,

                
                ft.Container(
                    ink=True,
                    on_click=lambda _: callback_navegacao("Emitir NF-e"),
                    border_radius=16,
                    content=ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.Icons.LOCAL_PRINTSHOP, icon_color=ft.Colors.WHITE),
                            ft.Text("Notas fiscais", color=ft.Colors.WHITE),
                        ]
                    )
                ),
                divider,
                ft.Container(
                    ink=True,
                    on_click=lambda _: callback_navegacao("Emitente"),
                    border_radius=16,
                    content=ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.Icons.SETTINGS, icon_color=ft.Colors.WHITE),
                            ft.Text("Configurações", color=ft.Colors.WHITE),
                        ]
                    )
                ),
            ]
        )
    )

    return container_lateral
