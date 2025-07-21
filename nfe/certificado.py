from OpenSSL import crypto

def carregar_certificado(caminho_pfx: str, senha: str):
    with open(caminho_pfx, 'rb') as f:
        pfx_data = f.read()

    p12 = crypto.load_pkcs12(pfx_data, senha.encode())

    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())
    key = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
    
    return cert.decode(), key.decode()
