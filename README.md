# 📊 Proyecto: Análisis Bibliométrico Automatizado

## 🧠 Introducción
La bibliometría es una disciplina que permite explorar y analizar volúmenes de datos derivados de la producción científica mediante métodos cuantitativos y cualitativos. Se fundamenta en matemáticas y estadística para establecer descripciones, relaciones, inferencias y visualizaciones sobre publicaciones científicas en diversas áreas del conocimiento.

Este proyecto aplica técnicas bibliométricas y algoritmos computacionales para analizar la producción científica en un dominio específico, utilizando bases de datos académicas disponibles en la Universidad del Quindío.

## 🔍 Fuentes de Información
Las bases de datos científicas utilizadas están disponibles en [https://library.uniquindio.edu.co/databases](https://library.uniquindio.edu.co/databases), agrupadas por facultades. Algunas de ellas incluyen:

- ACM Digital Library
- SAGE Journals
- ScienceDirect

Los formatos de exportación incluyen: RIS, BibTex, CSV, texto plano, entre otros. Las tipologías de productos científicos abarcan artículos, conferencias, capítulos de libro, etc.

## 🎯 Propósito del Proyecto
Desarrollar una aplicación que implemente algoritmos para el análisis bibliométrico automatizado sobre un dominio de conocimiento, integrando:

- Descarga y unificación de datos científicos.
- Algoritmos de similitud textual.
- Análisis de frecuencia de términos.
- Agrupamiento jerárquico de abstracts.
- Visualización geográfica, temporal y semántica.
- Documentación técnica y despliegue funcional.

## ✅ Requerimientos Funcionales
1. **Automatización de Descarga y Unificación:**  
   Descargar datos desde dos bases de datos, unificar registros eliminando duplicados, y generar archivo secundario con los productos eliminados.

2. **Similitud Textual:**  
   Implementar 4 algoritmos clásicos y 2 basados en IA, permitir análisis entre abstracts seleccionados y documentar el funcionamiento matemático.

3. **Frecuencia de Términos por Categoría:**  
   Analizar frecuencia de términos asociados, generar lista de términos emergentes y evaluar su precisión.

4. **Agrupamiento Jerárquico:**  
   Preprocesar texto, calcular similitud, aplicar clustering y representar mediante dendrograma.

5. **Visualización Científica:**  
   Mapa de calor geográfico, nube de palabras dinámica, línea temporal de publicaciones y exportación a PDF.

6. **Documentación Técnica:**  
   Documento de diseño con arquitectura, explicación técnica por requerimiento, fundamentación del uso de IA y manual de usuario.

## 🚀 Despliegue
La aplicación está empaquetada y lista para ejecución en una máquina virtual con Debian en Google Cloud.

## 📄 Licencia
Este proyecto es desarrollado con fines académicos en el marco del curso de Análisis de Algoritmos de la Universidad del Quindío.

