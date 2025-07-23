import sqlite3

def conectar():
    return sqlite3.connect("banco.db")

# Cria a tabela "clientes" se ainda não existir
   
def criar_tabela_clientes():
    conn = conectar()
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
            email TEXT,
            rg_ie TEXT 
        )
    """)
    conn.commit()
    conn.close()

# Cria a tabela "produtos" se ainda não existir
def criar_tabela_produtos():
    conn = conectar()
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

# Cria a tabela emitende se ainda não exixtir                  
def criar_tabela_emitente():
    conn = conectar()
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

# Cria a tebela configurações se ainda não existir 
def criar_tabela_configuracoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracoes (
            chave TEXT PRIMARY KEY,
            valor TEXT
        )
    """)
    conn.commit()
    conn.close()

# Cria tabela para NF-e
def criar_tabela_nfe():
    conn = conectar()
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

# Salva um novo cliente no banco de dados
def salvar_cliente_db(dados):
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (
                    nome, cpf_cnpj, cep, logradouro, numero,
                    complemento, bairro, cidade, uf, telefone, email, rg_ie
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
            """,( 
                dados["nome"],
                dados["cpf_cnpj"],
                dados["cep"],
                dados["logradouro"],
                dados["numero"],
                dados["complemento"],
                dados["bairro"],
                dados["cidade"],
                dados["uf"],
                dados["telefone"],
                dados["email"],
                dados["rg_ie"]
            ))
            conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade ao salvar cliente: {e}")
            
# Verifica se já existe um cliente com o CPF/CNPJ informado
def cliente_existe(cpf_cnpj):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM clientes WHERE cpf_cnpj = ?", (cpf_cnpj,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

# Lista todos os clientes (para a tela de listagem)
def listar_clientes():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, cpf_cnpj, telefone, email FROM clientes")       
        return cursor.fetchall()

# Busca um cliente específico pelo ID (para edição)
def buscar_cliente_por_id(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente

# Atualiza os dados de um cliente
def atualizar_cliente(id, dados):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes SET
            nome = ?, cpf_cnpj = ?, cep = ?, logradouro = ?, numero = ?,
            complemento = ?, bairro = ?, cidade = ?, uf = ?, telefone = ?,
            email = ?, rg_ie = ?
        WHERE id = ?
    """, (
        dados["nome"],
        dados["cpf_cnpj"],
        dados["cep"],
        dados["logradouro"],
        dados["numero"],
        dados["complemento"],
        dados["bairro"],
        dados["cidade"],
        dados["uf"],
        dados["telefone"],
        dados["email"],
        dados["rg_ie"],
        id
    ))
    conn.commit()
    conn.close()

# Remove um cliente do banco 
def excluir_cliente(cliente_id: int):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conn.commit()

# Salva os produtos no banco
def salvar_produto_db(dados: dict):   
    conn = conectar()
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

# Verifica se já existe o codigo de barras no banco 
def produto_existe(codigo: str) -> bool:    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM produtos WHERE codigo = ?", (codigo,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

# Lista produtos 
def listar_produtos():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, ean, descricao, ncm, valor_unitario FROM produtos")
        return cursor.fetchall()

# Busca produtos 
def buscar_produto_por_id(produto_id: int):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        return cursor.fetchone()

# Remove produto do banco 
def excluir_produto(produto_id: int):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()

# Salva os dados do emitente
def salvar_emitente(dados: dict):
    conn = conectar()
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

    cursor.execute("INSERT OR REPLACE INTO configuracoes (chave, valor) VALUES (?, ?)", ("crt", dados["crt"]))
    
    conn.commit()
    conn.close()

# Carrega os dados do emitente
def carregar_emitente():
    conn = conectar()
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
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", (chave,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def atualizar_produto(id, dados):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE produtos SET
                codigo = ?, descricao = ?, ncm = ?, cest = ?, unidade = ?,
                valor_unitario = ?, cst_csosn = ?, origem = ?, ean = ?, ativo = ?
            WHERE id = ?
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
            dados["ativo"],
            id
        ))
        conn.commit()
# Para chamar no arquivo main.py 
def inicializar_banco():
        criar_tabela_clientes()
        criar_tabela_produtos()
        criar_tabela_emitente()
        criar_tabela_configuracoes()
        criar_tabela_nfe()