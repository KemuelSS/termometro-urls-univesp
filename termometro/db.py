import sqlite3

from .config import DB_PATH


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            trust_score INTEGER,
            data_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn


def salvar_consulta(url, trust_score):
    conn = get_db_connection()
    conn.execute('INSERT INTO consultas (url, trust_score) VALUES (?, ?)', (url, trust_score))
    conn.commit()
    conn.close()


def listar_historico(limite=5):
    conn = get_db_connection()
    historico = conn.execute(
        'SELECT url, trust_score FROM consultas ORDER BY id DESC LIMIT ?', (limite,)
    ).fetchall()
    conn.close()
    return historico
