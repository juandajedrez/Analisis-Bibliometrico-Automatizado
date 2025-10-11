import re
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class KeywordAnalyzerComplete:
    def __init__(self, palabras_clave, ngram_range=(1, 3)):
        """
        palabras_clave: lista de palabras o frases clave
        ngram_range: rango de n-grams para detectar frases en TF-IDF
        """
        self.palabras_clave = palabras_clave
        self.ngram_range = ngram_range

    def limpiar_texto(self, texto):
        """Limpia el texto: minúsculas y elimina puntuación"""
        return re.sub(r"[^\w\s-]", "", texto.lower())

    def analizar(self, abstracts, top_n=15):
        # Limpiar abstracts
        abstracts_clean = [self.limpiar_texto(a) for a in abstracts]

        # -----------------------
        # 1️⃣ Conteo exacto
        # -----------------------
        frecuencias = np.zeros(
            (len(abstracts_clean), len(self.palabras_clave)), dtype=int
        )
        for i, abstract in enumerate(abstracts_clean):
            for j, palabra in enumerate(self.palabras_clave):
                frecuencias[i, j] = len(
                    re.findall(r"\b" + re.escape(palabra.lower()) + r"\b", abstract)
                )
        total_palabra = frecuencias.sum(axis=0)

        # -----------------------
        # 2️⃣ TF-IDF para palabras clave
        # -----------------------
        vectorizer = TfidfVectorizer(
            vocabulary=[p.lower() for p in self.palabras_clave],
            ngram_range=self.ngram_range,
        )
        tfidf_matrix = vectorizer.fit_transform(abstracts_clean)
        tfidf_array = tfidf_matrix.toarray()  # pyright: ignore
        tfidf_total = tfidf_array.sum(axis=0)

        # -----------------------
        # 3️⃣ Score combinado (frecuencia + TF-IDF)
        # -----------------------
        max_count = total_palabra.max() if total_palabra.max() > 0 else 1
        max_tfidf = tfidf_total.max() if tfidf_total.max() > 0 else 1
        score = (total_palabra / max_count) + (tfidf_total / max_tfidf)

        # -----------------------
        # 4️⃣ Top N palabras clave + nuevas palabras
        # -----------------------
        # Palabras clave más relevantes
        indices_top = np.argsort(score)[::-1][:top_n]
        palabras_asociadas = [
            {
                "palabra": self.palabras_clave[i],
                "frecuencia": total_palabra[i],
                "tfidf": tfidf_total[i],
                "score": score[i],
                "nueva": False,
            }
            for i in indices_top
        ]

        # -----------------------
        # 5️⃣ Detección de nuevas palabras
        # -----------------------
        # Usamos TF-IDF de todo el corpus (sin limitar a vocabulario)
        vectorizer_full = TfidfVectorizer(
            ngram_range=self.ngram_range, stop_words="english"
        )
        tfidf_full = vectorizer_full.fit_transform(abstracts_clean)
        feature_names = vectorizer_full.get_feature_names_out()
        tfidf_sum = tfidf_full.toarray().sum(axis=0)  # pyright: ignore

        # Seleccionar top N palabras del corpus completo
        top_indices_full = np.argsort(tfidf_sum)[::-1][
            : top_n * 2
        ]  # tomamos más para asegurar inclusión
        nuevas = []
        for idx in top_indices_full:
            palabra = feature_names[idx]
            if palabra not in [p.lower() for p in self.palabras_clave]:
                nuevas.append(
                    {
                        "palabra": palabra,
                        "tfidf": tfidf_sum[idx],
                        "frecuencia": sum(
                            [
                                abstract.lower().count(palabra)  # pyright:ignore
                                for abstract in abstracts_clean
                            ]
                        ),
                        "score": tfidf_sum[idx],  # usar TF-IDF como score
                        "nueva": True,
                    }
                )
            if len(nuevas) >= top_n:
                break

        # Combinar palabras clave + nuevas palabras
        todas_palabras = palabras_asociadas + nuevas

        # -----------------------
        # 6️⃣ Precisión de palabras clave
        # -----------------------
        palabras_sugeridas = [p["palabra"] for p in todas_palabras]
        palabras_correctas = set([p.lower() for p in self.palabras_clave])
        precision = sum(
            [1 for p in palabras_sugeridas if p.lower() in palabras_correctas]
        ) / len(palabras_sugeridas)

        return {
            "frecuencias_por_abstract": frecuencias,
            "total_por_palabra": total_palabra,
            "palabras_asociadas": todas_palabras,
            "precision": precision,
        }
