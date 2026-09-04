const colorSet = ['#7447df', '#a88cf5', '#d2c5fb', '#4d2a9b', '#edb9ff'];

function pieChart(items) {
  const total = items.reduce((sum, item) => sum + item.value, 0);
  if (!total) return '<div class="empty-chart">Sem solicitações ativas para exibir.</div>';
  let current = 0;
  const slices = items.map((item, index) => {
    const start = current;
    current += item.value / total * 100;
    return `${colorSet[index % colorSet.length]} ${start}% ${current}%`;
  });
  return `<div class="donut-wrap"><div class="donut" aria-label="Gráfico de pizza" style="background:conic-gradient(${slices.join(',')})"><span><b>${total}</b>ativas</span></div><div class="legend">${items.map((item, index) => `<span><i style="background:${colorSet[index % colorSet.length]}"></i>${item.label}<b>${item.value}</b></span>`).join('')}</div></div>`;
}

function verticalBarChart(items) {
  const maximum = Math.max(...items.map(item => item.value), 0);
  if (!maximum) return '<div class="empty-chart">Sem funcionários cadastrados para exibir.</div>';
  return `<div class="vertical-chart" role="img" aria-label="Quantidade de funcionários por secretaria">${items.map((item, index) => {
    const height = Math.max((item.value / maximum) * 100, 3);
    return `<div class="vertical-bar-item"><span class="vertical-bar-value">${item.value}</span><div class="vertical-bar-track"><i style="height:${height}%;background:${colorSet[index % colorSet.length]}"></i></div><span class="vertical-bar-label" title="${item.label}">${item.label}</span></div>`;
  }).join('')}</div>`;
}

function metric(label, value, detail) {
  return `<article class="metric-card"><div><small>${label}</small><strong>${value}</strong><em>${detail}</em></div></article>`;
}

function serviceChart(items) {
  const maximum = Math.max(...items.map(item => item.value), 0);
  if (!maximum) return '<div class="empty-chart">Sem solicitações para exibir.</div>';
  return `<div class="bar-chart">${items.slice(0, 5).map((item, index) => `<div class="bar-row"><span title="${item.label}">${item.label}</span><div class="bar-track"><i style="width:${item.value / maximum * 100}%;background:${colorSet[index % colorSet.length]}"></i></div><b>${item.value}</b></div>`).join('')}</div>`;
}

export function renderDashboard(records) {
  const secretarias = records.secretarias || [];
  const funcionarios = records.funcionarios || [];
  const ativos = new Set(['ativo', 'pendente', 'em análise', 'em analise', 'em andamento']);
  const solicitacoesAtivas = (records.solicitacoes || []).filter(solicitacao => ativos.has(String(solicitacao.status || '').trim().toLowerCase()));
  const porSecretaria = secretarias.map(secretaria => ({
    label: secretaria.nome,
    value: solicitacoesAtivas.filter(solicitacao => funcionarios.some(funcionario => Number(funcionario.id) === Number(solicitacao.id_funcionario) && Number(funcionario.id_secretaria) === Number(secretaria.id))).length
  }));
  const total = porSecretaria.reduce((sum, item) => sum + item.value, 0);
  const funcionariosPorSecretaria = secretarias.map(secretaria => ({
    label: secretaria.nome,
    value: funcionarios.filter(funcionario => Number(funcionario.id_secretaria) === Number(secretaria.id)).length
  }));
  const totalFuncionarios = funcionariosPorSecretaria.reduce((sum, item) => sum + item.value, 0);
  const solicitacoes = records.solicitacoes || [];
  const statusCount = status => solicitacoes.filter(item => String(item.status).trim().toLowerCase() === status).length;
  const pendentes = statusCount('pendente');
  const concluidas = statusCount('concluída');
  const canceladas = statusCount('cancelada');
  const servicosMaisSolicitados = (records.servicos || []).map(servico => ({ label: servico.nome, value: solicitacoes.filter(item => Number(item.id_servico) === Number(servico.id)).length })).filter(item => item.value).sort((a, b) => b.value - a.value || a.label.localeCompare(b.label, 'pt-BR'));
  return `<section class="dashboard">
    <div class="metric-grid">
      ${metric('Solicitações pendentes', pendentes, 'Aguardando atendimento')}
      ${metric('Solicitações concluídas', concluidas, 'Atendimentos finalizados')}
      ${metric('Solicitações canceladas', canceladas, 'Registros cancelados')}
      ${metric('Serviço mais solicitado', servicosMaisSolicitados[0]?.label || '—', `${servicosMaisSolicitados[0]?.value || 0} solicitações`)}</div>
    <div class="dashboard-grid">
      <article class="panel dashboard-chart"><div class="panel-heading"><div><h3>Solicitações ativas por secretaria</h3><p>Status considerados: ativo, pendente, em análise e em andamento.</p></div><span class="total-badge">${total} ativas</span></div>${pieChart(porSecretaria)}</article>
      <article class="panel dashboard-chart"><div class="panel-heading"><div><h3>Funcionários por secretaria</h3><p>Distribuição atual da equipe municipal.</p></div><span class="total-badge">${totalFuncionarios} funcionários</span></div>${verticalBarChart(funcionariosPorSecretaria)}</article>
      <article class="panel wide"><div class="panel-heading"><div><h3>Serviços mais solicitados</h3><p>Os cinco serviços com mais registros.</p></div><span class="total-badge">${solicitacoes.length} solicitações</span></div>${serviceChart(servicosMaisSolicitados)}</article>
    </div>
  </section>`;
}
