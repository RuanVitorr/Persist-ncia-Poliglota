from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["persistencia_poliglota"]
colecao = db["restaurantes"]

def inserir_restaurante(nome, estado, cidade, cardapio, coordenadas=None,
                        avaliacoes=None, fotos=None, horario_funcionamento=None):
    if avaliacoes is None:
        avaliacoes = []
    if fotos is None:
        fotos = []
    if horario_funcionamento is None:
        horario_funcionamento = {
            "segunda": "08:00-18:00",
            "terça": "08:00-18:00",
            "quarta": "08:00-18:00",
            "quinta": "08:00-18:00",
            "sexta": "08:00-18:00",
            "sábado": "08:00-14:00",
            "domingo": "Fechado"
        }

    doc = {
        "nome": nome,
        "estado": estado,
        "cidade": cidade,
        "cardapio_principal": cardapio,
        "avaliacoes": avaliacoes,
        "fotos": fotos,
        "horario_funcionamento": horario_funcionamento,
        "coordenadas": coordenadas if coordenadas else {"lat": None, "lon": None}
    }

    resultado = colecao.insert_one(doc)
    print(f"Restaurante inserido no MongoDB com _id: {resultado.inserted_id}")

def listar_restaurantes():
    return list(colecao.find({}, {"_id": 0}))
