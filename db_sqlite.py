
import sqlite3, os
from typing import List, Dict, Any, Optional

DB_NAME = "persistencia.db"

def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    with get_conn() as conn:
        cursor = conn.cursor()
                # Tabela de estados
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS estados (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
        """)

        # Tabela de cidades
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cidades (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nome      TEXT NOT NULL,
            estado_id INTEGER NOT NULL,
            FOREIGN KEY (estado_id) REFERENCES estados(id),
            UNIQUE (nome, estado_id)
        )
        """)

        # Tabela de restaurantes (igual à sua, mas já pronta para evoluir)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurantes (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            nome               TEXT NOT NULL,
            estado_id          INTEGER NOT NULL,
            cidade_id          INTEGER NOT NULL,
            cardapio_principal TEXT NOT NULL,
            -- Se quiser evoluir depois:
            -- categoria          TEXT,
            -- faixa_preco        TEXT,  -- $, $$, $$$, $$$$
            -- nota_media         REAL,  -- 0..5
            FOREIGN KEY (estado_id) REFERENCES estados(id),
            FOREIGN KEY (cidade_id) REFERENCES cidades(id)
        )
        """)

        conn.commit()
        print("Banco SQLite e tabelas criadas/atualizadas com sucesso!")

# -------------------- ESTADOS --------------------
def inserir_estado(nome: str) -> int:
    with get_conn() as conn:
        cur = conn.execute("INSERT OR IGNORE INTO estados (nome) VALUES (?)", (nome,))
        if cur.lastrowid:
            conn.commit()
            return cur.lastrowid
        row = conn.execute("SELECT id FROM estados WHERE nome = ?", (nome,)).fetchone()
        return row["id"]

def obter_estado_por_nome(nome: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute("SELECT id, nome FROM estados WHERE nome = ?", (nome,)).fetchone()
        return dict(row) if row else None

def listar_estados() -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute("SELECT id, nome FROM estados ORDER BY nome").fetchall()
        return [dict(r) for r in rows]

# -------------------- CIDADES --------------------
def inserir_cidade(nome: str, estado_id: int) -> int:
    with get_conn() as conn:
        cur = conn.execute("INSERT OR IGNORE INTO cidades (nome, estado_id) VALUES (?, ?)", (nome, estado_id))
        if cur.lastrowid:
            conn.commit()
            return cur.lastrowid
        row = conn.execute("SELECT id FROM cidades WHERE nome = ? AND estado_id = ?", (nome, estado_id)).fetchone()
        return row["id"]

def obter_cidade_por_nome(nome: str, estado_id: int) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute("SELECT id, nome, estado_id FROM cidades WHERE nome = ? AND estado_id = ?", (nome, estado_id)).fetchone()
        return dict(row) if row else None

def listar_cidades(estado_id: Optional[int] = None) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        if estado_id:
            rows = conn.execute("SELECT id, nome, estado_id FROM cidades WHERE estado_id = ? ORDER BY nome", (estado_id,)).fetchall()
        else:
            rows = conn.execute("SELECT id, nome, estado_id FROM cidades ORDER BY nome").fetchall()
        return [dict(r) for r in rows]

# -------------------- RESTAURANTES --------------------
def inserir_restaurante(nome: str, estado_id: int, cidade_id: int, cardapio_principal: str) -> int:
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO restaurantes (nome, estado_id, cidade_id, cardapio_principal)
            VALUES (?, ?, ?, ?)
        """, (nome, estado_id, cidade_id, cardapio_principal))
        conn.commit()
        return cur.lastrowid
    

def listar_restaurantes(estado_id: Optional[int] = None, cidade_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Lista com JOIN — já retorna nomes do estado e da cidade.
    """
    with get_conn() as conn:
        base = """
            SELECT r.id,
                   r.nome,
                   r.cardapio_principal,
                   r.estado_id,
                   e.nome AS estado_nome,
                   r.cidade_id,
                   c.nome AS cidade_nome
              FROM restaurantes r
              JOIN estados e ON e.id = r.estado_id
              JOIN cidades c ON c.id = r.cidade_id
        """
        conds, params = [], []
        if estado_id:
            conds.append("r.estado_id = ?")
            params.append(estado_id)
        if cidade_id:
            conds.append("r.cidade_id = ?")
            params.append(cidade_id)

        if conds:
            base += " WHERE " + " AND ".join(conds)
        base += " ORDER BY r.nome"

        rows = conn.execute(base, tuple(params)).fetchall()
        return [dict(r) for r in rows]

def obter_restaurante(rest_id: int) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        r = conn.execute("""
            SELECT r.id,
                   r.nome,
                   r.cardapio_principal,
                   r.estado_id,
                   e.nome AS estado_nome,
                   r.cidade_id,
                   c.nome AS cidade_nome
              FROM restaurantes r
              JOIN estados e ON e.id = r.estado_id
              JOIN cidades c ON c.id = r.cidade_id
             WHERE r.id = ?
        """, (rest_id,)).fetchone()
        return dict(r) if r else None

def atualizar_restaurante(rest_id: int, nome: str, estado_id: int, cidade_id: int, cardapio_principal: str) -> bool:
    with get_conn() as conn:
        cur = conn.execute("""
            UPDATE restaurantes
               SET nome = ?, estado_id = ?, cidade_id = ?, cardapio_principal = ?
             WHERE id = ?
        """, (nome, estado_id, cidade_id, cardapio_principal, rest_id))
        conn.commit()
        return cur.rowcount > 0

def deletar_restaurante(rest_id: int) -> bool:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM restaurantes WHERE id = ?", (rest_id,))
        conn.commit()
        return cur.rowcount > 0