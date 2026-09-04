import { api } from './api.js';
import { RESOURCE_CONFIG } from './config.js';
import { renderDashboard } from './dashboard.js';
import { renderResource, tableRows, openForm, openDetails, confirmDelete } from './resources.js';
import { loading, showToast } from './ui.js';

const state = { view: document.body.dataset.view || 'dashboard', records: {} };
const view = document.querySelector('#view');

const solicitacoesLink = document.createElement('a');
solicitacoesLink.className = 'nav-link';
solicitacoesLink.href = 'solicitacoes.html';
solicitacoesLink.dataset.view = 'solicitacoes';
solicitacoesLink.innerHTML = '<span>☷</span> Solicitações';
document.querySelector('.menu').append(solicitacoesLink);

function setNav(key) { document.querySelectorAll('.nav-link').forEach(link => link.classList.toggle('active', link.dataset.view === key)); document.querySelector('#page-title').textContent = key === 'dashboard' ? 'Visão geral' : RESOURCE_CONFIG[key].title; document.querySelector('#breadcrumb').textContent = key === 'dashboard' ? 'PAINEL' : 'CADASTROS'; document.querySelector('#sidebar').classList.remove('open'); }
async function fetchAll() {
  const sources = Object.entries(RESOURCE_CONFIG);
  const results = await Promise.allSettled(sources.map(async ([key, config]) => [key, await api.list(config.endpoint)]));
  const failed = results.filter(result => result.status === 'rejected');
  results.forEach(result => { if (result.status === 'fulfilled') state.records[result.value[0]] = Array.isArray(result.value[1]) ? result.value[1] : []; });
  if (failed.length) showToast(`${failed.length} recurso(s) não puderam ser carregados. Verifique a API.`, 'error');
}
async function render(force = false) {
  view.innerHTML = loading();
  if (force || !Object.keys(state.records).length) await fetchAll();
  view.innerHTML = state.view === 'dashboard' ? renderDashboard(state.records) : renderResource(state.view, state.records);
}
async function reloadCurrent() { await render(true); }
function selectView(key) {
  const pages = { dashboard: 'index.html', usuarios: 'usuarios.html', enderecos: 'enderecos.html', secretarias: 'secretarias.html', servicos: 'servicos.html', funcionarios: 'funcionarios.html', solicitacoes: 'solicitacoes.html' };
  window.location.href = pages[key];
}

document.addEventListener('click', event => {
  const action = event.target.closest('[data-action]'); if (!action) return;
  const { action: name, resource, id } = action.dataset;
  if (name === 'go-resource') return selectView(resource);
  const record = (state.records[resource] || []).find(item => String(item.id) === id);
  if (name === 'create') openForm(resource, null, state.records, reloadCurrent);
  if (name === 'edit' && record) openForm(resource, record, state.records, reloadCurrent);
  if (name === 'view' && record) openDetails(resource, record, state.records);
  if (name === 'delete' && record) confirmDelete(resource, record, reloadCurrent);
});
document.addEventListener('input', event => { if (event.target.id !== 'table-search') return; const query = event.target.value.toLowerCase(); const records = (state.records[state.view] || []).filter(record => Object.values(record).join(' ').toLowerCase().includes(query)); document.querySelector('#resource-table-body').innerHTML = tableRows(state.view, records, state.records); });
document.querySelectorAll('.nav-link').forEach(link => link.addEventListener('click', event => { event.preventDefault(); selectView(link.dataset.view); }));
document.querySelector('#refresh-button')?.remove();
document.querySelector('.sidebar-footer')?.remove();
document.querySelector('#menu-toggle').addEventListener('click', () => document.querySelector('#sidebar').classList.toggle('open'));
setNav(state.view); render();
