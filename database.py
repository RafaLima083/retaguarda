import sqlite3

        # Cria a tabela "clientes" se ainda não existir
   
def criar_tabela_clientes():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf_cnpj TEXT NOT NULL UNIQUE,
            cep TEXT,
            logradouro TEXT,
            numero TEXT,
            complemento TEXT,
            bairro TEXT,
            cidade TEXT,
            uf TEXT,
            telefone TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

# Cria a tabela "produtos" se ainda não existir
def criar_tabela_produtos():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            descricao TEXT NOT NULL,
            ncm TEXT NOT NULL,
            cest TEXT,            
            unidade TEXT NOT NULL,            
            valor_unitario REAL NOT NULL,
            cst_csosn TEXT NOT NULL,
            origem TEXT NOT NULL,
            ean TEXT,
            ativo INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()
                   



# Salva um novo cliente no banco de dados
def salvar_cliente_db(dados):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (
            nome, cpf_cnpj, cep, logradouro, numero,
            complemento, bairro, cidade, uf, telefone, email
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tuple(dados.values()))
    conn.commit()
    conn.close()


# Verifica se já existe um cliente com o CPF/CNPJ informado
def cliente_existe(cpf_cnpj):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM clientes WHERE cpf_cnpj = ?", (cpf_cnpj,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None


# Lista todos os clientes (para a tela de listagem)
def listar_clientes():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, cpf_cnpj, telefone, email FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes


# Busca um cliente específico pelo ID (para edição)
def buscar_cliente_por_id(cliente_id):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente


# Atualiza os dados de um cliente
def atualizar_cliente(cliente_id, dados):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    campos = ", ".join([f"{chave} = ?" for chave in dados])
    valores = list(dados.values()) + [cliente_id]
    cursor.execute(f"UPDATE clientes SET {campos} WHERE id = ?", valores)
    conn.commit()
    conn.close()


# Remove um cliente do banco (opcional, se necessário)
def excluir_cliente(cliente_id:int):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()

def salvar_produto_db(dados: dict):
    """
    Salva um novo produto no banco de dados.
    Espera um dicionário com os campos definidos na tabela produtos.
    """
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO produtos (
            codigo, descricao, ncm, cest,  unidade,
            valor_unitario, cst_csosn, origem, ean, ativo
        )
        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados["codigo"],
        dados["descricao"],
        dados["ncm"],
        dados["cest"],        
        dados["unidade"],
        dados["valor_unitario"],
        dados["cst_csosn"],
        dados["origem"],
        dados["ean"],
        dados["ativo"]
    ))

    conn.commit()
    conn.close()

def produto_existe(codigo: str) -> bool:
    """
    Verifica se já existe um produto com o código informado.
    """
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM produtos WHERE codigo = ?", (codigo,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def listar_produtos():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id,ean, descricao, ncm, valor_unitario FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def buscar_produto_por_id(produto_id: int):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    produto = cursor.fetchone()
    conn.close()
    return produto

def excluir_produto(produto_id: int):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()

def criar_tabela_emitente():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emitente (
            id INTEGER PRIMARY KEY,
            razao_social TEXT,
            cnpj TEXT,
            ie TEXT,
            crt TEXT,
            logradouro TEXT,
            numero TEXT,
            bairro TEXT,
            municipio TEXT,
            uf TEXT,
            cep TEXT,
            fone TEXT,
            cmun TEXT
        )
    """)
    conn.commit()
    conn.close()

def salvar_emitente(dados: dict):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM emitente")  # Sempre um único emitente
    cursor.execute("""
        INSERT INTO emitente (
            razao_social, cnpj, ie, crt,
            logradouro, numero, bairro,
            municipio, uf, cep, fone, cmun
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados["razao_social"],
        dados["cnpj"],
        dados["ie"],
        dados["crt"],
        dados["logradouro"],
        dados["numero"],
        dados["bairro"],
        dados["municipio"],
        dados["uf"],
        dados["cep"],
        dados["fone"],
        dados["cmun"]
    ))

    conn.commit()
    conn.close()

def carregar_emitente():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emitente LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "razao_social": row[1],
            "cnpj": row[2],
            "ie": row[3],
            "crt": row[4],
            "logradouro": row[5],
            "numero": row[6],
            "bairro": row[7],
            "municipio": row[8],
            "uf": row[9],
            "cep": row[10],
            "fone": row[11],
            "cmun": row[12],
        }
    return None

def obter_configuracao(chave):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", (chave,))
    resultado = cursor.fetchone()

    conn.close()
    return resultado[0] if resultado else None

def criar_tabela_configuracoes():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracoes (
            chave TEXT PRIMARY KEY,
            valor TEXT
        )
    """)
    conn.commit()
    conn.close()

def criar_tabela_nfe():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas_fiscais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER,
            serie INTEGER,
            data_emissao TEXT,
            cliente_id INTEGER,
            valor_total REAL,
            chave TEXT,
            xml TEXT,
            status TEXT,
            protocolo TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)
    conn.commit()
    conn.close()
