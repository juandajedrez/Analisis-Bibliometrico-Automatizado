document.addEventListener("DOMContentLoaded", async () => {
  const tablaBody = document.querySelector("#tablaResultados tbody");

  try {
    const response = await fetch("/api/resultados/");
    if (!response.ok) throw new Error("Error al cargar los resultados");

    const data = await response.json();
    tablaBody.innerHTML = ""; // limpia la tabla

    data.forEach((res) => {
      const row = document.createElement("tr");
      row.innerHTML = `
                <td>${res.source}</td>
                <td>${res.target}</td>
                <td>${res.distance.toFixed(6)}</td>
                <td>${res.path ? res.path.join(" → ") : "N/A"}</td>
            `;
      tablaBody.appendChild(row);
    });
  } catch (error) {
    console.error("Error al obtener los resultados:", error);
    tablaBody.innerHTML = `
            <tr><td colspan="4" style="color:red;">Error al cargar los resultados</td></tr>
        `;
  }
});

