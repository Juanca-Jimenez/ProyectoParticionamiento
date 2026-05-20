function renderResult(result) {
  const container = document.getElementById("results");
  const partitions = result.partitions || {};
  const groups = Object.entries(partitions)
    .sort(([a], [b]) => Number(a) - Number(b))
    .map(([group, nodes]) => {
      const count = nodes.length;
      return `
        <div class="result-section group-block">
          <div class="group-title">Grupo ${group} (${count} componente${count === 1 ? "" : "s"})</div>
          <div>${nodes.join(", ")}</div>
        </div>
      `;
    })
    .join("");

  const cutEdges = result.cut_edges || [];
  const cutEdgesHtml = cutEdges.length > 0
    ? cutEdges
        .map(
          (edge) =>
            `<li>${edge.from || edge.source} → ${edge.to || edge.target} (peso ${edge.weight})<br/><small>${edge.reason || "Se cortó porque los componentes quedan en grupos distintos."}</small></li>`
        )
        .join("")
    : "<li>No hay aristas cortadas.</li>";

  const explanation = result.explanation || {};
  const explanationHtml = [
    { title: "Por qué se eligió esta solución", text: explanation.solution_selection },
    { title: "Clasificación", text: explanation.classification },
    { title: "Por qué se usó este algoritmo", text: explanation.algorithm_reason },
    { title: "Por qué se cortan las aristas", text: explanation.cut_reason },
    { title: "Por qué se separan así los componentes", text: explanation.group_reason },
  ]
    .filter((item) => item.text)
    .map((item) => `<div class="result-section"><strong>${item.title}:</strong> ${item.text}</div>`)
    .join("");

  const componentReasons = (explanation.component_reasons || [])
    .map(
      (entry) =>
        `<div class="result-section"><strong>${entry.component} (Grupo ${entry.group}):</strong> ${entry.reason} <br/><small>Peso interno: ${entry.same_group_weight.toFixed(2)}, peso externo: ${entry.cross_group_weight.toFixed(2)}</small></div>`
    )
    .join("");

  const executionTime = result.execution_time_ms != null
    ? `${result.execution_time_ms.toFixed(4)} ms`
    : "N/A";

  const memoryUsage = result.memory_peak_kb != null
    ? `${result.memory_peak_kb} KB`
    : "N/A";

  const validAssignment = result.valid_assignment === true ? "Sí" : "No";
  const solutionType = result.optimal ? "Óptima" : "Aproximada";
  const algorithmType = result.algorithm_used || "No disponible";

  container.innerHTML = `
    <div class="result-summary">
      <div class="result-section"><strong>n:</strong> ${result.n}</div>
      <div class="result-section"><strong>k:</strong> ${result.k}</div>
      <div class="result-section"><strong>Algoritmo:</strong> ${algorithmType}</div>
      <div class="result-section"><strong>Tipo de solución:</strong> ${solutionType}</div>
      <div class="result-section"><strong>Valor de corte:</strong> ${result.cut_value}</div>
      <div class="result-section"><strong>Asignaciones totales:</strong> ${result.assignment_count}</div>
      <div class="result-section"><strong>Asignación válida:</strong> ${validAssignment}</div>
      <div class="result-section"><strong>Tiempo de ejecución:</strong> ${executionTime}</div>
      <div class="result-section"><strong>Memoria pico:</strong> ${memoryUsage}</div>
    </div>
    <div class="result-section"><strong>Particiones:</strong></div>
    ${groups}
    <div class="result-section"><strong>Explicación general:</strong></div>
    ${explanationHtml}
    <div class="result-section"><strong>Razón por componente:</strong></div>
    ${componentReasons}
    <div class="result-section"><strong>Aristas cortadas:</strong><ul>${cutEdgesHtml}</ul></div>
  `;
}
