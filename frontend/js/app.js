document.addEventListener("DOMContentLoaded", () => {
  const runButton = document.getElementById("run-button");
  const csvFileInput = document.getElementById("csv-file");
  const matrixInput = document.getElementById("matrix-input");
  const kInput = document.getElementById("k-input");
  const defaultSelect = document.getElementById("default-matrix-select");
  const useDefaultButton = document.getElementById("use-default-button");
  let currentMatrix = null;

  // Fill selector description (no heavy DOM changes)
  defaultSelect.addEventListener("change", () => {
    // nothing for now; user must click 'Usar matriz predeterminada'
  });

  useDefaultButton.addEventListener("click", (e) => {
    e.preventDefault();
    const sel = defaultSelect.value;
    if (!sel) {
      alert("Selecciona una matriz predeterminada primero.");
      return;
    }

    const newMatrix = getDynamicDefaultMatrix(sel);
    const csv = matrixToCsv(newMatrix);
    matrixInput.value = csv;
    displayInitialGraph();
    });

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

  // Utility: convert matrix (array of arrays) to CSV string
  function matrixToCsv(matrix) {
    return matrix.map((row) => row.join(",")).join("\n");
  }

  // Deterministic pseudo-random generator (LCG)
  function lcg(seed) {
    let state = seed % 2147483647;
    if (state <= 0) state += 2147483646;
    return function () {
      state = (state * 16807) % 2147483647;
      return (state - 1) / 2147483646;
    };
  }

  function generateSymmetricMatrix(n, density = 0.5, maxWeight = 10,seed = null) {
    const finalSeed = seed !== null ? seed : Date.now() + Math.random() * 1000000;
    const rand = lcg(finalSeed);
    const mat = Array.from({ length: n }, () => Array(n).fill(0));
    
    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        if (rand() < density) {
          const w = Math.floor(rand() * (maxWeight + 1));
          mat[i][j] = w;
          mat[j][i] = w;
        } else {
          mat[i][j] = 0;
          mat[j][i] = 0;
        }
      }
    }
    return mat;
  }

  function getDynamicDefaultMatrix(sizeType) {
    switch(sizeType) {
      case 'small':
        // Pequeña: 4-8 componentes, densidad alta
        const n = Math.floor(Math.random() * (8 - 4 + 1)) + 4;
        return generateSymmetricMatrix(n, 0.8, 8);
      case 'medium':
        // Mediana: 10-20 componentes, densidad media
        const n2 = Math.floor(Math.random() * (20 - 10 + 1)) + 10;
        return generateSymmetricMatrix(n2, 0.5, 12);
      case 'large':
        // Grande: 30-50 componentes, densidad baja
        const n3 = Math.floor(Math.random() * (50 - 30 + 1)) + 30;
        return generateSymmetricMatrix(n3, 0.25, 15);
      default:
        return generateSymmetricMatrix(13, 0.5, 10);
    }
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
      
      // Cargar y mostrar la sección de gráficas con cache-busting
      const timestamp = Date.now();
      document.getElementById("plot-time").src = `http://localhost:5000/api/plots/execution_time_vs_problem_size.png?t=${timestamp}`;
      document.getElementById("plot-quality").src = `http://localhost:5000/api/plots/solution_quality_vs_parameter.png?t=${timestamp}`;
      document.getElementById("plot-memory").src = `http://localhost:5000/api/plots/memory_vs_problem_size.png?t=${timestamp}`;
      document.getElementById("plots-card").style.display = "block";
    }
  });
});
