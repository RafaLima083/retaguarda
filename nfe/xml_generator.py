# nfe/xml_generator.py

import xml.etree.ElementTree as ET
from datetime import datetime
from database import carregar_emitente, buscar_cliente_por_id, buscar_produto_por_id

def gerar_xml_nfe(cliente_id: int, itens: list, observacoes: str) -> str:
    emitente = carregar_emitente()
    cliente = buscar_cliente_por_id(cliente_id)

    if not emitente or not cliente:
        raise ValueError("Emitente ou cliente não encontrados.")

    versao = "4.00"
    cUF = emitente["cmun"][:2]  # exemplo: "35" para SP
    cNF = "12345678"
    serie = "1"
    numero = "1"
    dhEmi = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")

    raiz = ET.Element("nfeProc", {
        "xmlns": "http://www.portalfiscal.inf.br/nfe",
        "versao": versao
    })

    nfe = ET.SubElement(raiz, "NFe")
    infNFe = ET.SubElement(nfe, "infNFe", {
        "Id": f"NFe{emitente['cnpj']}{numero.zfill(9)}",
        "versao": versao
    })

    # ide
    ide = ET.SubElement(infNFe, "ide")
    ET.SubElement(ide, "cUF").text = cUF
    ET.SubElement(ide, "cNF").text = cNF
    ET.SubElement(ide, "natOp").text = "VENDA"
    ET.SubElement(ide, "mod").text = "55"
    ET.SubElement(ide, "serie").text = serie
    ET.SubElement(ide, "nNF").text = numero
    ET.SubElement(ide, "dhEmi").text = dhEmi
    ET.SubElement(ide, "tpNF").text = "1"
    ET.SubElement(ide, "idDest").text = "1"
    ET.SubElement(ide, "cMunFG").text = emitente["cmun"]
    ET.SubElement(ide, "tpImp").text = "1"
    ET.SubElement(ide, "tpEmis").text = "1"
    ET.SubElement(ide, "cDV").text = "0"
    ET.SubElement(ide, "tpAmb").text = "2"  # 2 = homologação
    ET.SubElement(ide, "finNFe").text = "1"
    ET.SubElement(ide, "indFinal").text = "1"
    ET.SubElement(ide, "indPres").text = "1"
    ET.SubElement(ide, "procEmi").text = "0"
    ET.SubElement(ide, "verProc").text = "1.0"

    # emitente
    emit = ET.SubElement(infNFe, "emit")
    ET.SubElement(emit, "CNPJ").text = emitente["cnpj"]
    ET.SubElement(emit, "xNome").text = emitente["razao_social"]

    ender_emit = ET.SubElement(emit, "enderEmit")
    ET.SubElement(ender_emit, "xLgr").text = emitente["logradouro"]
    ET.SubElement(ender_emit, "nro").text = emitente["numero"]
    ET.SubElement(ender_emit, "xBairro").text = emitente["bairro"]
    ET.SubElement(ender_emit, "cMun").text = emitente["cmun"]
    ET.SubElement(ender_emit, "xMun").text = emitente["municipio"]
    ET.SubElement(ender_emit, "UF").text = emitente["uf"]
    ET.SubElement(ender_emit, "CEP").text = emitente["cep"]
    ET.SubElement(ender_emit, "fone").text = emitente["fone"]

    ET.SubElement(emit, "IE").text = emitente["ie"]
    ET.SubElement(emit, "CRT").text = emitente["crt"]

    # destinatário
    dest = ET.SubElement(infNFe, "dest")
    doc = cliente[2]
    ET.SubElement(dest, "CPF" if len(doc) == 11 else "CNPJ").text = doc
    ET.SubElement(dest, "xNome").text = cliente[1]

    ender_dest = ET.SubElement(dest, "enderDest")
    ET.SubElement(ender_dest, "xLgr").text = cliente[3] or ""
    ET.SubElement(ender_dest, "nro").text = cliente[4] or ""
    ET.SubElement(ender_dest, "xBairro").text = cliente[6] or ""
    ET.SubElement(ender_dest, "cMun").text = "3550308"  # SP - Exemplo
    ET.SubElement(ender_dest, "xMun").text = cliente[7] or ""
    ET.SubElement(ender_dest, "UF").text = cliente[8] or ""
    ET.SubElement(ender_dest, "CEP").text = cliente[5] or ""
    ET.SubElement(ender_dest, "fone").text = cliente[9] or ""

    # produtos
    total_nf = 0
    for idx, item in enumerate(itens, start=1):
        produto = buscar_produto_por_id(item["produto_id"])

        det = ET.SubElement(infNFe, "det", {"nItem": str(idx)})
        prod = ET.SubElement(det, "prod")
        ET.SubElement(prod, "cProd").text = produto[1]
        ET.SubElement(prod, "cEAN").text = produto[9] or ""
        ET.SubElement(prod, "xProd").text = produto[2]
        ET.SubElement(prod, "NCM").text = produto[3]
        ET.SubElement(prod, "CEST").text = produto[4] or ""
        ET.SubElement(prod, "CFOP").text = "5102"
        ET.SubElement(prod, "uCom").text = produto[5]
        ET.SubElement(prod, "qCom").text = str(item["quantidade"])
        ET.SubElement(prod, "vUnCom").text = f"{produto[6]:.2f}"
        ET.SubElement(prod, "vProd").text = f"{item['subtotal']:.2f}"
        ET.SubElement(prod, "cEANTrib").text = produto[9] or ""
        ET.SubElement(prod, "uTrib").text = produto[5]
        ET.SubElement(prod, "qTrib").text = str(item["quantidade"])
        ET.SubElement(prod, "vUnTrib").text = f"{produto[6]:.2f}"
        ET.SubElement(prod, "indTot").text = "1"

        # Imposto (exemplo simplificado)
        imposto = ET.SubElement(det, "imposto")
        icms = ET.SubElement(imposto, "ICMS")
        icms00 = ET.SubElement(icms, "ICMS00")
        ET.SubElement(icms00, "orig").text = produto[8]
        ET.SubElement(icms00, "CST").text = produto[7]
        ET.SubElement(icms00, "modBC").text = "3"
        ET.SubElement(icms00, "vBC").text = f"{item['subtotal']:.2f}"
        ET.SubElement(icms00, "pICMS").text = "0.00"
        ET.SubElement(icms00, "vICMS").text = "0.00"

        total_nf += item["subtotal"]

    # totais
    total = ET.SubElement(infNFe, "total")
    ICMSTot = ET.SubElement(total, "ICMSTot")
    ET.SubElement(ICMSTot, "vBC").text = f"{total_nf:.2f}"
    ET.SubElement(ICMSTot, "vICMS").text = "0.00"
    ET.SubElement(ICMSTot, "vProd").text = f"{total_nf:.2f}"
    ET.SubElement(ICMSTot, "vNF").text = f"{total_nf:.2f}"

    # transporte
    transp = ET.SubElement(infNFe, "transp")
    ET.SubElement(transp, "modFrete").text = "9"  # sem frete

    # adicionais
    infAdic = ET.SubElement(infNFe, "infAdic")
    ET.SubElement(infAdic, "infCpl").text = observacoes or ""

    # gerar XML final
    xml = ET.tostring(raiz, encoding="utf-8", method="xml")
    return xml.decode("utf-8")
