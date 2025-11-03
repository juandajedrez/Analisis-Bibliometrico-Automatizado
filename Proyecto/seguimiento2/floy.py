
import networkx as nx
def analyze_floyd_warshall(G):
    """
    Calcula caminos mínimos entre todos los nodos usando Floyd–Warshall.

    Retorna:
        list[dict]: [{'source', 'target', 'distance', 'path'}, ...]
    """

    # Convertir similitud → distancia
    for u, v, data in G.edges(data=True):
        data["weight"] = 1 - data["weight"]

    # Floyd–Warshall predecesores y distancias
    predecesores, distancias = nx.floyd_warshall_predecessor_and_distance(
        G, weight="weight"
    )

    def reconstruir_camino(predecesores, origen, destino):
        if origen == destino:
            return [origen]
        if destino not in predecesores[origen]:
            return None
        camino = [destino]
        while camino[-1] != origen:
            camino.append(predecesores[origen][camino[-1]])
        camino.reverse()
        return camino

    # Construir lista de resultados
    results = []
    for origen in G.nodes():
        for destino in G.nodes():
            if origen != destino:
                distancia = distancias.get(origen, {}).get(destino, float("inf"))
                camino = reconstruir_camino(predecesores, origen, destino)
                results.append(
                    {
                        "source": origen,
                        "target": destino,
                        "distance": float(distancia),
                        "path": camino,
                    }
                )

    return results

def find_strongly_connected_components(G):
    """
    Identifica los grupos de artículos fuertemente interrelacionados
    en un grafo dirigido de citaciones.

    Parámetros:
    -----------
    G : nx.DiGraph
        Grafo de citaciones.

    Retorna:
    --------
    list[list[str]]
        Lista de componentes, cada componente es una lista de claves de artículos.
    """
    # NetworkX devuelve un generador de listas de nodos
    scc_generator = nx.strongly_connected_components(G)

    # Convertir a lista de listas
    scc_list = [list(component) for component in scc_generator]

    return scc_list
