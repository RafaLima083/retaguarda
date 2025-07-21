# 📦 Sistema de Retaguarda com Emissão de NF-e (Modelo 55)

Este projeto é um sistema de retaguarda desktop desenvolvido em Python com [Flet](https://flet.dev) para gerenciamento de produtos, clientes e **emissão de NF-e modelo 55**, com suporte a:

- Cadastro de produtos com tributação
- Cadastro de clientes com endereço completo
- Geração de XML da NF-e (modelo 55)
- Assinatura digital do XML com certificado A1
- Interface responsiva com Flet
- Banco de dados SQLite

---

## 🚀 Tecnologias utilizadas

- Python 3.11+
- [Flet](https://flet.dev)
- SQLite
- PyNFe (versão da TadaSoftware)
- xmlsec (assinatura digital)
- OpenSSL

---

## 🔧 Como rodar o projeto

1. **Clone o repositório:**

```bash
git clone https://github.com/SEU_USUARIO/retaguarda.git
cd retaguarda
