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
  return `<section class="dashboard">
    <div class="dashboard-grid">
      <article class="panel dashboard-chart"><div class="panel-heading"><div><h3>Solicitações ativas por secretaria</h3><p>Status considerados: ativo, pendente, em análise e em andamento.</p></div><span class="total-badge">${total} ativas</span></div>${pieChart(porSecretaria)}</article>
      <article class="panel dashboard-chart"><div class="panel-heading"><div><h3>Funcionários por secretaria</h3><p>Distribuição atual da equipe municipal.</p></div><span class="total-badge">${totalFuncionarios} funcionários</span></div>${verticalBarChart(funcionariosPorSecretaria)}</article>
    </div>
  </section>`;
}
