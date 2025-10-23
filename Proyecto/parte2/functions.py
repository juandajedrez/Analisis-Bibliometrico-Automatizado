import os

import bibtexparser
from django.conf import settings

from .algorithmClassic import (cosineSimilary, distanceLCS, jaccadDistance,
                               levenshtein)
from .models import ResulAlgorithm


# Devuelve la ruta absoluta de un archivo .bib
def pathOfFiles():
    # return os.path.abspath("../Proyecto/DescargaApp/resources/Downloads/SAGE/IA/archivo_10_IA.bib")
    # return "/home/karurosu/Documents/programming/python/projectsAlgorithm/Analisis-Bibliometrico-Automatizado/Proyecto/DescargaApp/resources/Downloads/SAGE/IA/archivo_10_IA.bib"
    # return f"../DescargaApp/resources/Downloads/SAGE/IA/archivo_10_IA.bib"
    return os.path.join(
        settings.BASE_DIR, "DescargaApp/resources/Downloads/SAGE/IA/archivo_10_IA.bib"
    )


# Lee un archivo .bib y devuelve una lista de diccionarios con 'key' y 'abstract'
def groupOfFiles():
    filesGroup = []
    bibtexFileRead = bibtexparser.parse_file(pathOfFiles())
    for entry in bibtexFileRead.entries:
        libraryOfProduct = {}
        if "abstract" in entry.fields_dict:
            libraryOfProduct["abstract"] = entry.fields_dict["abstract"].value
        libraryOfProduct["key"] = entry.key
        filesGroup.append(libraryOfProduct)

    return filesGroup


# Función para Jaccard
def functionGroupResultsJaccard(groupFiles, count: int):
    groupResultJaccard = []
    i = 0
    # Mientras no se alcance el número de resultados deseados
    # y no se llegue al final de la lista
    while len(groupResultJaccard) != count and i < len(groupFiles) - 1:
        elementOne = groupFiles[i]
        elementTwo = groupFiles[i + 1]

        # Verificar que ambos tengan el campo 'abstract'
        if "abstract" not in elementOne or "abstract" not in elementTwo:
            i += 1
            continue  # Saltar este par y seguir con el siguiente

        # Calcular la distancia
        result = distanceLCS.editDistanceWith2Ops(
            elementOne["abstract"], elementTwo["abstract"]
        )

        groupResultJaccard.append(
            ResulAlgorithm(
                keyArticleOne=elementOne.get("key", "unknown"),
                keyArticleTwo=elementTwo.get("key", "unknown"),
                result=result,
            )
        )

        i += 1  # Avanzar al siguiente par

    return groupResultJaccard


# Función para LCS
def functionGroupResultsDistanceLCS(groupFiles, count: int):
    groupResultDistanceLCS = []
    i = 0

    # Mientras no se alcance el número de resultados deseados
    # y no se llegue al final de la lista
    while len(groupResultDistanceLCS) != count and i < len(groupFiles) - 1:
        elementOne = groupFiles[i]
        elementTwo = groupFiles[i + 1]

        # Verificar que ambos tengan el campo 'abstract'
        if "abstract" not in elementOne or "abstract" not in elementTwo:
            print(
                f"⚠️  Uno de los elementos no tiene 'abstract': "
                f"{elementOne.get('key')}, {elementTwo.get('key')}"
            )
            i += 1
            continue  # Saltar este par y seguir con el siguiente

        # Calcular la distancia
        result = distanceLCS.editDistanceWith2Ops(
            elementOne["abstract"], elementTwo["abstract"]
        )

        groupResultDistanceLCS.append(
            ResulAlgorithm(
                keyArticleOne=elementOne.get("key", "unknown"),
                keyArticleTwo=elementTwo.get("key", "unknown"),
                result=result,
            )
        )

        i += 1  # Avanzar al siguiente par

    return groupResultDistanceLCS


# Función para Cosine Similarity
def functionGroupResultsCosineSimilarity(groupFiles, count: int):
    groupResultCosine = []

    i = 0
    # Mientras no se alcance el número de resultados deseados
    # y no se llegue al final de la lista
    while len(groupResultCosine) != count and i < len(groupFiles) - 1:
        elementOne = groupFiles[i]
        elementTwo = groupFiles[i + 1]

        # Verificar que ambos tengan el campo 'abstract'
        if "abstract" not in elementOne or "abstract" not in elementTwo:
            print(
                f"⚠️  Uno de los elementos no tiene 'abstract': "
                f"{elementOne.get('key')}, {elementTwo.get('key')}"
            )
            i += 1
            continue  # Saltar este par y seguir con el siguiente

        # Calcular la distancia
        result = distanceLCS.editDistanceWith2Ops(
            elementOne["abstract"], elementTwo["abstract"]
        )

        groupResultCosine.append(
            ResulAlgorithm(
                keyArticleOne=elementOne.get("key", "unknown"),
                keyArticleTwo=elementTwo.get("key", "unknown"),
                result=result,
            )
        )

        i += 1  # Avanzar al siguiente par
    return groupResultCosine


# Función para Levenshtein
def functionGroupResultsLeven(groupFiles, count: int):
    groupResultLevenshtein = []
    i = 0
    # Mientras no se alcance el número de resultados deseados
    # y no se llegue al final de la lista
    while len(groupResultLevenshtein) != count and i < len(groupFiles) - 1:
        elementOne = groupFiles[i]
        elementTwo = groupFiles[i + 1]

        # Verificar que ambos tengan el campo 'abstract'
        if "abstract" not in elementOne or "abstract" not in elementTwo:
            print(
                f"⚠️  Uno de los elementos no tiene 'abstract': "
                f"{elementOne.get('key')}, {elementTwo.get('key')}"
            )
            i += 1
            continue  # Saltar este par y seguir con el siguiente

        # Calcular la distancia
        result = distanceLCS.editDistanceWith2Ops(
            elementOne["abstract"], elementTwo["abstract"]
        )

        groupResultLevenshtein.append(
            ResulAlgorithm(
                keyArticleOne=elementOne.get("key", "unknown"),
                keyArticleTwo=elementTwo.get("key", "unknown"),
                result=result,
            )
        )

        i += 1  # Avanzar al siguiente par

    return groupResultLevenshtein
