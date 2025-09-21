# api_fastapi.py

from typing import List
from typing import Optional
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv
import db_sqlite as db

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

# -------------------- Config --------------------
load_dotenv()
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:8501")

app = FastAPI(
    title="Persistência Poliglota — Restaurantes (Normalizado)",
    version="1.0.0",
    description="Estados, Cidades e Restaurantes com SQLite (FKs). "
                "Criação de restaurantes por IDs e por Nomes.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://127.0.0.1:8501", "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Schemas --------------------
class EstadoCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=80)

class Estado(EstadoCreate):
    id: int

class CidadeCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=80)
    estado_id: int

class Cidade(CidadeCreate):
    id: int

class RestauranteCreateIDs(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    estado_id: int
    cidade_id: int
    cardapio_principal: str = Field(min_length=1, max_length=120)

class RestauranteCreateNames(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    estado_nome: str = Field(min_length=1, max_length=80)
    cidade_nome: str = Field(min_length=1, max_length=80)
    cardapio_principal: str = Field(min_length=1, max_length=120)

class Restaurante(BaseModel):
    id: int
    nome: str
    cardapio_principal: str
    estado_id: int
    estado_nome: str
    cidade_id: int
    cidade_nome: str

# -------------------- Startup --------------------
@app.on_event("startup")
def on_startup():
    db.criar_tabelas()

# -------------------- Health --------------------
@app.get("/health")
def health():
    return {"status": "ok", "db": "sqlite", "modelo": "normalizado"}

# -------------------- ESTADOS --------------------
@app.post("/estados", response_model=Estado, status_code=201)
def criar_estado(payload: EstadoCreate):
    estado_id = db.inserir_estado(payload.nome)
    return Estado(id=estado_id, nome=payload.nome)

@app.get("/estados", response_model=List[Estado])
def listar_estados():
    rows = db.listar_estados()
    return [Estado(**r) for r in rows]

# -------------------- CIDADES --------------------
@app.post("/cidades", response_model=Cidade, status_code=201)
def criar_cidade(payload: CidadeCreate):
    # garante que estado existe
    estados = db.listar_estados()
    if not any(e["id"] == payload.estado_id for e in estados):
        raise HTTPException(400, "estado_id inexistente")
    cidade_id = db.inserir_cidade(payload.nome, payload.estado_id)
    return Cidade(id=cidade_id, **payload.model_dump())

@app.get("/cidades", response_model=List[Cidade])
def listar_cidades(estado_id: Optional[int] = Query(default=None)):
    rows = db.listar_cidades(estado_id=estado_id)
    return [Cidade(**r) for r in rows]

# -------------------- RESTAURANTES --------------------
# 1) Criação por IDs (quando front já sabe os IDs)
@app.post("/restaurantes", response_model=Restaurante, status_code=201)
def criar_restaurante_ids(payload: RestauranteCreateIDs):
    # valida existência de estado/cidade
    estados = db.listar_estados()
    if not any(e["id"] == payload.estado_id for e in estados):
        raise HTTPException(400, "estado_id inexistente")

    cidades = db.listar_cidades(estado_id=payload.estado_id)
    if not any(c["id"] == payload.cidade_id for c in cidades):
        raise HTTPException(400, "cidade_id inexistente (ou não pertence ao estado_id informado)")

    rest_id = db.inserir_restaurante(
        nome=payload.nome,
        estado_id=payload.estado_id,
        cidade_id=payload.cidade_id,
        cardapio_principal=payload.cardapio_principal,
    )
    r = db.obter_restaurante(rest_id)
    return Restaurante(**r)

# 2) Criação por Nomes (front envia texto e o backend resolve/insere estado/cidade)
@app.post("/restaurantes/por-nomes", response_model=Restaurante, status_code=201)
def criar_restaurante_por_nomes(payload: RestauranteCreateNames):
    rest_id = db.inserir_restaurante_por_nomes(
        nome=payload.nome,
        estado_nome=payload.estado_nome,
        cidade_nome=payload.cidade_nome,
        cardapio_principal=payload.cardapio_principal,
    )
    r = db.obter_restaurante(rest_id)
    return Restaurante(**r)

@app.get("/restaurantes", response_model=List[Restaurante])
def listar_restaurantes(
    estado_id: Optional[int] = Query(default=None),
    cidade_id: Optional[int] = Query(default=None),
):
    rows = db.listar_restaurantes(estado_id=estado_id, cidade_id=cidade_id)
    return [Restaurante(**r) for r in rows]

@app.get("/restaurantes/{restaurante_id}", response_model=Restaurante)
def obter_restaurante(restaurante_id: int):
    r = db.obter_restaurante(restaurante_id)
    if not r:
        raise HTTPException(404, "Restaurante não encontrado")
    return Restaurante(**r)

@app.put("/restaurantes/{restaurante_id}", response_model=Restaurante)
def atualizar_restaurante(restaurante_id: int, payload: RestauranteCreateIDs):
    # valida existência de estado/cidade
    estados = db.listar_estados()
    if not any(e["id"] == payload.estado_id for e in estados):
        raise HTTPException(400, "estado_id inexistente")

    cidades = db.listar_cidades(estado_id=payload.estado_id)
    if not any(c["id"] == payload.cidade_id for c in cidades):
        raise HTTPException(400, "cidade_id inexistente (ou não pertence ao estado_id informado)")

    ok = db.atualizar_restaurante(
        rest_id=restaurante_id,
        nome=payload.nome,
        estado_id=payload.estado_id,
        cidade_id=payload.cidade_id,
        cardapio_principal=payload.cardapio_principal,
    )
    if not ok:
        raise HTTPException(404, "Restaurante não encontrado")
    r = db.obter_restaurante(restaurante_id)
    return Restaurante(**r)

@app.delete("/restaurantes/{restaurante_id}", status_code=204)
def deletar_restaurante(restaurante_id: int):
    ok = db.deletar_restaurante(restaurante_id)
    if not ok:
        raise HTTPException(404, "Restaurante não encontrado")
    return