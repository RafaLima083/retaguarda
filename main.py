import flet as ft
from views import(
    tela_clientes,
    tela_produtos,
    tela_configuracoes_emitente,
    tela_emissao_nfe,
    menu
)
import database

def main(page: ft.Page):
    page.title = "Sistema de Notas Fiscais"
    
    page.window.maximized=True
    page.theme_mode = ft.ThemeMode.LIGHT

    # Inicializa o banco de dados
    try:    
        database.inicializar_banco()
    except Exception as e:
        page.dialog = ft.AlertDialog(
            title=ft.Text("Erro ao iniciar o banco de dados"),
            content=ft.Text(str(e)),
            actions=[ft.TextButton("Fechar", on_click=lambda e: page.dialog.close())]
        )
        page.dialog.open = True
        page.update()
        return

    # Container principal da área de conteúdo
    conteudo = ft.Container(expand=True)

    # Controla qual tela está sendo carregada
    def navegar_para(nome):
        match nome:
            #Clientes
            case "Cadastro de Clientes":
                tela_clientes.tela_cadastro_clientes(page, conteudo)
            case "Listar Clientes":
                tela_clientes.tela_listagem_clientes(page, conteudo)
                
            #Produtos
            case "Cadastro de Produtos":
                tela_produtos.tela_cadastro_produtos(page, conteudo)
            case "Listar Produtos":
                tela_produtos.tela_listagem_produtos(page, conteudo)
            
            #Configurações
            case "Emitente":
                tela_configuracoes_emitente.tela_configuracoes_emitente(page, conteudo)

            # Movimentações
            case "Emitir NF-e":
                tela_emissao_nfe.tela_emissao_nfe(page, conteudo)
            
            # caso der algum erro
            case _:
                conteudo.content = ft.Text(f"🚧 Página '{nome}' não encontrada.", size=20, color=ft.Colors.RED)
                print(f"[AVISO] Página '{nome}' não existe.")
                

    # Cria o menu lateral com os callbacks
    menu_lateral = menu.criar_menu_lateral(navegar_para)

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

# Inicializa app
ft.app(target=main)
