<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Proyecto: Análisis Bibliométrico Automatizado</title>
</head>
<body>

  <h1>📊 Proyecto: Análisis Bibliométrico Automatizado</h1>

  <h2>🧠 Introducción</h2>
  <p>
    La bibliometría es una disciplina que permite explorar y analizar volúmenes de datos derivados de la producción científica mediante métodos cuantitativos y cualitativos. Se fundamenta en matemáticas y estadística para establecer descripciones, relaciones, inferencias y visualizaciones sobre publicaciones científicas en diversas áreas del conocimiento.
  </p>
  <p>
    Este proyecto aplica técnicas bibliométricas y algoritmos computacionales para analizar la producción científica en un dominio específico, utilizando bases de datos académicas disponibles en la Universidad del Quindío.
  </p>

  <h2>🔍 Fuentes de Información</h2>
  <p>
    Las bases de datos científicas utilizadas están disponibles en <a href="https://library.uniquindio.edu.co/databases" target="_blank">https://library.uniquindio.edu.co/databases</a>, agrupadas por facultades. Algunas de ellas incluyen:
  </p>
  <ul>
    <li>ACM Digital Library</li>
    <li>SAGE Journals</li>
    <li>ScienceDirect</li>
  </ul>
  <p>
    Los formatos de exportación incluyen: RIS, BibTex, CSV, texto plano, entre otros. Las tipologías de productos científicos abarcan artículos, conferencias, capítulos de libro, etc.
  </p>

  <h2>🎯 Propósito del Proyecto</h2>
  <p>
    Desarrollar una aplicación que implemente algoritmos para el análisis bibliométrico automatizado sobre un dominio de conocimiento, integrando:
  </p>
  <ul>
    <li>Descarga y unificación de datos científicos.</li>
    <li>Algoritmos de similitud textual.</li>
    <li>Análisis de frecuencia de términos.</li>
    <li>Agrupamiento jerárquico de abstracts.</li>
    <li>Visualización geográfica, temporal y semántica.</li>
    <li>Documentación técnica y despliegue funcional.</li>
  </ul>

  <h2>✅ Requerimientos Funcionales</h2>
  <ol>
    <li>
      <strong>Automatización de Descarga y Unificación:</strong> Descargar datos desde dos bases de datos, unificar registros eliminando duplicados, y generar archivo secundario con los productos eliminados.
    </li>
    <li>
      <strong>Similitud Textual:</strong> Implementar 4 algoritmos clásicos y 2 basados en IA, permitir análisis entre abstracts seleccionados y documentar el funcionamiento matemático.
    </li>
    <li>
      <strong>Frecuencia de Términos por Categoría:</strong> Analizar frecuencia de términos asociados, generar lista de términos emergentes y evaluar su precisión.
    </li>
    <li>
      <strong>Agrupamiento Jerárquico:</strong> Preprocesar texto, calcular similitud, aplicar clustering y representar mediante dendrograma.
    </li>
    <li>
      <strong>Visualización Científica:</strong> Mapa de calor geográfico, nube de palabras dinámica, línea temporal de publicaciones y exportación a PDF.
    </li>
    <li>
      <strong>Documentación Técnica:</strong> Documento de diseño con arquitectura, explicación técnica por requerimiento, fundamentación del uso de IA y manual de usuario.
    </li>
  </ol>

  

  <h2>🚀 Despliegue</h2>
  <p>
    La aplicación está empaquetada y lista para ejecución en una maquina virtual con debian en Google cloud.
  </p>

  <h2>📄 Licencia</h2>
  <p>
    Este proyecto es desarrollado con fines académicos en el marco del curso de Análisis de Algoritmos de la Universidad del Quindío.
  </p>

</body>
</html>
