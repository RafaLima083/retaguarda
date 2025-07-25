import flet as ft
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
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.maximized = True
    page.scroll = ft.ScrollMode.HIDDEN
    page.padding = 0

    # Inicializa banco
    database.inicializar_banco()

    # Variáveis de controle
    conteudo = ft.Container(expand=True, padding=20)
    

    # Função de navegação entre telas
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

    # Cria menu lateral m callback de navegação
    menu_lateral = menu.criar_menu_lateral(page, navegar_para)

    # Containers do layout
    

    divisor = ft.VerticalDivider(width=1, visible=True)

    # Layout principal com menu lateral + conteúdo
    layout = ft.Row(
        controls=[
            menu_lateral,
            ft.VerticalDivider(width=1),
            conteudo
        ],
        expand=True
)

    # Responsividade ao redimensionar janela
    
    page.add(layout)



# Início da aplicação Flet
if __name__ == "__main__":
    ft.app(target=main)
