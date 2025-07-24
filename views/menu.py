import flet as ft

def criar_menu_lateral(callback_navegacao):
    return ft.Column(
        controls=[
            ft.Text("Retaguarda", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Divider(color=ft.Colors.WHITE),

            ft.Text("📁 Cadastros", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
            ft.ListTile(
                title=ft.Text("Clientes", color=ft.Colors.WHITE),
                leading=ft.Icon(ft.Icons.PERSON_OUTLINE, color=ft.Colors.WHITE),
                on_click=lambda _: callback_navegacao("Listar Clientes")
            ),
            ft.ListTile(
                title=ft.Text("Produtos", color=ft.Colors.WHITE),
                leading=ft.Icon(ft.Icons.SHOPPING_BAG_OUTLINED, color=ft.Colors.WHITE),
                on_click=lambda _: callback_navegacao("Listar Produtos")
            ),

            ft.Divider(color=ft.Colors.WHITE),
            ft.Text("🧾 NF-e", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
            ft.ListTile(
                title=ft.Text("Emitir NF-e", color=ft.Colors.WHITE),
                leading=ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED, color=ft.Colors.WHITE),
                on_click=lambda _: callback_navegacao("Emitir NF-e")
            ),

            ft.Divider(color=ft.Colors.WHITE),
            ft.Text("⚙️ Configurações", size=14, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
            ft.ListTile(
                title=ft.Text("Emitente", color=ft.Colors.WHITE),
                leading=ft.Icon(ft.Icons.BUSINESS, color=ft.Colors.WHITE),
                on_click=lambda _: callback_navegacao("Emitente")
            ),
        ],
        spacing=5,
        expand=True
    )
