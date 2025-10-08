import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar un modelo preentrenado de SBERT
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
# También podrías usar otros modelos disponibles en sentence‑transformers


def texto_a_embedding(model, texto):
    """
    Convierte un texto (oración, frase) a su embedding usando SBERT.
    """
    # encode devuelve un vector numpy (por defecto)
    emb = model.encode(texto, convert_to_numpy=True)
    return emb


def similitud_coseno(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """
    Calcula la similitud coseno entre dos vectores embeddings.
    Devuelve un valor entre -1 y 1 (usualmente entre 0 y 1 para embeddings positivos).
    """
    # reshape para sklearn si es necesario
    sim = cosine_similarity(emb1.reshape(1, -1), emb2.reshape(1, -1))
    return float(sim[0][0])


# Ejemplo de uso
if __name__ == "__main__":
    texto1 = "El gato está durmiendo en la alfombra."
    texto2 = "Un felino reposa sobre la alfombra."

    emb1 = texto_a_embedding(model, texto1)
    emb2 = texto_a_embedding(model, texto2)

    score = similitud_coseno(emb1, emb2)
    print("Similitud (coseno) entre los textos:", score)
