import sqlite3
import os
from datetime import date, timedelta

def get_db_path():
    if os.environ.get('RENDER') or os.environ.get('RAILWAY_ENVIRONMENT'):
        return '/tmp/kiosque.db'
    db_dir = os.path.join(os.path.dirname(__file__), '..', 'database')
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, 'kiosque.db')

DB_PATH = get_db_path()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS quiosques (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            nome       TEXT    NOT NULL,
            descricao  TEXT,
            capacidade INTEGER,
            preco_dia  REAL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            grupo_id        TEXT    NOT NULL,
            quiosque_id     INTEGER NOT NULL,
            usuario         TEXT    NOT NULL,
            data_reserva    TEXT    NOT NULL,
            data_inicio     TEXT    NOT NULL,
            data_fim        TEXT    NOT NULL,
            total_dias      INTEGER NOT NULL DEFAULT 1,
            nome_cliente    TEXT    NOT NULL,
            forma_pagamento TEXT    NOT NULL,
            status          TEXT    DEFAULT 'confirmada',
            criado_em       TEXT    DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (quiosque_id) REFERENCES quiosques(id)
        )
    ''')

    c.execute("SELECT COUNT(*) FROM usuarios")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO usuarios (login, senha) VALUES (?, ?)", ('123', '123'))

    c.execute("SELECT COUNT(*) FROM quiosques")
    if c.fetchone()[0] == 0:
        quiosques = [
            ('Quiosque 1 - Beira Mar',  'Vista privilegiada para o mar, ideal para eventos e churrascos ao ar livre.', 20, 350.00),
            ('Quiosque 2 - Jardim',     'Rodeado por jardins floridos, ambiente tranquilo e aconchegante.', 15, 280.00),
            ('Quiosque 3 - Piscina',    'Acesso exclusivo a piscina durante a locacao. Otimo para festas.', 25, 420.00),
            ('Quiosque 4 - Bosque',     'No coracao do bosque, sombra natural e ambiente rustico e especial.', 18, 300.00),
        ]
        c.executemany(
            "INSERT INTO quiosques (nome, descricao, capacidade, preco_dia) VALUES (?, ?, ?, ?)",
            quiosques
        )

    c.execute("SELECT COUNT(*) FROM reservas")
    if c.fetchone()[0] == 0:
        import uuid
        demo_grupos = [
            (1, 'demo', '2026-06-24', '2026-06-26', 'Carlos Souza',   'PIX'),
            (2, 'demo', '2026-06-24', '2026-06-24', 'Mariana Costa',  'Dinheiro'),
            (2, 'demo', '2026-06-27', '2026-06-28', 'Lucas Ferreira', 'PIX'),
            (3, 'demo', '2026-06-28', '2026-06-29', 'Julia Martins',  'Credito'),
            (4, 'demo', '2026-06-26', '2026-06-30', 'Beatriz Santos', 'Debito'),
        ]
        for qid, usr, di, df, nome, pag in demo_grupos:
            gid = str(uuid.uuid4())[:8]
            d_ini = date.fromisoformat(di)
            d_fim = date.fromisoformat(df)
            total = (d_fim - d_ini).days + 1
            cur = d_ini
            while cur <= d_fim:
                c.execute(
                    "INSERT INTO reservas (grupo_id,quiosque_id,usuario,data_reserva,data_inicio,data_fim,total_dias,nome_cliente,forma_pagamento) VALUES (?,?,?,?,?,?,?,?,?)",
                    (gid, qid, usr, cur.isoformat(), di, df, total, nome, pag)
                )
                cur += timedelta(days=1)

    conn.commit()
    conn.close()


def buscar_usuario(login, senha):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM usuarios WHERE login=? AND senha=?", (login, senha)
    ).fetchone()
    conn.close()
    return user

def listar_quiosques():
    conn = get_db()
    lista = conn.execute("SELECT * FROM quiosques").fetchall()
    conn.close()
    return lista

def buscar_quiosque(quiosque_id):
    conn = get_db()
    q = conn.execute("SELECT * FROM quiosques WHERE id=?", (quiosque_id,)).fetchone()
    conn.close()
    return q

def verificar_disponibilidade(quiosque_id, data):
    conn = get_db()
    r = conn.execute(
        "SELECT id FROM reservas WHERE quiosque_id=? AND data_reserva=? AND status='confirmada'",
        (quiosque_id, data)
    ).fetchone()
    conn.close()
    return r is None

def verificar_intervalo(quiosque_id, data_inicio, data_fim):
    conn = get_db()
    rows = conn.execute(
        "SELECT data_reserva FROM reservas WHERE quiosque_id=? AND status='confirmada' AND data_reserva BETWEEN ? AND ?",
        (quiosque_id, data_inicio, data_fim)
    ).fetchall()
    conn.close()
    return [r['data_reserva'] for r in rows]

def criar_reserva_intervalo(quiosque_id, usuario, data_inicio, data_fim, nome_cliente, forma_pagamento):
    import uuid
    conn = get_db()
    grupo_id = str(uuid.uuid4())[:8]
    d_ini  = date.fromisoformat(data_inicio)
    d_fim  = date.fromisoformat(data_fim)
    total  = (d_fim - d_ini).days + 1
    cur    = d_ini
    while cur <= d_fim:
        conn.execute(
            "INSERT INTO reservas (grupo_id,quiosque_id,usuario,data_reserva,data_inicio,data_fim,total_dias,nome_cliente,forma_pagamento) VALUES (?,?,?,?,?,?,?,?,?)",
            (grupo_id, quiosque_id, usuario, cur.isoformat(), data_inicio, data_fim, total, nome_cliente, forma_pagamento)
        )
        cur += timedelta(days=1)
    conn.commit()
    primeiro = conn.execute(
        "SELECT id FROM reservas WHERE grupo_id=? ORDER BY id LIMIT 1", (grupo_id,)
    ).fetchone()
    conn.close()
    return primeiro['id'], grupo_id, total

def buscar_reserva(reserva_id):
    conn = get_db()
    r = conn.execute('''
        SELECT r.*, q.nome AS quiosque_nome, q.preco_dia
        FROM reservas r JOIN quiosques q ON r.quiosque_id = q.id
        WHERE r.id=?
    ''', (reserva_id,)).fetchone()
    conn.close()
    return r

def listar_reservas_usuario(usuario):
    conn = get_db()
    lista = conn.execute('''
        SELECT r.grupo_id, r.quiosque_id, r.usuario, r.data_inicio, r.data_fim,
               r.total_dias, r.nome_cliente, r.forma_pagamento, r.status,
               MIN(r.id) AS id,
               q.nome AS quiosque_nome, q.preco_dia,
               (r.total_dias * q.preco_dia) AS total_valor
        FROM reservas r JOIN quiosques q ON r.quiosque_id = q.id
        WHERE r.usuario=? AND r.id = (
            SELECT MIN(r2.id) FROM reservas r2 WHERE r2.grupo_id = r.grupo_id
        )
        ORDER BY r.data_inicio DESC
    ''', (usuario,)).fetchall()
    conn.close()
    return lista

def cancelar_reserva_grupo(grupo_id, usuario):
    conn = get_db()
    conn.execute(
        "UPDATE reservas SET status='cancelada' WHERE grupo_id=? AND usuario=?",
        (grupo_id, usuario)
    )
    conn.commit()
    conn.close()

def listar_datas_reservadas(quiosque_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT data_reserva FROM reservas WHERE quiosque_id=? AND status='confirmada'",
        (quiosque_id,)
    ).fetchall()
    conn.close()
    return [r['data_reserva'] for r in rows]
