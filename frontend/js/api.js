async function callPartitionApi(payload) {
  try {
    const response = await fetch("http://localhost:5000/api/partition", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    return await response.json();
  } catch (error) {
    return { error: "No se pudo conectar con el servidor backend." };
  }
}
