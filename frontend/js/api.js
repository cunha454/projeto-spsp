import { API_BASE_URL } from './config.js';

function messageFrom(body, fallback) {
  if (typeof body?.detail === 'string') return body.detail;
  if (Array.isArray(body?.detail)) return body.detail.map(item => item.msg).join('; ');
  return fallback;
}

export async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: { Accept: 'application/json', ...(options.body ? { 'Content-Type': 'application/json' } : {}), ...options.headers },
      ...options
    });
  } catch {
    throw new Error(`Não foi possível conectar à API em ${API_BASE_URL}. Confirme se ela está em execução.`);
  }
  const text = await response.text();
  let body = null;
  try { body = text ? JSON.parse(text) : null; } catch { body = text; }
  if (!response.ok) throw new Error(messageFrom(body, `Erro ${response.status} ao comunicar com a API.`));
  return body;
}

export const api = {
  list: path => request(path),
  get: path => request(path),
  create: (path, data) => request(path, { method: 'POST', body: JSON.stringify(data) }),
  update: (path, data) => request(path, { method: 'PUT', body: JSON.stringify(data) }),
  remove: path => request(path, { method: 'DELETE' })
};
