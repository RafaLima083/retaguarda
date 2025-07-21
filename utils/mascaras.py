import re

def formatar_cpf_cnpj(valor: str) -> str:
    """
    Aplica máscara de CPF ou CNPJ automaticamente com base no número de dígitos.
    """
    numeros = re.sub(r'\D', '', valor)

    if len(numeros) <= 11:
        # CPF: 000.000.000-00
        return re.sub(r"(\d{3})(\d{3})(\d{3})(\d{0,2})", r"\1.\2.\3-\4", numeros)
    else:
        # CNPJ: 00.000.000/0000-00
        return re.sub(r"(\d{2})(\d{3})(\d{3})(\d{4})(\d{0,2})", r"\1.\2.\3/\4-\5", numeros)


def formatar_telefone(valor: str) -> str:
    """
    Aplica máscara ao número de telefone, diferenciando fixo e celular.
    """
    numeros = re.sub(r'\D', '', valor)
    if len(numeros) == 0:
        return ""

    if len(numeros) <= 10:
        # Fixo: (XX) XXXX-XXXX
        return re.sub(r"^(\d{0,2})(\d{0,4})(\d{0,4})$", r"(\1) \2-\3", numeros).strip(" ()-")
    else:
        # Celular: (XX) 9XXXX-XXXX
        return re.sub(r"^(\d{0,2})(\d{0,5})(\d{0,4})$", r"(\1) \2-\3", numeros).strip(" ()-")


def formatar_cep(valor: str) -> str:
    """
    Aplica máscara de CEP: 00000-000
    """
    numeros = re.sub(r'\D', '', valor)
    return re.sub(r"(\d{0,5})(\d{0,3})", r"\1-\2", numeros).strip("-")
