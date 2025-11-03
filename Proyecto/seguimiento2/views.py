from django.http import JsonResponse
from parte2 import functions
from .functions import build_citation_graph
from .dkfunction import analyze_dijkstra_paths

def resultados_view(request):
    articulos = functions.groupOfFiles()
    G = build_citation_graph(articulos, threshold=0.4)
    resultados = analyze_dijkstra_paths(G, articulos, source_key=articulos[0]["key"])
    return JsonResponse(resultados, safe=False)
