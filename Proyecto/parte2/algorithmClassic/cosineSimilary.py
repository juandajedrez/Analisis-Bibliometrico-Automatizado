import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def cosine_similarity_manual(matrix):
    """
    matrix: numpy array o scipy sparse, con dimensión (n_docs, n_features)
    retorna: matriz simétrica (n_docs × n_docs)
    """
    M = matrix.toarray() if hasattr(matrix, "toarray") else matrix
    n = M.shape[0]
    sim = np.zeros((n, n))
    norms = np.linalg.norm(M, axis=1)

    for i in range(n):
        for j in range(n):
            if norms[i] == 0 or norms[j] == 0:
                sim[i, j] = 0.0
            else:
                sim[i, j] = np.dot(M[i], M[j]) / (norms[i] * norms[j])

    return sim


def cosine_similarity_between_texts(text1, text2):
    """
    text1, text2: cadenas de texto
    Retorna: valor de similitud del coseno entre ambos textos
    """
    docs = [text1, text2]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs)
    sim_matrix = cosine_similarity_manual(tfidf_matrix)
    return sim_matrix[0, 1]
