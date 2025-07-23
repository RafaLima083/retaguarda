import flet as ft
import re
import database
from utils.validacoes import validar_cpf_cnpj
from utils.mascaras import formatar_cpf_cnpj, formatar_telefone, formatar_cep
from utils.api_externa import buscar_endereco_por_cep, buscar_dados_cnpj


def tela_cadastro_clientes(page: ft.Page, conteudo: ft.Container, modo_edicao=False, cliente_id=None, valores=None):
    nome = ft.TextField(label="Nome completo", expand=True, value=valores["nome"] if valores else "")
    cpf_cnpj = ft.TextField(
        label="CPF ou CNPJ",
        expand=True,
        value=valores["cpf_cnpj"] if valores else "",
        on_change=lambda e: atualizar_mascara_cpf_cnpj(e),
        on_blur=lambda e: preencher_dados_cnpj(e),
    )
    rg_ie = ft.TextField(label="RG ou Inscrição estadual", expand=True, value=valores.get("rg_ie", "") if valores else "")
    telefone = ft.TextField(label="Telefone", expand=True, value=valores["telefone"] if valores else "", on_change=lambda e: atualizar_mascara_telefone(e))
    cep = ft.TextField(label="CEP", expand=True, value=valores["cep"] if valores else "", on_change=lambda e: atualizar_mascara_cep(e), on_blur=lambda e: preencher_endereco_por_cep(e))

    logradouro = ft.TextField(label="Logradouro", expand=True, value=valores["logradouro"] if valores else "")
    numero = ft.TextField(label="Número", expand=True, value=valores["numero"] if valores else "")
    complemento = ft.TextField(label="Complemento", expand=True, value=valores["complemento"] if valores else "")
    bairro = ft.TextField(label="Bairro", expand=True, value=valores["bairro"] if valores else "")
    cidade = ft.TextField(label="Cidade", expand=True, value=valores["cidade"] if valores else "")
    uf = ft.TextField(label="Estado", expand=True, value=valores["uf"] if valores else "")
    email = ft.TextField(label="E-mail", expand=True, value=valores["email"] if valores else "")

    def atualizar_mascara_cpf_cnpj(e):
        cpf_cnpj.value = formatar_cpf_cnpj(cpf_cnpj.value)

    def atualizar_mascara_telefone(e):
        telefone.value = formatar_telefone(telefone.value)

    def atualizar_mascara_cep(e):
        cep.value = formatar_cep(cep.value)

    def preencher_dados_cnpj(e):
        cnpj = re.sub(r'\D', '', cpf_cnpj.value)
        if len(cnpj) == 14:
            dados = buscar_dados_cnpj(cnpj)
            if dados:
                nome.value = dados.get("nome", "")
                telefone.value = dados.get("telefone", "")
                cep.value = dados.get("cep", "")
                logradouro.value = dados.get("logradouro", "")
                numero.value = dados.get("numero", "")
                complemento.value = dados.get("complemento", "")
                bairro.value = dados.get("bairro", "")
                cidade.value = dados.get("municipio", "")
                uf.value = dados.get("uf", "")
                rg_ie.value = dados.get("RG_IE", "")

                page.snack_bar = ft.SnackBar(content=ft.Text("✅ CNPJ preenchido automaticamente"), bgcolor=ft.Colors.GREEN)
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text("❌ CNPJ inválido ou falha na consulta"), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
            page.update()

    def preencher_endereco_por_cep(e):
        dados = buscar_endereco_por_cep(cep.value)
        if dados:
            logradouro.value = dados.get("logradouro", "")
            bairro.value = dados.get("bairro", "")
            cidade.value = dados.get("localidade", "")
            uf.value = dados.get("uf", "")
            page.snack_bar = ft.SnackBar(content=ft.Text("✅ Endereço preenchido via CEP"), bgcolor=ft.Colors.GREEN)
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("❌ CEP inválido ou não encontrado"), bgcolor=ft.Colors.RED)
        page.snack_bar.open = True
        page.update()

    def limpar_formulario(e=None):
        for campo in [nome, cpf_cnpj, rg_ie, cep, logradouro, numero, complemento, bairro, cidade, uf, telefone, email]:
            campo.value = ""
        page.update()

    def salvar_cliente(e):
        if nome.value.strip() == "":
            mensagem = "❌ Nome é obrigatório"
            cor = ft.Colors.RED
        elif not modo_edicao and database.cliente_existe(cpf_cnpj.value):
            mensagem = "❌ CPF ou CNPJ já cadastrado"
            cor = ft.Colors.RED
        elif not validar_cpf_cnpj(cpf_cnpj.value):
            mensagem = "❌ CPF ou CNPJ inválido"
            cor = ft.Colors.RED
        elif len(re.sub(r'\D', '', telefone.value)) < 10:
            mensagem = "❌ Telefone incompleto"
            cor = ft.Colors.RED
        elif len(re.sub(r'\D', '', cep.value)) != 8:
            mensagem = "❌ CEP inválido"
            cor = ft.Colors.RED
        else:
            dados = {
                "nome": nome.value,
                "cpf_cnpj": cpf_cnpj.value,
                "cep": cep.value,
                "logradouro": logradouro.value,
                "numero": numero.value,
                "complemento": complemento.value,
                "bairro": bairro.value,
                "cidade": cidade.value,
                "uf": uf.value,
                "telefone": telefone.value,
                "email": email.value,
                "rg_ie": rg_ie.value,
            }

            if modo_edicao:
                database.atualizar_cliente(cliente_id, dados)
                mensagem = "✅ Cliente atualizado com sucesso!"
            else:
                database.salvar_cliente_db(dados)
                mensagem = f"✅ Cliente '{dados['nome']}' salvo com sucesso!"
                limpar_formulario()

            cor = ft.Colors.GREEN

        page.snack_bar = ft.SnackBar(content=ft.Text(mensagem), bgcolor=cor)
        page.snack_bar.open = True
        page.update()

    # Botões
    botoes = ft.Row([
        ft.ElevatedButton(text="Salvar", icon=ft.Icons.SAVE, on_click=salvar_cliente),
        ft.ElevatedButton(text="Limpar", icon=ft.Icons.CLEAR_ALL, on_click=limpar_formulario),
    ], spacing=10)

    formulario = ft.Column([
        ft.Text("👤 Cadastro de Clientes", size=22, weight="bold"),        
        cpf_cnpj, nome, rg_ie,
        ft.Row([cep, numero, complemento], spacing=10),
        logradouro, bairro,
        ft.Row([cidade, uf], spacing=10),
        telefone, email,
        botoes,
        
    ], spacing=10)

    conteudo.content = ft.Container(
        content=formulario,
        padding=20,
        alignment=ft.alignment.top_center,
        width=600
    )
    page.update()


