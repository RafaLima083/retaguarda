import flet as ft
import database
from utils.api_externa import consultar_cnpj


def tela_configuracoes_emitente(page: ft.Page, conteudo: ft.Container):
    
    # Campos
    razao_social = ft.TextField(label="Razão Social", expand=True)
    cnpj = ft.TextField(
        label="CNPJ", 
        width=200,         
    )
    ie = ft.TextField(label="Inscrição Estadual", width=200)
    crt = ft.Dropdown(
        label="Regime Tributário (CRT)",
        options=[
            ft.dropdown.Option("1", "1 - Simples Nacional"),
            ft.dropdown.Option("2", "2 - Simples Nacional - excesso de sublimite da receita bruta "),
            ft.dropdown.Option("3", "3 - Regime Normal"),
            ft.dropdown.Option("4", "4 - MEI"),
        ],
        width=250
    )

    logradouro = ft.TextField(label="Logradouro", expand=True)
    numero = ft.TextField(label="Número", width=150)
    bairro = ft.TextField(label="Bairro", expand=True)
    municipio = ft.TextField(label="Município", expand=True)
    uf = ft.TextField(label="UF", width=100, max_length=2)
    cep = ft.TextField(label="CEP", width=150)
    fone = ft.TextField(label="Telefone", width=200)
    cmun = ft.TextField(label="Código IBGE Município", width=200)

    msg_status = ft.Text("")

    def salvar_config(e):
        try:
            if not razao_social.value or not cnpj.value or not ie.value or not crt.value:
                raise ValueError("Preencha os campos obrigatórios")

            dados = {
                "razao_social": razao_social.value.strip(),
                "cnpj": cnpj.value.strip(),
                "ie": ie.value.strip(),
                "crt": crt.value,
                "logradouro": logradouro.value.strip(),
                "numero": numero.value.strip(),
                "bairro": bairro.value.strip(),
                "municipio": municipio.value.strip(),
                "uf": uf.value.strip().upper(),
                "cep": cep.value.strip(),
                "fone": fone.value.strip(),
                "cmun": cmun.value.strip()
            }

            database.salvar_emitente(dados)

            msg_status.value = "✅ Emitente salvo com sucesso!"
            msg_status.color = ft.Colors.GREEN
        except Exception as err:
            msg_status.value = f"❌ Erro: {err}"
            msg_status.color = ft.Colors.RED
        page.update()

    def carregar_config():
        dados = database.carregar_emitente()
        if dados:
            razao_social.value = dados["razao_social"]
            cnpj.value = dados["cnpj"]
            ie.value = dados["ie"]
            crt.value = dados["crt"]
            logradouro.value = dados["logradouro"]
            numero.value = dados["numero"]
            bairro.value = dados["bairro"]
            municipio.value = dados["municipio"]
            uf.value = dados["uf"]
            cep.value = dados["cep"]
            fone.value = dados["fone"]
            cmun.value = dados["cmun"]
            page.update()

    def buscar_cnpj():
        try:
            if not cnpj.value.strip():
                raise ValueError("Informe um CNPJ para busca")

            dados = consultar_cnpj(cnpj.value)

            razao_social.value = dados["razao_social"]
            logradouro.value = dados["logradouro"]
            numero.value = dados["numero"]
            bairro.value = dados["bairro"]
            municipio.value = dados["municipio"]
            uf.value = dados["uf"]
            cep.value = dados["cep"]
            fone.value = dados["fone"]

            msg_status.value = "✅ Dados carregados do CNPJ com sucesso!"
            msg_status.color = ft.Colors.GREEN
            page.update()
        except Exception as err:
            msg_status.value = f"❌ {err}"
            msg_status.color = ft.Colors.RED
        page.update()

    import requests

    btn_buscar_cnpj = ft.ElevatedButton("🔍 Buscar", on_click=lambda e: buscar_cnpj())

    # Layout
    formulario = ft.Column([
        ft.Text("⚙️ Configurações do Emitente", size=22, weight="bold"),
        ft.Divider(),

        ft.Row([razao_social]),
        ft.Row([cnpj,btn_buscar_cnpj, ie, crt]),
        ft.Text("📍 Endereço", size=16),
        ft.Row([logradouro, numero]),
        ft.Row([bairro, municipio]),
        ft.Row([uf, cep, fone]),
        ft.Row([cmun]),
        ft.Row([
            ft.ElevatedButton("Salvar", icon=ft.Icons.SAVE, on_click=salvar_config)
        ]),
        msg_status
    ], spacing=10)

    conteudo.content = ft.Container(content=formulario, padding=20)
    page.update()

    carregar_config()  # Carrega se houver
