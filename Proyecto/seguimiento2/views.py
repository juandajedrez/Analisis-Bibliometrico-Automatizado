from django.http import JsonResponse
from parte2 import functions

from .dkfunction import analyze_dijkstra_paths
from .floy import find_strongly_connected_components
from .functions import build_citation_graph

articulos = functions.groupOfFiles()
G = build_citation_graph(articulos, threshold=0.4)


def resultados_view(request):
    print(articulos)
    resultados = analyze_dijkstra_paths(G, articulos, source_key=articulos[0]["key"])
    return JsonResponse(resultados, safe=False)


def componentes_view(request):
    try:

        componentes = find_strongly_connected_components(G)

        data = [{"id": i + 1, "nodos": comp} for i, comp in enumerate(componentes)]

        return JsonResponse(data, safe=False)

    except Exception as e:
        print("Error en componentes_view:", e)
        return JsonResponse({"error": str(e)}, status=500)


def nodos_view(request):
    try:
        nodos = []
        for node in G.nodes():
            # Busca el artículo original que coincide con el nodo
            articulo = next((a for a in articulos if a["key"] == node), None)
            if articulo:
                nodos.append(
                    {
                        "key": articulo["key"],
                        "title": articulo["title"],
                        "abstract": articulo["abstract"],
                    }
                )
            else:
                nodos.append({"key": node, "title": "Desconocido", "abstract": ""})

        return JsonResponse(nodos, safe=False)

    except Exception as e:
        print("Error en nodos_view:", e)
        return JsonResponse({"error": str(e)}, status=500)
