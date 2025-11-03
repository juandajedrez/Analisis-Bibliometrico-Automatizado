import networkx as nx


def analyze_dijkstra_paths(G, articles, source_key=None):
    # Ajusta los pesos para Dijkstra: inverso de la similitud y garantiza no negativos
    for u, v, data in G.edges(data=True):
        sim = data["weight"]
        inv_weight = 1 - sim
        if inv_weight < 0:
            inv_weight = 0.0
        data["weight"] = inv_weight

    if source_key is None:
        source_key = articles[0]["key"]

    distances, paths = nx.single_source_dijkstra(G, source=source_key, weight="weight")

    results = []
    for (
        target,
        distance,
    ) in distances.items():  # pyright: ignore[reportAttributeAccessIssue]
        results.append(
            {
                "source": source_key,
                "target": target,
                "distance": float(distance),
                "path": paths[target],
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
    scc_generator = nx.strongly_connected_components(G)
    scc_list = [list(component) for component in scc_generator]
    return scc_list
