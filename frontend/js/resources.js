import { api } from './api.js';
import { RESOURCE_CONFIG } from './config.js';
import { showModal, showToast, escapeHtml, humanize } from './ui.js';

function value(record, field, records) {
  const raw = record[field];
  if (field === 'telefone' && raw) return formatMaskedValue('phone', raw);
  if (field === 'cep' && raw) return formatMaskedValue('cep', raw);
  if (field.startsWith('id_')) {
    const relation = { id_secretaria: 'secretarias', id_usuario: 'usuarios', id_endereco: 'enderecos', id_servico: 'servicos', id_funcionario: 'funcionarios' }[field];
    const related = (records[relation] || []).find(row => Number(row.id) === Number(raw));
    if (!related) return `#${raw ?? '—'}`;
    const label = field === 'id_endereco' ? `${related.logradouro}, ${related.cidade}` : related.nome;
    return `${label} (#${raw})`;
  }
  if (raw && field.includes('data_')) {
    const date = new Date(String(raw).includes('T') ? raw : `${raw}T00:00:00`);
    return Number.isNaN(date.getTime()) ? raw : new Intl.DateTimeFormat('pt-BR', { timeZone: 'UTC' }).format(date);
  }
  return raw ?? '—';
}

function relationLabel(relation, related, records) {
  if (relation === 'usuarios') return related.email ? `${related.nome} (${related.email})` : related.nome;
  if (relation === 'enderecos') return [related.logradouro, related.bairro, related.cidade].filter(Boolean).join(', ');
  if (relation === 'funcionarios') {
    const secretaria = (records.secretarias || []).find(item => Number(item.id) === Number(related.id_secretaria));
    return [related.nome, related.cargo, secretaria?.nome].filter(Boolean).join(' — ');
  }
  return related.nome;
}

function formatMaskedValue(mask, value) {
  const digits = String(value || '').replace(/\D/g, '');
  if (mask === 'cep') return digits.length > 5 ? `${digits.slice(0, 5)}-${digits.slice(5, 8)}` : digits.slice(0, 5);
  if (mask === 'phone') {
    const number = digits.slice(0, 11);
    if (number.length < 3) return number.length ? `(${number}` : '';
    if (number.length < 7) return `(${number.slice(0, 2)}) ${number.slice(2)}`;
    const prefixLength = number.length > 10 ? 7 : 6;
    return `(${number.slice(0, 2)}) ${number.slice(2, prefixLength)}-${number.slice(prefixLength)}`;
  }
  return value;
}

function validateField(field, input) {
  if (!input) return true;
  const value = input.value.trim();
  let message = '';
  if (field.type === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) message = 'Informe um e-mail válido.';
  if (field.mask === 'phone' && value && !/^\(\d{2}\) \d{4,5}-\d{4}$/.test(value)) message = 'Informe um telefone com DDD válido.';
  if (field.mask === 'cep' && value && !/^\d{5}-\d{3}$/.test(value)) message = 'Informe um CEP válido no formato 00000-000.';
  if (field.name === 'data_nascimento' && value && new Date(`${value}T00:00:00`) > new Date()) message = 'A data de nascimento não pode estar no futuro.';
  if (field.name === 'data_solicitacao' && value) {
    const today = new Date();
    const currentDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
    if (value.slice(0, 10) > currentDate) message = 'A data da solicitação não pode ser posterior a hoje.';
  }
  input.setCustomValidity(message);
  return !message;
}

