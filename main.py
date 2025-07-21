import flet as ft
from views.tela_clientes import tela_cadastro_clientes, tela_listagem_clientes
from views.tela_produtos import tela_cadastro_produtos, tela_listagem_produtos
from views.tela_configuracoes import tela_configuracoes_emitente
from views.tela_emissao_nfe import tela_emissao_nfe

from views.menu import criar_menu_lateral
import database

def main(page: ft.Page):
    page.title = "Sistema de Notas Fiscais"
    
    page.window.maximized=True
    # page.window_width = 1000
    # page.window_height = 900
    page.theme_mode = ft.ThemeMode.LIGHT

    # Cria o banco de dados se não existir
    database.criar_tabela_clientes()
    database.criar_tabela_produtos()
    database.criar_tabela_emitente()
    database.criar_tabela_configuracoes()
    database.criar_tabela_nfe()

    # Container principal da área de conteúdo
    conteudo = ft.Container(expand=True)

    # Controla qual tela está sendo carregada
    def carregar_pagina(nome):
        if nome == "Cadastro de Clientes":
            tela_cadastro_clientes(page, conteudo)
        elif nome == "Listar Clientes":
            tela_listagem_clientes(page, conteudo)
        elif nome == "Cadastro de Produtos":
            tela_cadastro_produtos(page, conteudo)
        elif nome == "Listar Produtos":
            tela_listagem_produtos(page, conteudo)
        elif nome == "Emitente":
            tela_configuracoes_emitente(page, conteudo)
        elif nome == "Emitir NF-e":
            tela_emissao_nfe(page, conteudo)
        else:
            conteudo.content = ft.Text(f"Você está em: {nome}", size=20)
            page.update()

    # Cria o menu lateral com os callbacks
    menu_lateral = criar_menu_lateral(carregar_pagina)

    # Layout principal com menu e conteúdo
    layout = ft.Row(
        controls=[
            menu_lateral,
            ft.VerticalDivider(width=1),
            conteudo
        ],
        expand=True
    )

    page.add(layout)

# Inicia a aplicação Flet
ft.app(target=main)
