import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_citation_graph(articles, threshold=0.4):
    """
    Construye un grafo dirigido de citaciones a partir de una lista de artículos.
    Cada nodo es un artículo y cada arista indica citación implícita basada en similitud TF-IDF + coseno.

    Parámetros:
    -----------
    articles : list[dict]
        Lista de artículos, cada uno con 'key', 'title' y 'abstract'.
    threshold : float
        Umbral mínimo de similitud para crear una arista (0–1).

    Retorna:
    --------
    G : nx.DiGraph
        Grafo dirigido con nodos y aristas ponderadas por similitud.
    """
    articles = [a for a in articles if "key" in a and "title" in a and "abstract" in a]
    if not articles:
        raise ValueError("No hay artículos válidos con 'key', 'title' y 'abstract'.")

    keys = [a["key"] for a in articles]
    texts = [f"{a['title']} {a['abstract']}" for a in articles]

    tfidf_matrix = TfidfVectorizer(stop_words="english").fit_transform(texts)
    sim_matrix = cosine_similarity(tfidf_matrix)

    G = nx.DiGraph()
    G.add_nodes_from(keys)

    n = len(keys)
    for i in range(n):
        for j in range(n):
            if i != j:
                sim = float(sim_matrix[i, j])
                if sim > threshold:
                    G.add_edge(keys[i], keys[j], weight=sim)

    for u, v, data in list(G.edges(data=True)):
        try:
            data["weight"] = float(data["weight"])
        except:
            G.remove_edge(u, v)

    return G
