from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import datetime
from models import (
    buscar_usuario, listar_quiosques, buscar_quiosque,
    verificar_disponibilidade, verificar_intervalo,
    criar_reserva_intervalo, buscar_reserva,
    listar_reservas_usuario, cancelar_reserva_grupo,
    listar_datas_reservadas
)

bp = Blueprint('main', __name__)

# ── AUTH ──────────────────────────────────────────────────
@bp.route('/')
def index():
    return redirect(url_for('main.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario' in session:
        return redirect(url_for('main.quiosques'))
    if request.method == 'POST':
        login_val = request.form.get('login', '').strip()
        senha_val = request.form.get('senha', '').strip()
        user = buscar_usuario(login_val, senha_val)
        if user:
            session['usuario'] = login_val
            return redirect(url_for('main.quiosques'))
        flash('Login ou senha incorretos!', 'error')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('main.login'))

# ── QUIOSQUES ─────────────────────────────────────────────
@bp.route('/quiosques')
def quiosques():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))
    return render_template('quiosques.html', quiosques=listar_quiosques())

# ── DISPONIBILIDADE (AJAX) ────────────────────────────────
@bp.route('/disponibilidade', methods=['POST'])
def disponibilidade():
    if 'usuario' not in session:
        return jsonify({'erro': 'Nao autorizado'}), 401
    data = request.json
    disponivel = verificar_disponibilidade(data['quiosque_id'], data['data'])
    return jsonify({'disponivel': disponivel})

@bp.route('/verificar-intervalo', methods=['POST'])
def checar_intervalo():
    if 'usuario' not in session:
        return jsonify({'erro': 'Nao autorizado'}), 401
    data = request.json
    bloqueadas = verificar_intervalo(data['quiosque_id'], data['data_inicio'], data['data_fim'])
    return jsonify({'disponivel': len(bloqueadas) == 0, 'bloqueadas': bloqueadas})

@bp.route('/datas-reservadas/<int:quiosque_id>')
def datas_reservadas(quiosque_id):
    if 'usuario' not in session:
        return jsonify({'erro': 'Nao autorizado'}), 401
    return jsonify({'datas': listar_datas_reservadas(quiosque_id)})

# ── RESERVA ───────────────────────────────────────────────
@bp.route('/reserva/<int:quiosque_id>', methods=['GET', 'POST'])
def reserva(quiosque_id):
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    quiosque = buscar_quiosque(quiosque_id)
    if not quiosque:
        flash('Quiosque não encontrado.', 'error')
        return redirect(url_for('main.quiosques'))

    if request.method == 'POST':
        nome_cliente    = request.form.get('nome_cliente', '').strip()
        data_inicio     = request.form.get('data_inicio', '').strip()
        data_fim        = request.form.get('data_fim', '').strip()
        forma_pagamento = request.form.get('forma_pagamento', '').strip()

        # Verificar intervalo completo
        bloqueadas = verificar_intervalo(quiosque_id, data_inicio, data_fim)
        if bloqueadas:
            flash(f'As seguintes datas já estão reservadas: {", ".join(bloqueadas)}', 'error')
            return redirect(url_for('main.reserva', quiosque_id=quiosque_id))

        reserva_id, grupo_id, total_dias = criar_reserva_intervalo(
            quiosque_id, session['usuario'],
            data_inicio, data_fim, nome_cliente, forma_pagamento
        )
        return redirect(url_for('main.confirmacao', reserva_id=reserva_id))

    hoje = datetime.now().strftime('%Y-%m-%d')
    return render_template('reserva.html', quiosque=quiosque, hoje=hoje)

# ── CONFIRMAÇÃO ───────────────────────────────────────────
@bp.route('/confirmacao/<int:reserva_id>')
def confirmacao(reserva_id):
    if 'usuario' not in session:
        return redirect(url_for('main.login'))
    r = buscar_reserva(reserva_id)
    if not r:
        flash('Reserva não encontrada.', 'error')
        return redirect(url_for('main.quiosques'))
    return render_template('confirmacao.html', reserva=r)

# ── MINHAS RESERVAS ───────────────────────────────────────
@bp.route('/minhas-reservas')
def minhas_reservas():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))
    return render_template('minhas_reservas.html', reservas=listar_reservas_usuario(session['usuario']))

@bp.route('/cancelar/<grupo_id>', methods=['POST'])
def cancelar(grupo_id):
    if 'usuario' not in session:
        return redirect(url_for('main.login'))
    cancelar_reserva_grupo(grupo_id, session['usuario'])
    flash('Reserva cancelada com sucesso.', 'success')
    return redirect(url_for('main.minhas_reservas'))
