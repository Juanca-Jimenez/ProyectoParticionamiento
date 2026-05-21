document.addEventListener("DOMContentLoaded", () => {
  const runButton = document.getElementById("run-button");
  const csvFileInput = document.getElementById("csv-file");
  const matrixInput = document.getElementById("matrix-input");
  const kInput = document.getElementById("k-input");
  const defaultSelect = document.getElementById("default-matrix-select");
  const useDefaultButton = document.getElementById("use-default-button");
  let currentMatrix = null;

  // Generate and store three default matrices (deterministic)
  const defaultMatrices = generateDefaultMatrices();

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
    const csv = matrixToCsv(defaultMatrices[sel]);
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

  function generateSymmetricMatrix(n, density = 0.5, maxWeight = 10, seed = 12345) {
    const rand = lcg(seed + n);
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

  function generateDefaultMatrices() {
    return {
      small: generateSymmetricMatrix(6, 0.8, 8, 101),
      medium: generateSymmetricMatrix(14, 0.5, 12, 202),
      large: generateSymmetricMatrix(30, 0.25, 15, 303),
    };
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
