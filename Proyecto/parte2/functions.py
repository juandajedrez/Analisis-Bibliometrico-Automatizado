from os import path

import bibtexparser

from .algorithmClassic import (cosineSimilary, distanceLCS, jaccadDistance,
                               levenshtein)
from .models import ResulAlgorithm


# Devuelve la ruta absoluta de un archivo .bib
def pathOfFiles():
    # return path.abspath("../DescargaApp/resources/Downloads/SAGE/IA/archivo_10_IA.bib")
    return "/home/karurosu/Documents/programming/python/projectsAlgorithm/Analisis-Bibliometrico-Automatizado/Proyecto/DescargaApp/resources/Downloads/SAGE/IA/archivo_10_IA.bib"


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
    for i in range(0, len(groupFiles) - 1):
        elementOne = groupFiles[i]
        elementTwo = groupFiles[i + 1]
        distance = jaccadDistance.jaccard_distance(
            elementOne["abstract"], elementTwo["abstract"]
        )

        groupResultJaccard.append(
            ResulAlgorithm(elementOne["key"], elementTwo["key"], distance)
        )

    return groupResultJaccard


# Función para LCS
def functionGroupResultsDistanceLCS(groupFiles, count: int):
    groupResultDistanceLCS = []
    for i in range(0, count - 1):
        elementOne = groupFiles[i]
        elementTwo = groupFiles[i + 1]

        result = distanceLCS.editDistanceWith2Ops(
            elementOne["abstract"], elementTwo["abstract"]
        )

        groupResultDistanceLCS.append(
            ResulAlgorithm(
                keyArticleOne=elementOne["key"],
                keyArticleTwo=elementTwo["key"],
                result=result,
            )
        )

    return groupResultDistanceLCS


# Función para Cosine Similarity
def functionGroupResultsCosineSimilarity(groupFiles, count: int):
    groupResultCosine = []
    for i in range(0, count - 1):
        elementOne = groupFiles[i]
        elementTwo = groupFiles[i + 1]

        distance = cosineSimilary.cosine_similarity_between_texts(
            elementOne["abstract"], elementTwo["abstract"]
        )

        groupResultCosine.append(
            ResulAlgorithm(
                keyArticleOne=elementOne["key"],
                keyArticleTwo=elementTwo["key"],
                result=distance,
            )
        )

    return groupResultCosine


# Función para Levenshtein
def functionGroupResultsLeven(groupFiles, count: int):
    groupResultLevenshtein = []
    for i in range(0, count - 1):
        elementOne = groupFiles[i]
        elementTwo = groupFiles[i + 1]

        distance = levenshtein.levenshtein_iterative(
            elementOne["abstract"], elementTwo["abstract"]
        )

        groupResultLevenshtein.append(
            ResulAlgorithm(
                keyArticleOne=elementOne["key"],
                keyArticleTwo=elementTwo["key"],
                result=distance,
            )
        )

    return groupResultLevenshtein
