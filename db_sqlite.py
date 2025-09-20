import sqlite3

DB_NAME = "persistencia.db"

def criar_tabelas():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabela de estados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)

    # Tabela de cidades
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        estado_id INTEGER NOT NULL,
        FOREIGN KEY (estado_id) REFERENCES estados(id)
    )
    """)

    # Tabela de restaurantes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        estado_id INTEGER NOT NULL,
        cidade_id INTEGER NOT NULL,
        cardapio_principal TEXT NOT NULL,
        FOREIGN KEY (estado_id) REFERENCES estados(id),
        FOREIGN KEY (cidade_id) REFERENCES cidades(id)
    )
    """)

    conn.commit()
    conn.close()
    print("Banco SQLite e tabelas de restaurantes criadas com sucesso!")

# Inserir restaurante
def inserir_restaurante(nome, estado_id, cidade_id, cardapio_principal):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO restaurantes (nome, estado_id, cidade_id, cardapio_principal)
        VALUES (?, ?, ?, ?)
    """, (nome, estado_id, cidade_id, cardapio_principal))
    conn.commit()
    conn.close()
    print(f"Restaurante {nome} inserido com sucesso!")

# Listar restaurantes
def listar_restaurantes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurantes")
    restaurantes = cursor.fetchall()
    conn.close()
    return restaurantes
