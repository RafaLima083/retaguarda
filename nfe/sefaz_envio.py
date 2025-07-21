import zeep
import requests
from lxml import etree
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin

# WebService da SEFAZ SP em homologação (exemplo com 4.00)
WSDL_URL = "https://homologacao.nfe.fazenda.sp.gov.br/ws/nfeautorizacao4.asmx?WSDL"

def enviar_nfe_para_sefaz(xml_assinado: str):
    try:
        # Plugin para capturar request/response SOAP
        history = HistoryPlugin()

        # Criando cliente SOAP com o WSDL
        session = requests.Session()
        session.verify = False  # Desabilita verificação SSL (⚠️ Apenas para testes!)
        transport = Transport(session=session)
        client = zeep.Client(wsdl=WSDL_URL, transport=transport, plugins=[history])

        # Envelope do XML
        envelope = f"""
        <nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NFeAutorizacao4">
            {xml_assinado}
        </nfeDadosMsg>
        """

        # Requisição SOAP
        resposta = client.service.nfeAutorizacaoLote(
            nfeDadosMsg=etree.fromstring(envelope.encode("utf-8"))
        )

        # Captura o XML de resposta
        raw_response = etree.tostring(history.last_received["envelope"], pretty_print=True).decode("utf-8")

        # Aqui, você pode extrair os campos do XML com lxml ou retornar o XML inteiro
        return {
            "sucesso": True,
            "xml_resposta": raw_response,
            "cStat": "100" if "<cStat>100</cStat>" in raw_response else "erro",
            "xMotivo": "Autorizado" if "<cStat>100</cStat>" in raw_response else "Erro na SEFAZ",
            "nProt": extrair_protocolo(raw_response)
        }

    except Exception as erro:
        return {
            "sucesso": False,
            "erro": str(erro)
        }


def extrair_protocolo(xml: str):
    try:
        raiz = etree.fromstring(xml.encode("utf-8"))
        protocolo = raiz.find(".//{*}nProt")
        return protocolo.text if protocolo is not None else "Não retornado"
    except:
        return "Erro ao extrair"
