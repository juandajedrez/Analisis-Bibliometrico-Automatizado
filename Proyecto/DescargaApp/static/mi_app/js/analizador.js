document.getElementById("btnAnalizar").addEventListener("click", async () => {
  const topN = parseInt(document.getElementById("top_n").value);
  const resultadosDiv = document.getElementById("resultados");

  resultadosDiv.innerHTML = "<p>Procesando análisis... ⏳</p>";

  try {
    const response = await fetch("/analizer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ top_n: topN })
    });

    if (!response.ok) throw new Error("Error al realizar el análisis.");

    const data = await response.json();
    mostrarResultados(data);

  } catch (error) {
    resultadosDiv.innerHTML = `<p style="color:red;">${error.message}</p>`;
  }
});

function mostrarResultados(data) {
  const resultadosDiv = document.getElementById("resultados");

  if (!data || !data.palabras_asociadas) {
    resultadosDiv.innerHTML = "<p>No se encontraron resultados.</p>";
    return;
  }

  let html = `
    <h2>Resultados del análisis</h2>
    <p><strong>Precisión:</strong> ${(data.precision * 100).toFixed(2)}%</p>
    <table class="tabla-resultados">
      <thead>
        <tr>
          <th>Palabra</th>
          <th>Frecuencia</th>
          <th>TF-IDF</th>
          <th>Score</th>
          <th>Tipo</th>
        </tr>
      </thead>
      <tbody>
  `;

  data.palabras_asociadas.forEach(p => {
    html += `
      <tr>
        <td>${p.palabra}</td>
        <td>${p.frecuencia ?? "-"}</td>
        <td>${p.tfidf.toFixed(4)}</td>
        <td>${p.score.toFixed(4)}</td>
        <td>${p.nueva ? "🆕 Nueva" : "✅ Clave"}</td>
      </tr>
    `;
  });

  html += "</tbody></table>";
  resultadosDiv.innerHTML = html;
}

