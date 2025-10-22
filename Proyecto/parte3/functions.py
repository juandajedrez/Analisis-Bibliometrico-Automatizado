import re

import numpy as np
from parte2 import functions
from sklearn.feature_extraction.text import TfidfVectorizer


class KeywordAnalyzerComplete:
    def __init__(self, palabras_clave, ngram_range=(1, 3)):
        """
        palabras_clave: lista de palabras o frases clave
        ngram_range: rango de n-grams para detectar frases en TF-IDF
        """
        self.palabras_clave = [p.lower() for p in palabras_clave]
        self.ngram_range = ngram_range

    def limpiar_texto(self, texto):
        """Limpia el texto: minúsculas y elimina puntuación"""
        if not isinstance(texto, str):
            return ""
        return re.sub(r"[^\w\s-]", "", texto.lower())

    def analizar(self, abstracts, top_n=15):
        """
        Analiza los abstracts y devuelve un diccionario con resultados de frecuencia,
        TF-IDF y detección de nuevas palabras.
        """
        if not abstracts or not isinstance(abstracts, list):
            raise ValueError("La lista de abstracts está vacía o no es válida.")

        # Limpiar abstracts
        abstracts_clean = [
            self.limpiar_texto(a) for a in abstracts if isinstance(a, str)
        ]
        print(f"✅ Procesando {len(abstracts_clean)} abstracts...")

        # -----------------------
        # 1️⃣ Conteo exacto de palabras clave
        # -----------------------
        frecuencias = np.zeros(
            (len(abstracts_clean), len(self.palabras_clave)), dtype=int
        )
        for i, abstract in enumerate(abstracts_clean):
            for j, palabra in enumerate(self.palabras_clave):
                try:
                    frecuencias[i, j] = len(
                        re.findall(r"\b" + re.escape(palabra) + r"\b", abstract)
                    )
                except re.error:
                    frecuencias[i, j] = 0

        total_palabra = frecuencias.sum(axis=0)

        # -----------------------
        # 2️⃣ TF-IDF (limitado al vocabulario de palabras clave)
        # -----------------------
        try:
            vectorizer = TfidfVectorizer(
                vocabulary=self.palabras_clave,
                ngram_range=self.ngram_range,
                stop_words="english",
            )
            tfidf_matrix = vectorizer.fit_transform(abstracts_clean)
            tfidf_array = tfidf_matrix.toarray()
            tfidf_total = tfidf_array.sum(axis=0)
        except ValueError:
            print("⚠️ Error en TF-IDF (posiblemente vocabulario vacío)")
            tfidf_total = np.zeros(len(self.palabras_clave))

        # -----------------------
        # 3️⃣ Score combinado (frecuencia + TF-IDF)
        # -----------------------
        max_count = max(total_palabra.max(), 1)
        max_tfidf = max(tfidf_total.max(), 1)
        score = (total_palabra / max_count) + (tfidf_total / max_tfidf)

        # -----------------------
        # 4️⃣ Top N palabras clave más relevantes
        # -----------------------
        indices_top = np.argsort(score)[::-1][:top_n]
        palabras_asociadas = [
            {
                "palabra": self.palabras_clave[i],
                "frecuencia": int(total_palabra[i]),
                "tfidf": float(tfidf_total[i]),
                "score": float(score[i]),
                "nueva": False,
            }
            for i in indices_top
        ]

        # -----------------------
        # 5️⃣ Detección de nuevas palabras relevantes en el corpus
        # -----------------------
        try:
            vectorizer_full = TfidfVectorizer(
                ngram_range=self.ngram_range,
                stop_words="english",
                max_features=5000,  # evitar consumo excesivo
            )
            tfidf_full = vectorizer_full.fit_transform(abstracts_clean)
            feature_names = vectorizer_full.get_feature_names_out()
            tfidf_sum = tfidf_full.toarray().sum(axis=0)

            top_indices_full = np.argsort(tfidf_sum)[::-1][: top_n * 2]
            nuevas = []
            for idx in top_indices_full:
                palabra = feature_names[idx]
                if palabra not in self.palabras_clave:
                    nuevas.append(
                        {
                            "palabra": palabra,
                            "frecuencia": sum(
                                a.lower().count(palabra) for a in abstracts_clean
                            ),
                            "tfidf": float(tfidf_sum[idx]),
                            "score": float(tfidf_sum[idx]),
                            "nueva": True,
                        }
                    )
                if len(nuevas) >= top_n:
                    break
        except Exception as e:
            print("⚠️ Error en detección de nuevas palabras:", e)
            nuevas = []

        # Combinar todas
        todas_palabras = palabras_asociadas + nuevas

        # -----------------------
        # 6️⃣ Calcular precisión
        # -----------------------
        palabras_sugeridas = [p["palabra"] for p in todas_palabras]
        palabras_correctas = set(self.palabras_clave)
        precision = (
            sum(1 for p in palabras_sugeridas if p.lower() in palabras_correctas)
            / len(palabras_sugeridas)
            if palabras_sugeridas
            else 0
        )

        return {"palabras_asociadas": todas_palabras, "precision": precision}


def abstractsVerification():
    """
    Recupera todos los abstracts desde los archivos procesados en parte2.functions.groupOfFiles()
    y devuelve una lista de textos limpios.
    """
    abstracts = []
    try:
        dictionaryAuxiliary = functions.groupOfFiles()
    except Exception as e:
        print("❌ Error al obtener archivos:", e)
        return []

    if not isinstance(dictionaryAuxiliary, list):
        print("⚠️ groupOfFiles() no devolvió una lista válida.")
        return []

    for element in dictionaryAuxiliary:
        if not isinstance(element, dict):
            continue
        abstract = element.get("abstract")
        if abstract and isinstance(abstract, str):
            abstracts.append(abstract)

    print(f"✅ Se obtuvieron {len(abstracts)} abstracts válidos.")
    return abstracts
