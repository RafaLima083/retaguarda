import flet as ft

def main(page: ft.Page):
    page.window.maximized = True

    menu_visivel = True

    def page_resize(e):
        nonlocal menu_visivel
        if page.width < 700 and menu_visivel:
            menu_lateral.visible = False
            menu_visivel = False
        elif page.width >= 700 and not menu_visivel:
            menu_lateral.visible = True
            menu_visivel = True
        page.update()

    page.on_resized = page_resize

    def navegar_para(pagina):
        conteudo.value = f"📄 Você está em: {pagina}"
        page.update()

    menu_lateral = ft.Column(
        [
            ft.Text("Menu", color=ft.Colors.WHITE, size=18),
            ft.ListTile(
                title=ft.Text("Clientes", color=ft.Colors.WHITE),
                on_click=lambda e: navegar_para("Clientes")
            ),
            ft.ListTile(
                title=ft.Text("Produtos", color=ft.Colors.WHITE),
                on_click=lambda e: navegar_para("Produtos")
            ),
        ],
        expand=True,
    )

    menu_container = ft.Container(
        content=menu_lateral,
        width=200,
        bgcolor=ft.Colors.BLUE_700,
        padding=10,
        visible=True
    )

    conteudo = ft.Text("Conteúdo principal")

    layout = ft.ResponsiveRow(
        [
            ft.Container(menu_container, col={"sm": 12, "md": 2, "xl": 2}),
            ft.Container(ft.VerticalDivider(width=1), col={"sm": 0, "md": 0.1}),
            ft.Container(conteudo, col={"sm": 12, "md": 9.9}),
        ],
        spacing=0
    )

    page.add(layout) 
from views import (
    tela_clientes,
    tela_produtos,
    tela_configuracoes_emitente,
    tela_emissao_nfe,
    menu
)
import database

def main(page: ft.Page):
    page.title = "Sistema de Notas Fiscais"
    page.window.maximizable = True
    page.theme_mode = ft.ThemeMode.LIGHT

    database.inicializar_banco()

    conteudo = ft.Container(expand=True, padding=20)
    menu_visivel = True

    def navegar_para(nome):
        match nome:
            case "Cadastro de Clientes":
                tela_clientes.tela_cadastro_clientes(page, conteudo)
            case "Listar Clientes":
                tela_clientes.tela_listagem_clientes(page, conteudo)
            case "Cadastro de Produtos":
                tela_produtos.tela_cadastro_produtos(page, conteudo)
            case "Listar Produtos":
                tela_produtos.tela_listagem_produtos(page, conteudo)
            case "Emitente":
                tela_configuracoes_emitente.tela_configuracoes_emitente(page, conteudo)
            case "Emitir NF-e":
                tela_emissao_nfe.tela_emissao_nfe(page, conteudo)
            case _:
                conteudo.content = ft.Text(f"🚧 Página '{nome}' não encontrada.", color=ft.Colors.RED)
                page.update()

    menu_coluna = menu.criar_menu_lateral(navegar_para)

    menu_container = ft.Container(
        content=menu_coluna,
        bgcolor=ft.Colors.BLUE_800,
        padding=10,
        width=230,
        visible=True,
        
    )

    divider = ft.VerticalDivider(width=1, visible=True)

    def page_resize(e):
        nonlocal menu_visivel
        if page.width < 720:
            if menu_visivel:
                menu_container.visible = False
                divider.visible = False
                menu_visivel = False
        else:
            if not menu_visivel:
                menu_container.visible = True
                divider.visible = True
                menu_visivel = True
        page.update()

    page.on_resize = page_resize

    layout = ft.ResponsiveRow(
        [
            ft.Container(menu_container, col={"sm": 0, "md": 2}),
            ft.Container(divider, col={"sm": 0, "md": 0.1}),
            ft.Container(conteudo, col={"sm": 12, "md": 9.9}),
        ],
        spacing=0
    )

    page.add(layout)
    page_resize(None)

ft.app(target=main)

