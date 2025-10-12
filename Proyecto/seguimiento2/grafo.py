import networkx as nx


def addGraph(articleToAdd):
    grafo.add_node(str(articleToAdd["title"]), **articleToAdd)


grafo = nx.DiGraph()
