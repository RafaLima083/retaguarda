import csv

# Carrega a tabela IBPT uma vez em memória
def carregar_ncm_ibpt(caminho="utils/tabela_ncm.csv"):
    ncm_validos = set()
    with open(caminho, newline="", encoding="latin1") as f:
        leitor = csv.DictReader(f, delimiter=';')
        next(leitor)  # pula o cabeçalho
        for linha in leitor:
            ncm = linha.get("codigo", "").strip()
            if len(ncm) == 8:
                ncm_validos.add(ncm)
    return ncm_validos

NCM_VALIDOS = carregar_ncm_ibpt()

def ncm_existe(ncm: str) -> bool:
    return ncm.strip() in NCM_VALIDOS
