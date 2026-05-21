document.addEventListener("DOMContentLoaded", () => {
  const runButton = document.getElementById("run-button");
  const csvFileInput = document.getElementById("csv-file");
  const matrixInput = document.getElementById("matrix-input");
  const kInput = document.getElementById("k-input");
  let currentMatrix = null;

  csvFileInput.addEventListener("change", async (event) => {
    const file = event.target.files[0];
    if (!file) {
      return;
    }
    const text = await file.text();
    matrixInput.value = text.trim();
    displayInitialGraph();
  });

  matrixInput.addEventListener("change", () => {
    displayInitialGraph();
  });

  matrixInput.addEventListener("blur", () => {
    displayInitialGraph();
  });

  matrixInput.addEventListener("input", () => {
    displayInitialGraph();
  });

  function displayInitialGraph() {
    console.log("displayInitialGraph called");
    const matrixText = matrixInput.value.trim();
    if (!matrixText) {
      console.log("Matrix text is empty");
      document.getElementById("graph-initial-card").style.display = "none";
      return;
    }
    const matrix = matrixText
      .split(/\r?\n/)
      .map((line) => line.split(",").map((cell) => parseFloat(cell.trim())));
    console.log("Parsed matrix:", matrix);
    currentMatrix = matrix;
    renderInitialGraph(matrix);
  }

  runButton.addEventListener("click", async () => {
    const matrixText = matrixInput.value.trim();
    const k = parseInt(kInput.value, 10);
    if (!matrixText) {
      alert("Ingresa la matriz de dependencias o carga un CSV.");
      return;
    }

    const matrix = matrixText
      .split(/\r?\n/)
      .map((line) => line.split(",").map((cell) => parseFloat(cell.trim())));
    currentMatrix = matrix;
    const payload = {
      matrix,
      k,
    };

    const result = await callPartitionApi(payload);
    if (result.error || result.status === "error") {
      const message = result.error || result.message || "Ocurrió un error en el servidor.";
      document.getElementById("results").innerHTML = `<p class="error">Error: ${message}</p>`;
      return;
    }
    renderResult(result);
    if (result.partitions && currentMatrix) {
      const assignment = [];
      Object.entries(result.partitions).forEach(([group, nodes]) => {
        nodes.forEach((node) => {
          const idx = parseInt(node.split("_")[1]);
          assignment[idx] = parseInt(group);
        });
      });
      renderPartitionedGraph(currentMatrix, assignment, result.k);
    }
  });
});