function formField(field, record, records = {}) {
  const currentRecord = record || {};
  if (field.createOnly && currentRecord.id !== undefined) return '';
  const currentValue = field.mask ? formatMaskedValue(field.mask, currentRecord[field.name]) : (currentRecord[field.name] ?? '');
  const relatedRecords = field.relation ? (records[field.relation] || []) : [];
  const emptyRelation = field.relation && !relatedRecords.length;
  let input;
  if (field.relation) {
    const options = relatedRecords.map(related => ({ id: related.id, label: relationLabel(field.relation, related, records) })).sort((a, b) => a.label.localeCompare(b.label, 'pt-BR', { sensitivity: 'base' })).map(related => `<option value="${related.id}" ${Number(currentValue) === Number(related.id) ? 'selected' : ''}>${escapeHtml(related.label)}</option>`).join('');
    input = `<select name="${field.name}" ${field.required ? 'required' : ''} ${emptyRelation ? 'disabled' : ''}><option value="">${emptyRelation ? `Nenhum registro de ${field.label.toLowerCase()} cadastrado` : `Selecione ${field.label.toLowerCase()}`}</option>${options}</select>`;
  } else if (field.type === 'select') {
    const options = (field.options || []).slice().sort((a, b) => a.localeCompare(b, 'pt-BR', { sensitivity: 'base' })).map(option => `<option value="${escapeHtml(option)}" ${currentValue === option ? 'selected' : ''}>${escapeHtml(option)}</option>`).join('');
    input = `<select name="${field.name}" ${field.required ? 'required' : ''}><option value="">Selecione ${field.label.toLowerCase()}</option>${options}</select>`;
  } else input = field.type === 'textarea'
    ? `<textarea name="${field.name}" ${field.required ? 'required' : ''} placeholder="Informe ${field.label.toLowerCase()}">${escapeHtml(currentRecord[field.name] ?? '')}</textarea>`
    : `<input name="${field.name}" type="${field.type}" value="${escapeHtml(field.type === 'datetime-local' && currentRecord[field.name] ? String(currentRecord[field.name]).slice(0, 16) : currentValue)}" ${field.required ? 'required' : ''} ${field.pattern ? `pattern="${field.pattern}"` : ''} ${field.maxlength ? `maxlength="${field.maxlength}"` : ''} ${field.mask ? `data-mask="${field.mask}" inputmode="numeric"` : ''} placeholder="Informe ${field.label.toLowerCase()}" />`;
  const relationHint = emptyRelation ? `Cadastre um registro de ${field.label.toLowerCase()} antes de continuar.` : '';
  return `<label class="form-field"><span>${field.label}${field.required ? ' <b>*</b>' : ''}</span>${input}${field.hint ? `<small>${field.hint}</small>` : ''}${relationHint ? `<small>${relationHint}</small>` : ''}</label>`;
}

export function renderResource(key, records) {
  const config = RESOURCE_CONFIG[key];
  const items = records[key] || [];
  return `<section class="resource-view"><div class="resource-header"><div><p class="eyebrow">CADASTROS</p><h2>${config.title}</h2><p>Gerencie os registros de ${config.title.toLowerCase()}.</p></div><button class="primary-button" data-action="create" data-resource="${key}">+ Cadastrar ${config.singular}</button></div>
  <article class="panel table-panel"><div class="table-toolbar"><span><b>${items.length}</b> ${items.length === 1 ? 'registro' : 'registros'}</span><label class="search-field">⌕ <input id="table-search" type="search" placeholder="Buscar nos registros" /></label></div>
  <div class="table-wrap"><table><thead><tr>${config.columns.map(column => `<th>${humanize(column)}</th>`).join('')}<th class="actions-head">Ações</th></tr></thead><tbody id="resource-table-body">${tableRows(key, items, records)}</tbody></table></div></article></section>`;
}

export function tableRows(key, items, records) {
  const config = RESOURCE_CONFIG[key];
  if (!items.length) return `<tr><td colspan="${config.columns.length + 1}" class="empty-state">Nenhum registro encontrado.</td></tr>`;
  return items.map(item => `<tr>${config.columns.map(column => `<td>${escapeHtml(String(value(item, column, records)))}</td>`).join('')}<td class="actions"><button title="Visualizar" data-action="view" data-resource="${key}" data-id="${item.id}">◉</button><button title="Editar" data-action="edit" data-resource="${key}" data-id="${item.id}">✎</button><button title="Excluir" class="danger" data-action="delete" data-resource="${key}" data-id="${item.id}">⌫</button></td></tr>`).join('');
}

