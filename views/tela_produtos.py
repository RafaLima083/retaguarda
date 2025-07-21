import flet as ft
import re
import database
from utils.ncm_validador import ncm_existe



def tela_cadastro_produtos(page: ft.Page, conteudo: ft.Container, modo_edicao=False, produto_id=None, valores=None):

    regime_emitente = database.obter_configuracao("crt")  # exemplo: "1", "3", etc
    def opcoes_cst_por_regime(regime: str):       
        if regime == "1" :
            return [
                ft.dropdown.Option("101", "101 - Simples Nacional com crédito"),
                ft.dropdown.Option("102", "102 - Simples Nacional sem crédito"),
                ft.dropdown.Option("103", "103 - Isenção (Simples Nacional)"),
                ft.dropdown.Option("201", "201 - SN c/ ST e crédito"),
                ft.dropdown.Option("202", "202 - SN c/ ST sem crédito"),
                ft.dropdown.Option("500", "500 - ICMS cobrado anteriormente por ST (Simples Nacional)"),
            ]
        elif regime == "2" :
            return [
                ft.dropdown.Option("101", "101 - Simples Nacional com crédito"),
                ft.dropdown.Option("102", "102 - Simples Nacional sem crédito"),
                ft.dropdown.Option("103", "103 - Isenção (Simples Nacional)"),
                ft.dropdown.Option("201", "201 - SN c/ ST e crédito"),
                ft.dropdown.Option("202", "202 - SN c/ ST sem crédito"),
                ft.dropdown.Option("500", "500 - ICMS cobrado anteriormente por ST (Simples Nacional)"),
            ]
        elif regime == "4" :
            return [
                ft.dropdown.Option("101", "101 - Simples Nacional com crédito"),
                ft.dropdown.Option("102", "102 - Simples Nacional sem crédito"),
                ft.dropdown.Option("103", "103 - Isenção (Simples Nacional)"),
                ft.dropdown.Option("201", "201 - SN c/ ST e crédito"),
                ft.dropdown.Option("202", "202 - SN c/ ST sem crédito"),
                ft.dropdown.Option("500", "500 - ICMS cobrado anteriormente por ST (Simples Nacional)"),
            ]
        else:
            return [
                ft.dropdown.Option("00", "00 - Tributação integral"),
                ft.dropdown.Option("20", "20 - Com redução de base de cálculo"),
                ft.dropdown.Option("40", "40 - Isenta"),
                ft.dropdown.Option("41", "41 - Não tributada"),
                ft.dropdown.Option("60", "60 - ICMS cobrado anteriormente (ST)"),
            ]
    codigo = ft.TextField(label="Código Interno", width=120)
    descricao = ft.TextField(label="Descrição do Produto", width=800)
    ncm = ft.TextField(
        label="NCM",
        width=120,
        max_length=8,
        input_filter=ft.InputFilter(
            regex_string=r"[0-9.]",
            replacement_string=""
        )
    )
    cest = ft.TextField(
        label="CEST (Preencher se ST)",
          width=120,
          max_length=7,
          input_filter=ft.InputFilter(
              regex_string=r"[0-9.]",
              replacement_string=""
          )
        )    
    unidade =ft.Dropdown(
        label="UN, LT, PC...",
        width=200,
        options=[
            ft.dropdown.Option("UN"),
            ft.dropdown.Option("KG"),
            ft.dropdown.Option("PC"),
            ft.dropdown.Option("LT"),
            ft.dropdown.Option("MT"),
        ]
    )  
    valor_unitario = ft.TextField(
        label="Valor Venda", 
        width=120,
        input_filter=ft.InputFilter(
            regex_string=r"[0-9.,]",
            replacement_string=""
        )
    )
    cst_csosn = ft.Dropdown(
        label="CST/CSOSN",
        width=250,        
        options=opcoes_cst_por_regime(regime_emitente)
    )
    origem = ft.Dropdown(
        label="Origem do produto",
        width=250,
        options=[
            ft.dropdown.Option("0", "0 - Nacional, exceto as indicadas nos códigos 3, 4, 5 e 8"),
            ft.dropdown.Option("1", "1 - Estrangeira - Importação direta"),
            ft.dropdown.Option("2", "2 - Estrangeira - Adquirida no mercado interno"),
            ft.dropdown.Option("3", "3 - Nacional, mercadoria ou bem com conteúdo de importação > 40%"),
            ft.dropdown.Option("4", "4 - Nacional, produção conforme processos produtivos básicos"),
            ft.dropdown.Option("5", "5 - Nacional, com conteúdo de importação ≤ 40%"),
            ft.dropdown.Option("6", "6 - Estrangeira - Sem similar nacional, conforme CAMEX"),
            ft.dropdown.Option("7", "7 - Estrangeira - Adquirida no mercado interno, sem similar nacional"),
            ft.dropdown.Option("8", "8 - Nacional, mercadoria com conteúdo de importação > 70%"),
        ]
    )
    ean = ft.TextField(
        label="Código de Barras",
        width=200,
        max_length=13,
        input_filter=ft.InputFilter(
            regex_string=r"[0-9]",
            replacement_string=""
        )        
    )
    msg_status = ft.Text("")

    # Preenche valores se for edição
    if valores:
        codigo.value = valores.get("codigo", "")
        descricao.value = valores.get("descricao", "")
        ncm.value = valores.get("ncm", "")
        cest.value = valores.get("cest", "")        
        unidade.value = valores.get("unidade", "")        
        valor_unitario.value = valores.get("valor_unitario", "")
        cst_csosn.value = valores.get("cst_csosn", "")
        origem.value = valores.get("origem", "")
        ean.value = valores.get("ean", "")

    def limpar_formulario(e=None):
        for campo in [
            codigo, descricao, ncm, cest, unidade, 
            valor_unitario, cst_csosn, origem, ean
        ]:
            campo.value = ""
            msg_status.value = ""
        page.update()

    def ean_formatado(valor):
        numeros = re.sub(r'\D', '', valor)  # remove qualquer coisa que não for número

        if not numeros:
            return ""  # EAN vazio (não obrigatório)

        if len(numeros) > 13:
            raise ValueError("EAN deve ter no máximo 13 dígitos")

        return numeros.zfill(13)  # completa com zeros à esquerda

    def salvar_produto(e):
        

        try:
            # Validações
            if codigo.value.strip() == "" or descricao.value.strip() == "":
                raise ValueError("Código e descrição são obrigatórios")
            if not re.match(r'^\d{8}$', ncm.value.strip()):
                raise ValueError("NCM inválido (deve conter 8 dígitos)")
            if not ncm_existe(ncm.value.strip()):
                raise ValueError("NCM não encontrado na tabela IBPT")
            if not unidade.value.strip():
                raise ValueError("Unidade é obrigatória")
            if not valor_unitario.value.strip().replace(',', '.').replace('.', '', 1).isdigit():
                raise ValueError("Valor unitário inválido")
            if cst_csosn.value.startswith("---") or not cst_csosn.value:
                raise ValueError("Selecione um CST/CSOSN válido")
            if not origem.value:
                raise ValueError("Origem do produto obrigatória")

            dados = {
                "codigo": codigo.value.strip().upper(),
                "descricao": descricao.value.strip().upper(),
                "ncm": ncm.value.strip(),
                "cest": cest.value.strip(),
                "unidade": unidade.value.strip().upper(),
                "valor_unitario": float(valor_unitario.value.strip().replace(",", ".")),
                "cst_csosn": cst_csosn.value,
                "origem": origem.value,
                "ean": ean_formatado(ean.value),
                "ativo": 1
            }

            if not modo_edicao and database.produto_existe(dados["codigo"]):
                raise ValueError("Já existe um produto com este código")

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

    

    # Botões
    btn_salvar = ft.ElevatedButton("Salvar Produto", icon=ft.Icons.SAVE, on_click=salvar_produto)
    btn_limpar = ft.ElevatedButton("Limpar", icon=ft.Icons.CLEAR_ALL, on_click=limpar_formulario)

    # Layout
    formulario = ft.Column([
    ft.Text("📦 Cadastro de Produtos", size=22, weight="bold"),

    # 🔖 Seção: Identificação
    ft.Card(
        content=ft.Container(
            padding=10,
            content=ft.Column([
                ft.Text("🔖 Identificação", size=16, weight="bold"),
                ft.Divider(),
                ft.Row([ean,codigo], spacing=10),
                descricao,
            ], spacing=10)
        )
    ),

    # 🧾 Seção: Informações Fiscais
    ft.Card(
        content=ft.Container(
            padding=10,
            content=ft.Column([
                ft.Text("🧾 Informações Fiscais", size=16, weight="bold"),
                ft.Divider(),
                ft.Row([ncm, cest], spacing=10),
                ft.Row([cst_csosn, origem], spacing=10),
            ], spacing=10)
        )
    ),

    # 🛒 Seção: Comercialização
    ft.Card(
        content=ft.Container(
            padding=10,
            content=ft.Column([
                ft.Text("🛒 Comercialização", size=16, weight="bold"),
                ft.Divider(),
                ft.Row([unidade, valor_unitario], spacing=10),
            ], spacing=10)
        )
    ),

    # 🔘 Ações
    ft.Row([btn_salvar, btn_limpar], spacing=10),
    msg_status
], spacing=20)

    conteudo.content = ft.Container(content=formulario, padding=20)
    page.update()

