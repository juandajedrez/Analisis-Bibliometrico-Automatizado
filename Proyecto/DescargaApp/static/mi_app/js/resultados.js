document.addEventListener("DOMContentLoaded", () => {
  // ======= Funciones para cargar los datos =======
  const cargarDatos = async (url, tablaBody, columnas, nombreAlgoritmo) => {
    tablaBody.innerHTML = `
            <tr><td colspan="${columnas}" class="mensaje">Cargando resultados de ${nombreAlgoritmo}...</td></tr>
        `;
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Error al cargar ${nombreAlgoritmo}`);
      const data = await response.json();
      renderTabla(tablaBody, data, nombreAlgoritmo);
    } catch (error) {
      console.error(`Error en ${nombreAlgoritmo}:`, error);
      tablaBody.innerHTML = `
                <tr><td colspan="${columnas}" class="mensaje" style="color:red;">Error al cargar ${nombreAlgoritmo}</td></tr>
            `;
    }
  };

  const renderTabla = (tablaBody, data, nombreAlgoritmo) => {
    tablaBody.innerHTML = "";
    if (!data || !data.length) {
      tablaBody.innerHTML = `<tr><td colspan="4" class="mensaje">No se encontraron resultados para ${nombreAlgoritmo}</td></tr>`;
      return;
    }

    // Detectar tipo de datos (Dijkstra/Floyd o Componentes)
    const isComponentes = data[0].hasOwnProperty("nodos");

    data.forEach(res => {
      const tr = document.createElement("tr");

      if (isComponentes) {
        tr.innerHTML = `
                    <td>${res.id}</td>
                    <td>${res.nodos.join(", ")}</td>
                `;
      } else {
        tr.innerHTML = `
                    <td>${res.source}</td>
                    <td>${res.target}</td>
                    <td>${res.distance.toFixed(6)}</td>
                    <td>${res.path ? res.path.join(" → ") : "N/A"}</td>
                `;
      }

      tablaBody.appendChild(tr);
    });
  };

  // ======= Cargar cada tabla =======
  cargarDatos("/api/resultados", document.getElementById("tablaDijkstra"), 4, "Dijkstra");
  cargarDatos("/api/floyd", document.getElementById("tablaFloyd"), 4, "Floyd–Warshall");
  cargarDatos("/api/componentes/", document.getElementById("tablaComponentes"), 2, "Componentes");

  // ======= Sistema de pestañas =======
  const buttons = document.querySelectorAll(".tab-button");
  const contents = document.querySelectorAll(".tab-content");

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      buttons.forEach(b => b.classList.remove("active"));
      contents.forEach(c => c.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(btn.dataset.tab).classList.add("active");
    });
  });
});

