// ── PAGAMENTO ─────────────────────────────────────────────
document.querySelectorAll('.pag-item').forEach(item => {
  item.addEventListener('click', () => {
    document.querySelectorAll('.pag-item').forEach(i => i.classList.remove('on'));
    item.classList.add('on');
    item.querySelector('input').checked = true;
  });
});

// ── DISPONIBILIDADE ───────────────────────────────────────
const dataInput = document.getElementById('data_reserva');
const dispMsg   = document.getElementById('disp-msg');
const btnReserv = document.getElementById('btn-reservar');

if (dataInput) {
  dataInput.addEventListener('change', async () => {
    const data        = dataInput.value;
    const quiosqueId  = dataInput.dataset.id;
    if (!data) return;

    dispMsg.className = 'disp-msg';
    dispMsg.textContent = '⏳ Verificando disponibilidade...';
    dispMsg.style.display = 'block';

    try {
      const res  = await fetch('/disponibilidade', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ quiosque_id: Number(quiosqueId), data })
      });
      const json = await res.json();

      if (json.disponivel) {
        dispMsg.className   = 'disp-msg disp-ok';
        dispMsg.textContent = '✅ Disponível para esta data!';
        if (btnReserv) { btnReserv.disabled = false; btnReserv.style.opacity = '1'; }
      } else {
        dispMsg.className   = 'disp-msg disp-err';
        dispMsg.textContent = '❌ Quiosque já reservado para este dia.';
        if (btnReserv) { btnReserv.disabled = true; btnReserv.style.opacity = '.45'; }
      }
    } catch {
      dispMsg.className   = 'disp-msg disp-err';
      dispMsg.textContent = '⚠️ Erro ao verificar. Tente novamente.';
    }
  });
}
