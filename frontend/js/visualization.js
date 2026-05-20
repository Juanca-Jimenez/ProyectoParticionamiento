function renderResult(result) {
  const container = document.getElementById("results");
  const partitions = result.partitions || {};
  const parts = Object.entries(partitions)
    .map(([group, nodes]) => `<div class="result-section"><strong>Grupo ${group}</strong>: ${nodes.join(", ")}</div>`)
    .join("");
  const cutEdges = (result.cut_edges || [])
    .map((edge) => `<li>${edge.source || edge.from} → ${edge.target || edge.to} (peso ${edge.weight})</li>`)
    .join("");
  const executionTime = result.execution_time_seconds != null
    ? `${result.execution_time_seconds}s`
    : result.execution_time_ms != null
      ? `${result.execution_time_ms}ms`
      : "N/A";

  container.innerHTML = `
    <div class="result-section"><strong>Valor de corte:</strong> ${result.cut_value}</div>
    <div class="result-section"><strong>Solución:</strong> ${result.optimal ? "Óptima" : "Aproximada"}</div>
    <div class="result-section"><strong>Tiempo de ejecución:</strong> ${executionTime}</div>
    ${parts}
    <div class="result-section"><strong>Aristas cortadas:</strong><ul>${cutEdges}</ul></div>
    <pre>${JSON.stringify(result, null, 2)}</pre>
  `;
}
