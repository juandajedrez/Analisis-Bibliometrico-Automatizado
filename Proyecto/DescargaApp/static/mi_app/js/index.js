document.addEventListener("DOMContentLoaded", () => {
  const boton = document.getElementById("btnEnviar");
  const campo = document.getElementById("campoDato");

  boton.addEventListener("click", async () => {
    const valor = campo.value.trim();
    if (!valor) {
      alert("Por favor ingrese un valor antes de ejecutar los algoritmos.");
      return;
    }

    // Limpiar resultados previos
    ["tablaJacardi", "tablaLcs", "tablaCosen", "tablaLeven"].forEach(id => {
      const div = document.getElementById(id);
      if (div) div.innerHTML = "";
    });

    try {
      // Ejecutar las 4 peticiones simultáneamente
      const endpoints = ["/jacardi", "/lcs", "/cosen", "/leven"];
      const fetches = endpoints.map(url =>
        fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ dato: valor })
        })
      );

      const responses = await Promise.all(fetches);

      // Convertir respuestas a JSON y manejar errores si no es válido
      const resultados = await Promise.all(responses.map(async res => {
        try {
          const json = await res.json();
          console.log(json)
          return json
        } catch (e) {
          console.error("Error al parsear JSON:", e);
          return []; // Retornar arreglo vacío si falla
        }
      }));

      // Crear tablas con validación de datos
      const nombresTablas = ["tablaJacardi", "tablaLcs", "tablaCosen", "tablaLeven"];
      const titulos = ["Jaccard", "LCS", "Cosen", "Levenshtein"];

      resultados.forEach((datos, i) => {
        crearTabla(nombresTablas[i], titulos[i], datos);
      });

    } catch (error) {
      console.error("Error al obtener los resultados:", error);
      alert("Ocurrió un error al comunicarse con el servidor.");
    }
  });

  // Función para crear una tabla con los resultados
  function crearTabla(idDiv, titulo, datos) {
    const div = document.getElementById(idDiv);

    if (!div) return;

    if (!datos || !Array.isArray(datos) || datos.length === 0 || !datos[0]) {
      div.innerHTML = `<h3>${titulo}</h3><p>No se encontraron resultados</p>`;
      return;
    }

    let tabla = `<h3>${titulo}</h3><table border="1"><thead><tr>`;
    const headers = Object.keys(datos[0]);
    headers.forEach(h => tabla += `<th>${h}</th>`);
    tabla += `</tr></thead><tbody>`;

    datos.forEach(fila => {
      tabla += `<tr>`;
      headers.forEach(h => tabla += `<td>${fila[h] !== undefined ? fila[h] : ''}</td>`);
      tabla += `</tr>`;
    });

    tabla += `</tbody></table>`;
    div.innerHTML = tabla;
  }
});

