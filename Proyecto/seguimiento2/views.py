from django.shortcuts import render
from parte2 import functions

# Create your views here.
def resultados_view(request):
    # generar artículos y grafo como en tus pruebas
    articulos= functions.groupOfFiles()
    G = build_citation_graph(articulos, threshold=0.4)
    resultados = analyze_dijkstra_paths(G, articulos, source_key=articulos[0]["key"])
    return render(request, "resultados.html", {"resultados": resultados})
