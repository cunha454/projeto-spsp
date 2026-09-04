// Altere somente este valor se a API for publicada em outro endereço.
export const API_BASE_URL = 'http://127.0.0.1:8000';

export const RESOURCE_CONFIG = {
  usuarios: {
    title: 'Usuários', singular: 'usuário', endpoint: '/usuarios',
    fields: [
      { name: 'nome', label: 'Nome completo', type: 'text', required: true },
      { name: 'email', label: 'E-mail', type: 'email', required: true, maxlength: 75 },
      { name: 'telefone', label: 'Telefone', type: 'tel', required: true, mask: 'phone', hint: 'Formato: (00) 00000-0000' },
      { name: 'data_nascimento', label: 'Data de nascimento', type: 'date', required: true }
    ],
    columns: ['id', 'nome', 'email', 'telefone', 'data_nascimento'],
    itemEndpoint: '/usuarios'
  },
  enderecos: {
    title: 'Endereços', singular: 'endereço', endpoint: '/enderecos',
    fields: [
      { name: 'cep', label: 'CEP', type: 'text', required: true, mask: 'cep', pattern: '[0-9]{5}-[0-9]{3}', hint: 'Formato: 00000-000' },
      { name: 'estado', label: 'UF', type: 'text', required: true, maxlength: 2, pattern: '[A-Za-z]{2}', transform: 'uppercase' },
      { name: 'cidade', label: 'Cidade', type: 'text', required: true },
      { name: 'bairro', label: 'Bairro', type: 'text', required: true },
      { name: 'logradouro', label: 'Logradouro', type: 'text', required: true },
      { name: 'id_usuario', label: 'Usuário', type: 'number', required: true, relation: 'usuarios' }
    ],
    columns: ['id', 'cep', 'estado', 'cidade', 'bairro', 'logradouro', 'id_usuario']
  },
  secretarias: {
    title: 'Secretarias', singular: 'secretaria', endpoint: '/secretarias',
    fields: [{ name: 'nome', label: 'Nome', type: 'text', required: true }, { name: 'descricao', label: 'Descrição', type: 'textarea', required: false }],
    columns: ['id', 'nome', 'descricao']
  },
  servicos: {
    title: 'Serviços', singular: 'serviço', endpoint: '/servicos',
    fields: [{ name: 'nome', label: 'Nome', type: 'text', required: true }, { name: 'descricao', label: 'Descrição', type: 'textarea', required: false }, { name: 'id_secretaria', label: 'Secretaria', type: 'number', required: true, relation: 'secretarias' }],
    columns: ['id', 'nome', 'descricao', 'id_secretaria']
  },
  funcionarios: {
    title: 'Funcionários', singular: 'funcionário', endpoint: '/funcionarios',
    fields: [{ name: 'nome', label: 'Nome', type: 'text', required: true }, { name: 'cargo', label: 'Cargo', type: 'text', required: true }, { name: 'telefone', label: 'Telefone', type: 'tel', required: true, mask: 'phone', hint: 'Formato: (00) 00000-0000' }, { name: 'email', label: 'E-mail', type: 'email', required: true, maxlength: 75 }, { name: 'id_secretaria', label: 'Secretaria', type: 'number', required: true, relation: 'secretarias' }],
    columns: ['id', 'nome', 'cargo', 'telefone', 'email', 'id_secretaria']
  },
  solicitacoes: {
    title: 'Solicitações', singular: 'solicitação', endpoint: '/solicitacoes',
    fields: [
      { name: 'descricao', label: 'Descrição', type: 'textarea', required: true },
      { name: 'data_solicitacao', label: 'Data da solicitação', type: 'datetime-local', required: true },
      { name: 'status', label: 'Status', type: 'select', required: true, options: ['Pendente', 'Em análise', 'Em andamento', 'Concluída', 'Cancelada'] },
      { name: 'id_endereco', label: 'Endereço', type: 'number', required: true, relation: 'enderecos' },
      { name: 'id_servico', label: 'Serviço', type: 'number', required: true, relation: 'servicos' },
      { name: 'id_funcionario', label: 'Funcionário', type: 'number', required: true, relation: 'funcionarios' }
    ],
    columns: ['id', 'descricao', 'data_solicitacao', 'status', 'id_endereco', 'id_servico', 'id_funcionario']
  }
};