def tela_listagem_produtos(page: ft.Page, conteudo: ft.Container):
    todos_produtos = database.listar_produtos()  # pega todos
    resultados = todos_produtos  # usado para filtragem

    busca = ft.TextField(
        label="🔎 Buscar por código ou nome...",
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
            id_,ean, descricao, ncm,valor_unitario = produto
            linha = ft.DataRow(
                cells=[
                    
                    ft.DataCell(ft.Text(ean)),
                    ft.DataCell(ft.Text(descricao)),
                    ft.DataCell(ft.Text(ncm)),
                    
                    
                    ft.DataCell(ft.Text(f"R$ {valor_unitario:.2f}")),
                    
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar produto",
                                on_click=lambda e, id=id_: carregar_edicao_produto(e, id)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                tooltip="Excluir produto",
                                on_click=lambda e, id=id_: excluir_produto_direto(e, id)
                            ),
                        ])
                    )
                ]
            )
            tabela_produtos.rows.append(linha)

        tabela_produtos.columns = [            
            ft.DataColumn(label=ft.Text("EAN")),
            ft.DataColumn(label=ft.Text("Descrição")),
            ft.DataColumn(label=ft.Text("NCM")),            
            ft.DataColumn(label=ft.Text("Valor Unit.")),
            ft.DataColumn(label=ft.Text("Ações")),
        ]
        page.update()

    def carregar_edicao_produto(e, id_produto):
        produto = database.buscar_produto_por_id(id_produto)
        if produto:
            (
                id_,
                codigo_val, descricao_val, ncm_val, cest_val, 
                unidade_val,  valor_val, cst_val, origem_val, ean_val, ativo_val
            ) = produto

            tela_cadastro_produtos(
                page,
                conteudo,
                modo_edicao=True,
                produto_id=id_,
                valores={
                    "codigo": codigo_val,
                    "descricao": descricao_val,
                    "ncm": ncm_val,
                    "cest": cest_val,
                    "unidade": unidade_val,                    
                    "valor_unitario": str(valor_val),
                    "cst_csosn": cst_val,
                    "origem": origem_val,
                    "ean": ean_val,
                }
            )

    def excluir_produto_direto(e, id_produto):
        try:
            database.excluir_produto(id_produto)
            page.snack_bar = ft.SnackBar(
                content=ft.Text("✅ Produto excluído com sucesso."),
                bgcolor=ft.Colors.GREEN_600,
                behavior=ft.SnackBarBehavior.FLOATING,
                duration=2000,
            )
            page.snack_bar.open = True
        except Exception as erro:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ Erro ao excluir: {erro}"),
                bgcolor=ft.Colors.RED,
                behavior=ft.SnackBarBehavior.FLOATING,
                duration=4000,
            )
            page.snack_bar.open = True
        finally:
            tela_listagem_produtos(page, conteudo)

    atualizar_tabela()

    conteudo.content = ft.Column(
        [
            ft.Text("📦 Lista de Produtos", size=22, weight="bold"),
            busca,
            tabela_produtos
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
    page.update()
    

