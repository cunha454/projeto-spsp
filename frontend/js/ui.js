export function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' })[character]); }
export function humanize(value) { return ({ id: 'ID', cep: 'CEP', estado: 'UF', id_usuario: 'Usuário', id_secretaria: 'Secretaria', data_nascimento: 'Nascimento' })[value] || value.replaceAll('_', ' ').replace(/\b\w/g, letter => letter.toUpperCase()); }

export function showToast(message, type = 'success') {
  const toast = document.createElement('div'); toast.className = `toast ${type}`; toast.innerHTML = `<span>${type === 'success' ? '✓' : '!'}</span><p>${escapeHtml(message)}</p><button aria-label="Fechar">×</button>`;
  document.querySelector('#toast-area').append(toast); toast.querySelector('button').onclick = () => toast.remove(); setTimeout(() => toast.remove(), 5500);
}

export function showModal(title, content) {
  document.querySelector('#modal-root').innerHTML = `<div class="modal-backdrop"><section class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title"><header><h2 id="modal-title">${escapeHtml(title)}</h2><button data-modal-close aria-label="Fechar">×</button></header><div class="modal-content">${content}</div></section></div>`;
  const close = () => { document.querySelector('#modal-root').innerHTML = ''; };
  document.querySelectorAll('[data-modal-close]').forEach(button => button.onclick = close);
  document.querySelector('.modal-backdrop').addEventListener('click', event => { if (event.target === event.currentTarget) close(); });
}

export function loading(label = 'Carregando dados…') { return `<div class="loading"><i></i><span>${label}</span></div>`; }
