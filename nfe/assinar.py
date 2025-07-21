from signxml import XMLSigner
from lxml import etree

def assinar_nfe(xml: str, cert_pem: str, key_pem: str) -> str:
    ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}
    root = etree.fromstring(xml.encode("utf-8"))

    infNFe = root.find(".//nfe:infNFe", namespaces=ns)
    if infNFe is None:
        raise ValueError("❌ Tag infNFe não encontrada para assinatura.")

    # Assinador com SHA-1 (exigido pela SEFAZ)
    signer = XMLSigner(
        method="enveloped",
        signature_algorithm="rsa-sha1",
        digest_algorithm="sha1"
    )

    signed_infNFe = signer.sign(
        infNFe,
        key=key_pem.encode(),
        cert=cert_pem.encode(),
        reference_uri="#" + infNFe.get("Id")  # ex: NFe3512...
    )

    # Substitui o infNFe original pelo assinado
    parent = infNFe.getparent()
    parent.replace(infNFe, signed_infNFe)

    return etree.tostring(root, encoding="utf-8", xml_declaration=True).decode()
