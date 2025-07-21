# 📦 Sistema de Retaguarda com Emissão de NF-e

Este projeto é um sistema completo de retaguarda em Python com interface gráfica utilizando [Flet](https://flet.dev) e suporte à emissão de NF-e modelo 55.

## ✨ Funcionalidades

- Cadastro e listagem de **clientes** e **produtos**
- Busca inteligente com filtros dinâmicos
- Geração de **XML da NF-e** conforme layout oficial
- Assinatura digital do XML com certificado A1 (.pfx)
- Integração futura com Sefaz
- Interface gráfica responsiva e moderna com Flet

## 🚀 Tecnologias

- Python 3.12+
- Flet
- PyNFe (NF-e 4.0)
- SQLite

## 📦 Instalação

```bash
# Crie o ambiente virtual
python -m venv venv
# Ative o ambiente
# Windows:
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
