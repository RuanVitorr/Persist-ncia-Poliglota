from db_sqlite import criar_tabelas, inserir_restaurante, listar_restaurantes
import sqlite3

DB_NAME = "persistencia.db"

# 1️⃣ Criar tabelas
criar_tabelas()

# 2️⃣ Inserir alguns estados e cidades
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Inserir estados
estados = ["Paraíba", "São Paulo", "Rio de Janeiro"]
for e in estados:
    cursor.execute("INSERT OR IGNORE INTO estados (nome) VALUES (?)", (e,))

# Inserir cidades (vinculadas aos estados)
# Paraíba
cursor.execute("INSERT OR IGNORE INTO cidades (nome, estado_id) VALUES (?, ?)", ("João Pessoa", 1))
cursor.execute("INSERT OR IGNORE INTO cidades (nome, estado_id) VALUES (?, ?)", ("Campina Grande", 1))
# São Paulo
cursor.execute("INSERT OR IGNORE INTO cidades (nome, estado_id) VALUES (?, ?)", ("São Paulo", 2))
cursor.execute("INSERT OR IGNORE INTO cidades (nome, estado_id) VALUES (?, ?)", ("Campinas", 2))
# Rio de Janeiro
cursor.execute("INSERT OR IGNORE INTO cidades (nome, estado_id) VALUES (?, ?)", ("Rio de Janeiro", 3))
cursor.execute("INSERT OR IGNORE INTO cidades (nome, estado_id) VALUES (?, ?)", ("Niterói", 3))

conn.commit()
conn.close()

# 3️⃣ Inserir restaurante de teste
inserir_restaurante(
    nome="Restaurante do Ruan",
    estado_id=1,  # Paraíba
    cidade_id=1,  # João Pessoa
    cardapio_principal="Carne de sol, macaxeira frita, arroz e feijão"
)

# 4️⃣ Listar restaurantes cadastrados
restaurantes = listar_restaurantes()
print("\nRestaurantes cadastrados atualmente:")
for r in restaurantes:
    print(r)
