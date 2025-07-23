import flet as ft
import re
import database
from utils.ncm_validador import ncm_existe


def tela_cadastro_produtos(page: ft.Page, conteudo: ft.Container, modo_edicao=False, produto_id=None, valores=None):
    emitente = database.carregar_emitente()
    regime_emitente = emitente["crt"] if emitente else ""

    def opcoes_cst_por_regime(regime: str):
        regime = str(regime).strip()
        if regime in ["1", "2", "4"]:
            return [
                ft.dropdown.Option("101", "101 - SN c/ crédito"),
                ft.dropdown.Option("102", "102 - SN s/ crédito"),
                ft.dropdown.Option("103", "103 - Isenção (SN)"),
                ft.dropdown.Option("201", "201 - SN c/ ST e crédito"),
                ft.dropdown.Option("202", "202 - SN c/ ST s/ crédito"),
                ft.dropdown.Option("500", "500 - ST anterior (SN)"),
            ]
        return [
            ft.dropdown.Option("00", "00 - Tributação integral"),
            ft.dropdown.Option("20", "20 - Redução de base"),
            ft.dropdown.Option("40", "40 - Isenta"),
            ft.dropdown.Option("41", "41 - Não tributada"),
            ft.dropdown.Option("60", "60 - ST anterior"),
        ]

    # Campos
    codigo = ft.TextField(label="Código Interno", width=120)
    descricao = ft.TextField(label="Descrição do Produto", width=800)
    ncm = ft.TextField(label="NCM", width=120, max_length=8)
    cest = ft.TextField(label="CEST (se houver)", width=120, max_length=7)
    unidade = ft.Dropdown(label="Unidade", width=200, options=[
        ft.dropdown.Option("---", "---"),
        ft.dropdown.Option("UN"),
        ft.dropdown.Option("KG"),
        ft.dropdown.Option("PC"),
        ft.dropdown.Option("LT"),
        ft.dropdown.Option("MT"),
    ])
    valor_unitario = ft.TextField(
        label="Valor de Venda",
        width=120,
        input_filter=ft.InputFilter(regex_string=r"[0-9.,]", replacement_string="")
    )
    cst_csosn = ft.Dropdown(label="CST/CSOSN", width=250, options=opcoes_cst_por_regime(regime_emitente))
    origem = ft.Dropdown(label="Origem do Produto", width=250, options=[
        ft.dropdown.Option("0", "0 - Nacional"),
        ft.dropdown.Option("1", "1 - Importado Direto"),
        ft.dropdown.Option("2", "2 - Importado Interno"),
        ft.dropdown.Option("3", "3 - Nacional > 40% importado"),
        ft.dropdown.Option("4", "4 - Nacional (PPB)"),
        ft.dropdown.Option("5", "5 - Nacional ≤ 40% importado"),
        ft.dropdown.Option("6", "6 - Importado sem similar"),
        ft.dropdown.Option("7", "7 - Importado interno s/ similar"),
        ft.dropdown.Option("8", "8 - Nacional > 70% importado"),
    ])
    ean = ft.TextField(label="Código de Barras", width=200, max_length=13)
    msg_status = ft.Text("")

    if valores:
        codigo.value = valores.get("codigo", "")
        descricao.value = valores.get("descricao", "")
        ncm.value = valores.get("ncm", "")
        cest.value = valores.get("cest", "")
        unidade.value = valores.get("unidade", "")
        valor_unitario.value = str(valores.get("valor_unitario", ""))
        cst_csosn.value = valores.get("cst_csosn", "")
        origem.value = valores.get("origem", "")
        ean.value = valores.get("ean", "")

    def limpar_formulario(e=None):
        for campo in [codigo, descricao, ncm, cest, unidade, valor_unitario, cst_csosn, origem, ean]:
            campo.value = ""
        msg_status.value = ""
        page.update()

    def ean_formatado(valor):
        numeros = re.sub(r'\D', '', valor)
        return numeros.zfill(13) if numeros else ""

    def salvar_produto(e):
        try:
            if not codigo.value.strip() or not descricao.value.strip():
                raise ValueError("Código e descrição são obrigatórios.")
            if not re.match(r'^\d{8}$', ncm.value.strip()):
                raise ValueError("NCM deve conter 8 dígitos.")
            if not ncm_existe(ncm.value.strip()):
                raise ValueError("NCM não encontrado na tabela.")
            if not unidade.value or unidade.value == "---":
                raise ValueError("Unidade obrigatória.")
            
            valor_raw = valor_unitario.value.strip().replace(".", "").replace(",", ".")
            if not re.match(r'^\d+(\.\d{1,2})?$', valor_raw):
                raise ValueError("Valor unitário inválido.")

            if not cst_csosn.value:
                raise ValueError("Selecione um CST/CSOSN.")
            if not origem.value:
                raise ValueError("Selecione a origem do produto.")

            dados = {
                "codigo": codigo.value.strip().upper(),
                "descricao": descricao.value.strip().upper(),
                "ncm": ncm.value.strip(),
                "cest": cest.value.strip(),
                "unidade": unidade.value.strip().upper(),
                "valor_unitario": float(valor_raw),
                "cst_csosn": cst_csosn.value,
                "origem": origem.value,
                "ean": ean_formatado(ean.value),
                "ativo": 1
            }

            # Validação de duplicidade de código
            if not modo_edicao and database.produto_existe(dados["codigo"]):
                raise ValueError("Já existe um produto com este código.")
            elif modo_edicao and dados["codigo"] != valores["codigo"] and database.produto_existe(dados["codigo"]):
                raise ValueError("Código em uso por outro produto.")

            if modo_edicao:
                database.atualizar_produto(produto_id, dados)
                msg_status.value = "✅ Produto atualizado com sucesso!"
            else:
                database.salvar_produto_db(dados)
                msg_status.value = f"✅ Produto '{dados['descricao']}' salvo com sucesso!"
                limpar_formulario()

            msg_status.color = ft.Colors.GREEN_600

        except ValueError as ve:
            msg_status.value = f"❌ {ve}"
            msg_status.color = ft.Colors.RED
        except Exception as ex:
            msg_status.value = f"❌ Erro inesperado: {ex}"
            msg_status.color = ft.Colors.RED

        page.update()

    formulario = ft.Column([
        ft.Text("📦 Cadastro de Produtos", size=22, weight="bold"),

        ft.Card(content=ft.Container(padding=10, content=ft.Column([
            ft.Text("🔖 Identificação", size=16, weight="bold"),
            ft.Row([ean, codigo], spacing=10),
            descricao,
        ]))),

        ft.Card(content=ft.Container(padding=10, content=ft.Column([
            ft.Text("🧾 Informações Fiscais", size=16, weight="bold"),
            ft.Row([ncm, cest], spacing=10),
            ft.Row([cst_csosn, origem], spacing=10),
        ]))),

        ft.Card(content=ft.Container(padding=10, content=ft.Column([
            ft.Text("🛒 Comercialização", size=16, weight="bold"),
            ft.Row([unidade, valor_unitario], spacing=10),
        ]))),

        ft.Row([
            ft.ElevatedButton("Salvar", icon=ft.Icons.SAVE, on_click=salvar_produto),
            ft.ElevatedButton("Limpar", icon=ft.Icons.CLEAR_ALL, on_click=limpar_formulario),
        ]),
        msg_status
    ], spacing=20)

    conteudo.content = ft.Container(content=formulario, padding=20)
    page.update()


