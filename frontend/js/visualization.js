function renderResult(result) {
  const container = document.getElementById("results");
  const parts = result.partitions.map((group, index) => `<div class=\"result-section\"><strong>Grupo ${index}</strong>: ${group.join(", ")}</div>`).join("");
  const cutEdges = result.cut_edges
    .map((edge) => `<li>${edge.source} → ${edge.target} (peso ${edge.weight})</li>`)
    .join("");

  container.innerHTML = `
    <div class=\"result-section\"><strong>Valor de corte:</strong> ${result.cut_value}</div>
    <div class=\"result-section\"><strong>Solución:</strong> ${result.optimal ? "Óptima" : "Aproximada"}</div>
    <div class=\"result-section\"><strong>Tiempo de ejecución:</strong> ${result.execution_time_seconds}s</div>
    ${parts}
    <div class=\"result-section\"><strong>Aristas cortadas:</strong><ul>${cutEdges}</ul></div>
    <pre>${JSON.stringify(result, null, 2)}</pre>
  `;
}
