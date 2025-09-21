import sqlite3

DB_NAME = "persistencia.db"  # caminho relativo para o banco SQLite

# Conecta ao banco
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# 1️⃣ Mostrar todas as tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()
print("Tabelas existentes no banco:")
for t in tabelas:
    print("-", t[0])

# 2️⃣ Mostrar todos os restaurantes cadastrados
cursor.execute("""
    SELECT r.id, r.nome, e.nome, c.nome, r.cardapio_principal
    FROM restaurantes r
    JOIN estados e ON r.estado_id = e.id
    JOIN cidades c ON r.cidade_id = c.id
""")
restaurantes = cursor.fetchall()

print("\nRestaurantes cadastrados atualmente:")
for r in restaurantes:
    print(f"ID: {r[0]}, Nome: {r[1]}, Estado: {r[2]}, Cidade: {r[3]}, Cardápio: {r[4]}")

conn.close()