import flet as ft
import database
from nfe.certificado import carregar_certificado
from nfe.xml_generator import gerar_xml_nfe
from nfe.assinar import assinar_nfe


def tela_emissao_nfe(page: ft.Page, conteudo: ft.Container):
    produtos_adicionados = []
    lista_itens = ft.Column()
    total_label = ft.Text("💰 Total da NF-e: R$ 0.00", size=18, weight="bold")

    nome_cliente = ft.Text("")
    cpf_cnpj_cliente = ft.Text("")

    card_cliente = ft.Card(
        content=ft.Container(
            content=ft.Column([nome_cliente, cpf_cnpj_cliente]),
            padding=10,
            bgcolor=ft.Colors.BLUE_50
        )
    )

    dropdown_clientes = ft.Dropdown(label="Cliente", options=[], expand=True)
    produtos_dropdown = ft.Dropdown(label="Produto", options=[], width=500)

    quantidade = ft.TextField(
        label="Quantidade",
        width=100,
        input_filter=ft.InputFilter("[0-9]", "")
    )

    observacoes = ft.TextField(
        label="Observações da NF-e",
        multiline=True,
        min_lines=3,
        max_lines=5,
        expand=True
    )

    # 🔍 Função de busca de clientes
    def atualizar_lista_clientes(texto):
        texto = texto.lower().strip()
        clientes = database.listar_clientes()
        filtrados = [
            c for c in clientes if texto in (c[1] or "").lower() or texto in (c[2] or "")
        ]
        ordenados = sorted(filtrados, key=lambda c: c[1].lower())
        dropdown_clientes.options.clear()
        for cliente in ordenados:
            id, nome, cpf_cnpj, *_ = cliente
            dropdown_clientes.options.append(
                ft.dropdown.Option(str(id), f"{nome} - {cpf_cnpj}")
            )
        page.update()

    # 🔁 Função chamada quando cliente é selecionado
    def cliente_selecionado(e):
        cliente_id = dropdown_clientes.value
        if not cliente_id:
            return
        cliente = database.buscar_cliente_por_id(int(cliente_id))
        if cliente:
            nome_cliente.value = f"👤 Nome: {cliente[1]}"
            cpf_cnpj_cliente.value = f"🆔 CPF/CNPJ: {cliente[2]}"
            page.update()

    dropdown_clientes.on_change = cliente_selecionado

    # 🔍 Função de busca de produtos
    def atualizar_lista_produtos(texto):
        texto = texto.lower().strip()
        produtos = database.listar_produtos()
        filtrados = [
            p for p in produtos if texto in (p[1] or "").lower() or texto in (p[2] or "").lower()
        ]
        ordenados = sorted(filtrados, key=lambda p: p[2].lower())
        produtos_dropdown.options.clear()
        for produto in ordenados:
            id, ean, descricao, _, valor = produto
            produtos_dropdown.options.append(
                ft.dropdown.Option(str(id), f"{descricao} | R$ {valor:.2f} | Ref: {ean}")
            )
        page.update()

    def atualizar_total():
        total = sum(p["subtotal"] for p in produtos_adicionados)
        total_label.value = f"💰 Total da NF-e: R$ {total:.2f}"
        page.update()

    def adicionar_item(e):
        if not produtos_dropdown.value or not quantidade.value:
            return
        prod_id = int(produtos_dropdown.value)
        qtd = int(quantidade.value)

        produto = database.buscar_produto_por_id(prod_id)
        if produto:
            nome = produto[2]
            valor_unitario = produto[6]
            subtotal = valor_unitario * qtd

            item = {
                "produto_id": prod_id,
                "descricao": nome,
                "quantidade": qtd,
                "valor_unitario": valor_unitario,
                "subtotal": subtotal
            }
            produtos_adicionados.append(item)

            def remover_item(ev):
                lista_itens.controls.remove(item_row)
                produtos_adicionados.remove(item)
                atualizar_total()
                page.update()

            item_row = ft.Row([
                ft.Text(f"{nome} x {qtd} = R$ {subtotal:.2f}", expand=True),
                ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=remover_item)
            ])
            lista_itens.controls.append(item_row)
            atualizar_total()

    def emitir_nfe(e):
        if not dropdown_clientes.value or not produtos_adicionados:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ Selecione o cliente e adicione pelo menos um produto."),
                bgcolor=ft.Colors.RED,
                duration=3000
            )
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Gera XML
            xml = gerar_xml_nfe(
                cliente_id=int(dropdown_clientes.value),
                itens=produtos_adicionados,
                observacoes=observacoes.value
            )

            with open("xml_nfe_nao_assinado.xml", "w", encoding="utf-8") as f:
                f.write(xml)

            # Assina XML
            cert, key = carregar_certificado("certificado.pfx", "sua_senha")
            xml_assinado = assinar_nfe(xml, cert, key)

            with open("xml_nfe_assinado.xml", "w", encoding="utf-8") as f:
                f.write(xml_assinado)

            # Aqui você pode chamar `enviar_nfe_para_sefaz(xml_assinado)` depois
            page.snack_bar = ft.SnackBar(
                content=ft.Text("✅ XML gerado e assinado com sucesso!"),
                bgcolor=ft.Colors.GREEN,
                duration=3000
            )
            page.snack_bar.open = True

        except Exception as erro:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ Erro: {erro}"),
                bgcolor=ft.Colors.RED,
                duration=4000
            )
            page.snack_bar.open = True

        page.update()

    def visualizar_xml(e):
        try:
            with open("xml_nfe_assinado.xml", encoding="utf-8") as f:
                conteudo = f.read()
        except FileNotFoundError:
            conteudo = "XML ainda não foi gerado."

        page.dialog = ft.AlertDialog(
            title=ft.Text("Pré-visualização do XML"),
            content=ft.Text(conteudo),
            on_dismiss=lambda e: None
        )
        page.dialog.open = True
        page.update()

    # Layout da tela
    layout = ft.Column([
        ft.Text("🧾 Emissão de NF-e", size=22, weight="bold"),
        ft.TextField(label="🔎 Buscar cliente por nome ou CPF/CNPJ", on_change=lambda e: atualizar_lista_clientes(e.control.value), expand=True),
        dropdown_clientes,
        card_cliente,
        ft.Divider(),

        ft.TextField(label="🔎 Buscar produto por nome ou código", on_change=lambda e: atualizar_lista_produtos(e.control.value), expand=True),
        ft.Row([produtos_dropdown, quantidade, ft.ElevatedButton("Adicionar", on_click=adicionar_item)], spacing=10),
        lista_itens,
        total_label,

        ft.Divider(),
        observacoes,

        ft.Row([
            ft.ElevatedButton("Emitir NF-e", icon=ft.Icons.SEND, on_click=emitir_nfe),
            ft.OutlinedButton("Pré-visualizar XML", icon=ft.Icons.CODE, on_click=visualizar_xml)
        ], spacing=20)
    ], spacing=20)

    conteudo.content = ft.Container(content=layout, padding=20)
    page.update()
