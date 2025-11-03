document.addEventListener('DOMContentLoaded', function () {
  const tabla = document.getElementById("tablaResultados");
  // Si hay muchas filas, ajusta la fuente y la altura para mejor visibilidad
  const filas = tabla.getElementsByTagName("tbody")[0].rows.length;
  if (filas > 20) {
    tabla.style.fontSize = "0.85rem";
    tabla.parentElement.style.maxHeight = "78vh";
  }
});
