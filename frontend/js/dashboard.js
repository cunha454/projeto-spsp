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
  return `<section class="dashboard">
    <article class="panel dashboard-chart"><div class="panel-heading"><div><h3>Solicitações ativas por secretaria</h3><p>Status considerados: ativo, pendente, em análise e em andamento.</p></div><span class="total-badge">${total} ativas</span></div>${pieChart(porSecretaria)}</article>
  </section>`;
}
