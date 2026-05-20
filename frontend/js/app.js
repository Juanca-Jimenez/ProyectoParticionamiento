document.addEventListener("DOMContentLoaded", () => {
  const runButton = document.getElementById("run-button");
  const csvFileInput = document.getElementById("csv-file");
  const matrixInput = document.getElementById("matrix-input");
  const kInput = document.getElementById("k-input");

  csvFileInput.addEventListener("change", async (event) => {
    const file = event.target.files[0];
    if (!file) {
      return;
    }
    const text = await file.text();
    matrixInput.value = text.trim();
  });

  runButton.addEventListener("click", async () => {
    const matrixText = matrixInput.value.trim();
    const k = parseInt(kInput.value, 10);
    if (!matrixText) {
      alert("Ingresa la matriz de dependencias o carga un CSV.");
      return;
    }

    const matrix = matrixText.split(/\r?\n/).map((line) => line.split(",").map((cell) => cell.trim()));
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
  });
});
