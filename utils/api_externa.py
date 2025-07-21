import re
import requests

def buscar_endereco_por_cep(cep: str):
    """
    Consulta a API ViaCEP e retorna um dicionário com dados do endereço.
    Retorna None se o CEP for inválido ou não encontrado.
    """
    cep = re.sub(r'\D', '', cep)

    if len(cep) != 8:
        return None

    try:
        resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if resposta.status_code == 200:
            dados = resposta.json()
            if "erro" not in dados:
                return dados
    except Exception as e:
        print(f"[Erro ViaCEP] {e}")

    return None


def buscar_dados_cnpj(cnpj: str):
    """
    Consulta a API ReceitaWS e retorna os dados do CNPJ como dicionário.
    Retorna None se o CNPJ for inválido, não encontrado ou em caso de erro.
    """
    cnpj = re.sub(r'\D', '', cnpj)

    if len(cnpj) != 14:
        return None

    try:
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
        headers = {"Accept": "application/json"}
        resposta = requests.get(url, headers=headers)

        if resposta.status_code == 200:
            dados = resposta.json()
            if dados.get("status") == "OK":
                return dados
    except Exception as e:
        print(f"[Erro ReceitaWS] {e}")

    return None

import requests

def consultar_cnpj(cnpj):
    try:
        cnpj = ''.join(filter(str.isdigit, cnpj))  # remove pontuações
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            raise Exception("Erro ao consultar CNPJ")

        data = response.json()

        if data.get("status") == "ERROR":
            raise Exception(data.get("message", "Erro desconhecido"))

        return {
            "razao_social": data.get("nome"),
            "ie": data.get("ie", ""),  # IE não é sempre retornado
            "logradouro": data.get("logradouro"),
            "numero": data.get("numero"),
            "bairro": data.get("bairro"),
            "municipio": data.get("municipio"),
            "uf": data.get("uf"),
            "cep": data.get("cep"),
            "fone": data.get("telefone"),
        }
    except Exception as e:
        raise Exception(f"Erro na consulta do CNPJ: {e}")
