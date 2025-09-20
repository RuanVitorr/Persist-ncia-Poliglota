from pymongo import MongoClient

# 1️⃣ Conectar ao MongoDB local
client = MongoClient("mongodb://localhost:27017/")

# Seleciona o banco de dados
db = client["persistencia_poliglota"]

# Seleciona a coleção de restaurantes
restaurantes_col = db["restaurantes"]

# 2️⃣ Criar um restaurante de teste
restaurante = {
    "nome": "Restaurante da Angela",
    "estado": "Paraíba",
    "cidade": "João Pessoa",
    "cardapio_principal": "sushi, temaki, macarrão com coisas yaksoba",
    "avaliacoes": [],
    "fotos": [],
    "horario_funcionamento": {
        "segunda": "08:00-18:00",
        "terça": "08:00-18:00",
        "quarta": "08:00-18:00",
        "quinta": "08:00-18:00",
        "sexta": "08:00-18:00",
        "sábado": "08:00-14:00",
        "domingo": "Fechado"
    }
}

# Insere no MongoDB
resultado = restaurantes_col.insert_one(restaurante)
print("Restaurante inserido com _id:", resultado.inserted_id)

# 3️⃣ Listar restaurantes cadastrados
print("\nRestaurantes cadastrados atualmente:")
for r in restaurantes_col.find():
    print(f"Nome: {r['nome']}, Estado: {r['estado']}, Cidade: {r['cidade']}, Cardápio: {r['cardapio_principal']}")
