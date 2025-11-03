import networkx as nx
from itertools import combinations

def construir_grafo_coocurrencia(abstracts_limpios, lista_terminos):

    # Inicializar grafo no dirigido
    grafo = nx.Graph()

    # Asegurar que todos los términos estén como nodos
    for termino in lista_terminos:
        grafo.add_node(termino)

    # Procesar cada abstract
    for abstract in abstracts_limpios:
        # Identificar términos presentes en el abstract
        presentes = [t for t in lista_terminos if t in abstract.split()]
        presentes_unicos = set(presentes)

        # Generar todas las combinaciones de pares únicos
        for termino1, termino2 in combinations(presentes_unicos, 2):
            if grafo.has_edge(termino1, termino2):
                grafo[termino1][termino2]['weight'] += 1
            else:
                grafo.add_edge(termino1, termino2, weight=1)

    return grafo


def analizar_grado_nodos(grafo):
    """
    Calcula el grado simple y ponderado de cada nodo en el grafo.

    Parameters:
    - grafo: objeto NetworkX.Graph previamente construido.

    Returns:
    - grados: diccionario con el grado simple de cada nodo.
    - grados_ponderados: diccionario con el grado ponderado de cada nodo.
    - top_nodos: lista de nodos ordenados por grado ponderado (de mayor a menor).
    """
    # Grado simple: número de conexiones por nodo
    grados = dict(grafo.degree())

    # Grado ponderado: suma de los pesos de las aristas por nodo
    grados_ponderados = dict(grafo.degree(weight='weight'))

    # Ordenar nodos por grado ponderado descendente
    top_nodos = sorted(grados_ponderados.items(), key=lambda x: x[1], reverse=True)

    return grados, grados_ponderados, top_nodos

def detectar_componentes_conexas(grafo):
    """
    Detecta componentes conexas en el grafo de coocurrencia.

    Parameters:
    - grafo: objeto NetworkX.Graph previamente construido.

    Returns:
    - componentes: lista de conjuntos, cada uno contiene los nodos de una componente conexa.
    """
    # Utiliza el algoritmo de componentes conexas de NetworkX
    componentes = list(nx.connected_components(grafo))

    # Ordenar componentes por tamaño (opcional)
    componentes_ordenadas = sorted(componentes, key=lambda x: len(x), reverse=True)

    return componentes_ordenadas

