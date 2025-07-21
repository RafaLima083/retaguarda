import flet as ft

def criar_menu_lateral(callback_pagina):
    """
    Cria o menu lateral com seções e botões de navegação.
    O parâmetro 'callback_pagina' é uma função que será chamada ao clicar nos itens.
    """

    return ft.Container(
        width=260,
        bgcolor=ft.Colors.GREY_100,
        padding=10,        
        content=ft.Column(
            controls=[
                ft.Text("Menu", weight="bold", size=16),

                ft.ExpansionTile(
                    title=ft.Text("Cadastros"),
                    leading=ft.Icon(ft.Icons.PERSON),
                    controls=[
                        ft.ListTile(
                            title=ft.Text("Clientes"),
                            leading=ft.Icon(ft.Icons.PEOPLE),
                            on_click=lambda e: callback_pagina("Cadastro de Clientes")
                        ),
                        ft.ListTile(
                            title=ft.Text("Listar clientes"),
                            leading=ft.Icon(ft.Icons.LIST),
                            on_click=lambda e: callback_pagina("Listar Clientes")
                        ),
                        ft.ListTile(
                            title=ft.Text("Produtos"),
                            leading=ft.Icon(ft.Icons.INVENTORY),
                            on_click=lambda e: callback_pagina("Cadastro de Produtos")
                        ),
                        ft.ListTile(
                            title=ft.Text("Listar Produtos"),
                            leading=ft.Icon(ft.Icons.INVENTORY),
                            on_click=lambda e: callback_pagina("Listar Produtos")
                        ),
                    ]
                ),

                ft.ExpansionTile(
                    title=ft.Text("Movimentações"),
                    leading=ft.Icon(ft.Icons.SWAP_HORIZ),
                    controls=[
                        ft.ListTile(
                            title=ft.Text("Emitir NF-e"),
                            leading=ft.Icon(ft.Icons.RECEIPT_LONG),
                            on_click=lambda e: callback_pagina("Emitir NF-e")
                        ),
                        ft.ListTile(
                            title=ft.Text("Consultar NF"),
                            leading=ft.Icon(ft.Icons.RECEIPT_LONG),
                            on_click=lambda e: callback_pagina("...")
                        ),
                    ]
                ),

                ft.ExpansionTile(
                    title=ft.Text("Relatórios"),
                    leading=ft.Icon(ft.Icons.BAR_CHART),
                    controls=[
                        ft.ListTile(
                            title=ft.Text("Vendas"),
                            leading=ft.Icon(ft.Icons.SHOW_CHART),
                            on_click=lambda e: callback_pagina("Relatório de Vendas")
                        ),
                        ft.ListTile(
                            title=ft.Text("Clientes Ativos"),
                            leading=ft.Icon(ft.Icons.GROUP),
                            on_click=lambda e: callback_pagina("Relatório de Clientes")
                        ),
                    ]
                ),
                ft.ExpansionTile(
                    title=ft.Text(" Configurações"),
                    leading=ft.Icon(ft.Icons.SETTINGS),
                    controls=[
                        ft.ListTile(
                            title=ft.Text("Emitente"),
                            leading=ft.Icon(ft.Icons.SHOW_CHART),
                            on_click=lambda e: callback_pagina("Emitente")
                        ),                        
                    ]
                ),
            ],
            spacing=5,
            expand=True
        )
    )