def tela_listagem_produtos(page: ft.Page, conteudo: ft.Container):
    todos_produtos = database.listar_produtos()

    busca = ft.TextField(
        label="🔍 Buscar por código ou descrição...",
        on_change=lambda e: atualizar_tabela(e.control.value),
        expand=True
    )

    tabela_produtos = ft.DataTable(columns=[], rows=[], expand=True)

    def atualizar_tabela(texto_busca=""):
        texto_busca = texto_busca.lower().strip()
        tabela_produtos.rows.clear()

        filtrados = [
            p for p in todos_produtos
            if texto_busca in p[1].lower() or texto_busca in p[2].lower()
        ] if texto_busca else todos_produtos

        for produto in filtrados:
            id_, ean_val, desc_val, ncm_val, val_unit = produto
            linha = ft.DataRow(cells=[
                ft.DataCell(ft.Text(ean_val)),
                ft.DataCell(ft.Text(desc_val)),
                ft.DataCell(ft.Text(ncm_val)),
                ft.DataCell(ft.Text(f"R$ {val_unit:.2f}")),
                ft.DataCell(ft.Row([
                    ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, id=id_: carregar_edicao_produto(id)),
                    ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, tooltip="Excluir", on_click=lambda e, id=id_: excluir_produto_direto(id)),
                ]))
            ])
            tabela_produtos.rows.append(linha)

        tabela_produtos.columns = [
            ft.DataColumn(label=ft.Text("EAN")),
            ft.DataColumn(label=ft.Text("Descrição")),
            ft.DataColumn(label=ft.Text("NCM")),
            ft.DataColumn(label=ft.Text("Valor Unitário")),
            ft.DataColumn(label=ft.Text("Ações")),
        ]
        page.update()

    def carregar_edicao_produto(id_produto):
        produto = database.buscar_produto_por_id(id_produto)
        if produto:
            (
                id_, codigo_val, desc_val, ncm_val, cest_val,
                un_val, val_unit, cst_val, ori_val, ean_val, ativo
            ) = produto
            tela_cadastro_produtos(page, conteudo, modo_edicao=True, produto_id=id_, valores={
                "codigo": codigo_val,
                "descricao": desc_val,
                "ncm": ncm_val,
                "cest": cest_val,
                "unidade": un_val,
                "valor_unitario": str(val_unit),
                "cst_csosn": cst_val,
                "origem": ori_val,
                "ean": ean_val,
            })

    def excluir_produto_direto(id_produto):
        try:
            database.excluir_produto(id_produto)
            page.snack_bar = ft.SnackBar(content=ft.Text("✅ Produto excluído com sucesso."), bgcolor=ft.Colors.GREEN_600, duration=2000)
        except Exception as erro:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"❌ Erro ao excluir: {erro}"), bgcolor=ft.Colors.RED, duration=4000)
        finally:
            page.snack_bar.open = True
            tela_listagem_produtos(page, conteudo)

    btn_novo = ft.ElevatedButton("➕ Novo Produto", on_click=lambda e: tela_cadastro_produtos(page, conteudo))

    atualizar_tabela()

    conteudo.content = ft.Column([
        ft.Text("📦 Lista de Produtos", size=22, weight="bold"),
        ft.Row([btn_novo, busca], spacing=10),
        tabela_produtos
    ], scroll=ft.ScrollMode.AUTO, expand=True)
    page.update()
