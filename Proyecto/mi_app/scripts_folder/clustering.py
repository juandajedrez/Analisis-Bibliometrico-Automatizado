# Modulos estándar de Python
import os
from typing import List, Dict, Tuple

# Librerías científicas
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Scikit-learn (procesamiento y métricas) 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances, silhouette_score

# SciPy (clustering jerárquico y distancias) 
from scipy.cluster.hierarchy import linkage, dendrogram, cophenet, fcluster
from scipy.spatial.distance import pdist, squareform

# Manejo de archivos BibTeX 
import bibtexparser


# Obtenemos solo los Abstracts del archivo bibtex
def load_abstracts_from_bibtex(path: str) -> List[Dict]:
    with open(path, 'r', encoding='utf-8') as f:
        bib = bibtexparser.load(f)
    entries = []
    #el cuerpo de los entries se compone de abstract y titulo del articulo y el ID
    for e in bib.entries:
        abstract = e.get('abstract') or ''
        title = e.get('title') or e.get('ID') or ''
        entries.append({'id': e.get('ID', ''), 'title': title, 'abstract': abstract})
    return entries

# vectorizamos los abstract por medio del metodo TF-IDF
def preprocess_and_vectorize(abstracts: List[str],
                             language: str = 'english',
                             max_features: int = 5000,
                             ngram_range=(1,1)) -> Tuple[np.ndarray, TfidfVectorizer]:
    vec = TfidfVectorizer(stop_words=language, max_features=max_features, ngram_range=ngram_range)
    X = vec.fit_transform(abstracts)
    return X.toarray(), vec

# calcula la matriz de distancias preparada para linkage.
def compute_distance_matrix(X: np.ndarray, metric: str = 'cosine') -> np.ndarray:
    
    if metric == 'cosine':
        D = pairwise_distances(X, metric='cosine')
        D = (D + D.T) / 2.0
        np.fill_diagonal(D, 0.0)
        return squareform(D)  #vector condensado de distancias (formato requerido por scipy.linkage).
    else:
        return pdist(X, metric=metric)

# corremos los metodos de clustering
def run_hierarchical_methods(condensed_dist: np.ndarray,
                             methods: List[str] = None) -> Dict[str, np.ndarray]:
    if methods is None:
        methods = ['single', 'complete', 'average']  # linkage methods
    Zs = {}
    for m in methods:
        Zs[m] = linkage(condensed_dist, method=m)
    return Zs

# realizamos la evaluación de los metodos para definir el mejor
def evaluate_methods(Zs: Dict[str, np.ndarray], condensed_dist: np.ndarray, X: np.ndarray,
                     k_eval: int = 5) -> Dict[str, Dict]:
    results = {}

    for name, Z in Zs.items():
        coph_corr, coph_dists = cophenet(Z, condensed_dist)
        # silhouette: need cluster labels; compute for a range of K and take best
        best_sil = None
        best_k = None

        for k in range(2, min(k_eval+1, X.shape[0])):
            labels = fcluster(Z, k, criterion='maxclust')
            try:
                sil = silhouette_score(X, labels, metric='cosine')
            except Exception:
                sil = -1
            if best_sil is None or sil > best_sil:
                best_sil = sil
                best_k = k
        results[name] = {'cophenet': float(coph_corr), 'best_silhouette': float(best_sil), 'best_k': int(best_k)}
    return results

# guardamos las graficas de los dendogramas
def plot_and_save_dendrogram(Z: np.ndarray, labels: List[str], out_path: str,
                             truncate_mode=None, p=30):
    num_labels = len(labels)
    max_label_len = max(len(label) for label in labels)

    # Ajuste dinámico del tamaño de la figura
    width = max(12, num_labels * 0.4)
    height = max(6, max_label_len * 0.2)

    plt.figure(figsize=(width, height))
    dendrogram(Z,
               labels=labels,
               leaf_rotation=90,
               leaf_font_size=10,
               truncate_mode=truncate_mode,
               p=p,
               color_threshold=None)

    # Ajustar márgenes para evitar corte de etiquetas
    plt.subplots_adjust(bottom=0.3) 

    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


# Funcion root que ejecuta todas las demas en orden
def pipeline_from_bibtex(bibpath: str, out_dir: str,
                         language: str = 'english',
                         methods: List[str] = None) -> Dict:
    os.makedirs(out_dir, exist_ok=True)
    entries = load_abstracts_from_bibtex(bibpath)
    abstracts = [e['abstract'] or '' for e in entries]
    titles = [e['title'] or e['id'] for e in entries]
    X, vec = preprocess_and_vectorize(abstracts, language=language)
    condensed = compute_distance_matrix(X, metric='cosine')
    Zs = run_hierarchical_methods(condensed, methods=methods)
    evals = evaluate_methods(Zs, condensed, X, k_eval=10)
    outputs = {}
    for name, Z in Zs.items():
        out_png = os.path.join(out_dir, f'dendrogram_{name}.png')
        plot_and_save_dendrogram(Z, labels=titles, out_path=out_png)
        outputs[name] = {#'dendrogram': out_png, 
                         'cophenet': evals[name]['cophenet'],
                         'best_silhouette': evals[name]['best_silhouette'],
                         'best_k': evals[name]['best_k']}
    
    # Elige lo mejor de Cophenet y luego Silhouette
    best = max(outputs.items(), key=lambda kv: (kv[1]['cophenet'], kv[1]['best_silhouette']))[0]
    
    resumen = f"Evaluación de métodos de agrupamiento jerárquico sobre {len(entries)} entradas:\n\n"
    for metodo, datos in outputs.items():
        resumen += (
            f"  Método: **{metodo}**\n"
            f"   - Coeficiente de correlación cophenética: {datos['cophenet']:.4f}\n"
            f"   - Mejor puntuación de Silhouette: {datos['best_silhouette']:.4f}\n"
            f"   - Número óptimo de clústeres (k): {datos['best_k']}\n\n"
        )
    resumen += f"El método con mejores resultados es **{best}**, seleccionado por tener la mayor combinación de cophenet y Silhouette.\n"
    return resumen
