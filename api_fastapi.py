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

load_dotenv()

class RestauranteCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    categoria: str = Field(min_length=1, max_length=60)
    cidade: str = Field(min_length=1, max_length=80)
    estado: str = Field(min_length=1, max_length=10)
    pais: str = Field(min_length=1, max_length=60)
    faixa_preco: Optional[str] = Field(default=None, description="$, $$, $$$ ou $$$$")
    nota_media: Optional[float] = Field(default=None, ge=0, le=5)

    @field_validator("faixa_preco")
    @classmethod
    def valida_preco(cls, v):
        if not v:
            return None
        if v not in {"$", "$$", "$$$", "$$$$"}:
            raise ValueError("faixa_preco deve ser $, $$, $$$ ou $$$$")
        return v

class Restaurante(RestauranteCreate):
    id: int

app = FastAPI(
    title="Persistência Poliglota — Fase 1 (Restaurantes)",
    version="1.0.0",
    description="CRUD de restaurantes em SQLite.",
)

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:8501")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://127.0.0.1:8501", "http://localhost:8501"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    db.init_db()

@app.get("/health")
def health():
    return {"status": "ok", "fase": 1, "entidade": "restaurantes"}

@app.post("/restaurantes", response_model=Restaurante, status_code=201)
def criar_restaurante(payload: RestauranteCreate):
    new_id = db.inserir_restaurante(payload.model_dump())
    return Restaurante(id=new_id, **payload.model_dump())

@app.get("/restaurantes", response_model=List[Restaurante])
def listar_restaurantes():
    return [Restaurante(**r) for r in db.listar_restaurantes()]

@app.get("/restaurantes/{restaurante_id}", response_model=Restaurante)
def obter_restaurante(restaurante_id: int):
    r = db.obter_restaurante(restaurante_id)
    if not r:
        raise HTTPException(404, "Restaurante não encontrado")
    return Restaurante(**r)

@app.put("/restaurantes/{restaurante_id}", response_model=Restaurante)
def atualizar_restaurante(restaurante_id: int, payload: RestauranteCreate):
    ok = db.atualizar_restaurante(restaurante_id, payload.model_dump())
    if not ok:
        raise HTTPException(404, "Restaurante não encontrado")
    return Restaurante(**db.obter_restaurante(restaurante_id))

@app.delete("/restaurantes/{restaurante_id}", status_code=204)
def deletar_restaurante(restaurante_id: int):
    ok = db.deletar_restaurante(restaurante_id)
    if not ok:
        raise HTTPException(404, "Restaurante não encontrado")
    return
