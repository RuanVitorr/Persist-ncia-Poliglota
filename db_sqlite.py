# FASE 1 — SQLite simples para RESTAURANTES
import sqlite3, os
from typing import List, Dict, Any, Optional

DB_PATH = os.getenv("SQLITE_URL", "poliglota.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS restaurantes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL,
            pais TEXT NOT NULL,
            faixa_preco TEXT,        -- $, $$, $$$, $$$$
            nota_media REAL          -- 0.0 a 5.0
        );
        """)
        c.commit()

def inserir_restaurante(data: Dict[str, Any]) -> int:
    with get_conn() as c:
        cur = c.execute("""
            INSERT INTO restaurantes (nome, categoria, cidade, estado, pais, faixa_preco, nota_media)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data["nome"], data["categoria"], data["cidade"], data["estado"], data["pais"],
              data.get("faixa_preco"), data.get("nota_media")))
        c.commit()
        return cur.lastrowid

def listar_restaurantes() -> List[Dict[str, Any]]:
    with get_conn() as c:
        rows = c.execute("""
            SELECT id, nome, categoria, cidade, estado, pais, faixa_preco, nota_media
            FROM restaurantes ORDER BY nome ASC
        """).fetchall()
        return [dict(r) for r in rows]

def obter_restaurante(rest_id: int) -> Optional[Dict[str, Any]]:
    with get_conn() as c:
        r = c.execute("""
            SELECT id, nome, categoria, cidade, estado, pais, faixa_preco, nota_media
            FROM restaurantes WHERE id = ?
        """, (rest_id,)).fetchone()
        return dict(r) if r else None

def atualizar_restaurante(rest_id: int, data: Dict[str, Any]) -> bool:
    with get_conn() as c:
        cur = c.execute("""
            UPDATE restaurantes
            SET nome=?, categoria=?, cidade=?, estado=?, pais=?, faixa_preco=?, nota_media=?
            WHERE id=?
        """, (data["nome"], data["categoria"], data["cidade"], data["estado"], data["pais"],
              data.get("faixa_preco"), data.get("nota_media"), rest_id))
        c.commit()
        return cur.rowcount > 0

def deletar_restaurante(rest_id: int) -> bool:
    with get_conn() as c:
        cur = c.execute("DELETE FROM restaurantes WHERE id = ?", (rest_id,))
        c.commit()
        return cur.rowcount > 0