def tela_listagem_clientes(page: ft.Page, conteudo: ft.Container):
    clientes = database.listar_clientes()

    def carregar_edicao_cliente(e, id_cliente):
        cliente = database.buscar_cliente_por_id(id_cliente)
        if cliente:
            (
                id_, nome_val, cpf_val, cep_val, log_val, num_val,
                comp_val, bairro_val, cidade_val, uf_val, tel_val, email_val, rg_ie_val,
            ) = cliente

            tela_cadastro_clientes(
                page, conteudo, modo_edicao=True, cliente_id=id_,
                valores={
                    "nome": nome_val,
                    "cpf_cnpj": cpf_val,
                    "cep": cep_val,
                    "logradouro": log_val,
                    "numero": num_val,
                    "complemento": comp_val,
                    "bairro": bairro_val,
                    "cidade": cidade_val,
                    "uf": uf_val,
                    "telefone": tel_val,
                    "email": email_val,
                    "rg_ie": rg_ie_val,
                }
            )

    def excluir_cliente_direto(e, id_cliente):
        try:
            database.excluir_cliente(id_cliente)
            #page.snack_bar = ft.SnackBar(content=ft.Text("✅ Cliente excluído com sucesso."), bgcolor=ft.Colors.GREEN_600, duration=3000)
            page.open(ft.SnackBar(ft.Text("✅ Cliente excluído com sucesso."), bgcolor=ft.Colors.GREEN_600, duration=3000))
        except Exception as erro:
            page.open = (ft.SnackBar(ft.Text(f"❌ Erro ao excluir: {erro}"), bgcolor=ft.Colors.RED, duration=4000))
        finally:
            page.open = ft.SnackBar=True
            tela_listagem_clientes(page, conteudo)

    linhas = []
    for cliente in clientes:
        id_, nome, cpf_cnpj, telefone, email = cliente
        linha = ft.DataRow(cells=[
            ft.DataCell(ft.Text(nome)),
            ft.DataCell(ft.Text(cpf_cnpj)),
            ft.DataCell(ft.Text(telefone)),
            ft.DataCell(ft.Text(email)),
            ft.DataCell(
                ft.Row([
                    ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, id=id_: carregar_edicao_cliente(e, id)),
                    ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, tooltip="Excluir", on_click=lambda e, id=id_: excluir_cliente_direto(e, id)),
                ])
            )
        ])
        linhas.append(linha)

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Nome")),
            ft.DataColumn(label=ft.Text("CPF/CNPJ")),
            ft.DataColumn(label=ft.Text("Telefone")),
            ft.DataColumn(label=ft.Text("E-mail")),
            ft.DataColumn(label=ft.Text("Ações")),
        ],
        rows=linhas
    )

    conteudo.content = ft.Column([
        ft.Text("📋 Lista de Clientes", size=22, weight="bold"),
        tabela
    ], scroll=ft.ScrollMode.AUTO, expand=True)
    page.update()