export function openForm(key, record, records, onSaved) {
  const config = RESOURCE_CONFIG[key]; const editing = Boolean(record);
  const missingRelation = config.fields.some(field => field.relation && !(records[field.relation] || []).length);
  showModal(`${editing ? 'Editar' : 'Cadastrar'} ${config.singular}`, `<form id="record-form" class="record-form"><div class="form-grid">${config.fields.map(field => formField(field, record, records)).join('')}</div><div class="modal-actions"><button type="button" class="secondary-button" data-modal-close>Cancelar</button><button class="primary-button" type="submit" ${missingRelation ? 'disabled title="Cadastre os registros relacionados antes de continuar"' : ''}>${editing ? 'Salvar alterações' : 'Cadastrar'}</button></div></form>`);
  const form = document.querySelector('#record-form');
  form.querySelectorAll('[data-mask]').forEach(input => input.addEventListener('input', () => { input.value = formatMaskedValue(input.dataset.mask, input.value); input.setCustomValidity(''); }));
  form.querySelectorAll('input, select, textarea').forEach(input => input.addEventListener('input', () => { const field = config.fields.find(item => item.name === input.name); validateField(field, input); }));
  form.addEventListener('submit', async event => {
    event.preventDefault(); const form = event.currentTarget;
    config.fields.forEach(field => validateField(field, form.elements.namedItem(field.name)));
    if (!form.reportValidity()) return;
    const data = Object.fromEntries(new FormData(form));
    config.fields.forEach(field => { if ((field.type === 'number' || field.relation) && data[field.name] !== undefined) data[field.name] = Number(data[field.name]); if (field.transform === 'uppercase' && data[field.name]) data[field.name] = data[field.name].toUpperCase(); });
    const button = form.querySelector('[type="submit"]'); button.disabled = true; button.textContent = 'Salvando…';
    try { await (editing ? api.update(`${config.endpoint}/${record.id}`, data) : api.create(config.endpoint, data)); showToast(`${config.singular[0].toUpperCase() + config.singular.slice(1)} ${editing ? 'atualizado' : 'cadastrado'} com sucesso.`, 'success'); document.querySelector('[data-modal-close]').click(); onSaved(); }
    catch (error) { showToast(error.message, 'error'); button.disabled = false; button.textContent = editing ? 'Salvar alterações' : 'Cadastrar'; }
  });
}

export async function openDetails(key, record, records) {
  const config = RESOURCE_CONFIG[key]; let data = record;
  if (config.itemEndpoint !== null) { try { data = await api.get(`${config.endpoint}/${record.id}`); } catch (error) { showToast(error.message, 'error'); return; } }
  showModal(`${config.singular[0].toUpperCase() + config.singular.slice(1)} #${record.id}`, `<dl class="details-list">${config.columns.map(field => `<div><dt>${humanize(field)}</dt><dd>${escapeHtml(String(value(data, field, records)))}</dd></div>`).join('')}</dl><div class="modal-actions"><button class="secondary-button" data-modal-close>Fechar</button></div>`);
}

export function confirmDelete(key, record, onDeleted) {
  const config = RESOURCE_CONFIG[key];
  showModal('Confirmar exclusão', `<div class="confirm-content"><span class="warning-icon">!</span><p>Deseja realmente excluir este(a) ${config.singular}?</p><small>Esta ação não pode ser desfeita.</small><div class="modal-actions"><button class="secondary-button" data-modal-close>Cancelar</button><button class="danger-button" id="confirm-delete">Excluir registro</button></div></div>`);
  document.querySelector('#confirm-delete').addEventListener('click', async event => { event.currentTarget.disabled = true; try { const path = config.deletePath ? config.deletePath(record.id) : `${config.endpoint}/${record.id}`; await api.remove(path); showToast('Registro excluído com sucesso.', 'success'); document.querySelector('[data-modal-close]').click(); onDeleted(); } catch (error) { showToast(error.message, 'error'); event.currentTarget.disabled = false; } });
}
