import networkx as nx
from django.test import TestCase
from parte2 import functions

from .dkfunction import analyze_dijkstra_paths
from .floy import analyze_floyd_warshall
from .functions import build_citation_graph


class GroupOfFilesTestCase(TestCase):
    def test_group_of_files(self):
        # Llamamos a la función
        articles = functions.groupOfFiles()

        self.assertIsNotNone(articles)
        self.assertIsInstance(articles, list)
        # Puedes ajustar esto según tus datos:
        # self.assertEqual(len(articles), 10)


class CitationGraphTest(TestCase):
    def setUp(self):
        # Simulamos unos artículos
        self.articles = functions.groupOfFiles()
        # Creamos el grafo
        self.G = build_citation_graph(
            self.articles, threshold=0.4
        )  # threshold ajustable

    def test_dijkstra_paths(self):
        source_key = self.articles[0]["key"]
        results = analyze_dijkstra_paths(self.G, self.articles, source_key=source_key)
        print(results)

        node_keys = [a["key"] for a in self.articles]
        result_keys = [r["target"] for r in results]

        # Solo los nodos alcanzables están en los resultados
        self.assertTrue(set(result_keys).issubset(set(node_keys)))

        # Test: El camino al mismo nodo debe ser sólo el nodo (camino trivial)
        for r in results:
            if r["target"] == source_key:
                self.assertEqual(r["path"], [source_key])
                self.assertEqual(r["distance"], 0.0)

        # Test: La suma de los pesos del camino coincide con 'distance'
        for r in results:
            path = r["path"]
            if len(path) == 1:
                continue
            dist_calc = 0.0
            for i in range(len(path) - 1):
                dist_calc += self.G[path[i]][path[i + 1]]["weight"]
            self.assertAlmostEqual(r["distance"], dist_calc, places=6)


class FloydWarshallTest(TestCase):
    def setUp(self):
        # Grafo simple dirigido con similitud como pesos
        self.G = nx.DiGraph()
        self.G.add_edge("A", "B", weight=0.8)
        self.G.add_edge("B", "C", weight=0.7)
        self.G.add_edge("A", "C", weight=0.4)
        self.G.add_edge("C", "A", weight=0.3)

    def test_floyd_warshall_results(self):
        results = analyze_floyd_warshall(self.G)

        possible_pairs = [
            (u, v) for u in self.G.nodes() for v in self.G.nodes() if u != v
        ]
        result_pairs = [(r["source"], r["target"]) for r in results]
        self.assertCountEqual(possible_pairs, result_pairs)

        for r in results:
            self.assertIsInstance(r["distance"], float)
            self.assertGreaterEqual(r["distance"], 0)

        # El path, si existe, empieza en source y termina en target
        for r in results:
            if r["path"]:
                self.assertEqual(r["path"][0], r["source"])
                self.assertEqual(r["path"][-1], r["target"])
            else:
                self.assertEqual(r["distance"], float("inf"))

        # La suma de los pesos del camino debe coincidir con la distancia
        # *** Ojo: la función ya transformó los pesos antes del algoritmo ***
        for r in results:
            if r["path"] and len(r["path"]) > 1:
                dist_calc = 0.0
                for i in range(len(r["path"]) - 1):
                    # Usar el peso tal como está en el grafo
                    dist_calc += self.G[r["path"][i]][r["path"][i + 1]]["weight"]
                self.assertAlmostEqual(r["distance"], dist_calc, places=6)
