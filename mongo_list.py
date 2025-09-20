from pymongo import MongoClient

# 1️⃣ Conectar ao MongoDB local
client = MongoClient("mongodb://localhost:27017/")

# 2️⃣ Selecionar o banco e a coleção
db = client["persistencia_poliglota"]
restaurantes_col = db["restaurantes"]

# 3️⃣ Buscar todos os restaurantes
restaurantes = restaurantes_col.find()

print("Restaurantes cadastrados atualmente:")
for r in restaurantes:
    print(f"Nome: {r['nome']}, Estado: {r['estado']}, Cidade: {r['cidade']}, Cardápio: {r['cardapio_principal']}")
