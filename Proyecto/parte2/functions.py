from os import path

import bibtexparser
from algorithmClassic import (cosineSimilary, distanceLCS, jaccadDistance,
                              levenshtein)
from models import ResulAlgorithm


def pathOfFiles(nameFile):
    pathDirectorie = path.abspath(
        "../DescargaApp/resources/Downloads/SAGE/IA/archivo_10_IA.bib"
    )
    full_path = path.join(pathDirectorie, nameFile)
    return full_path


def groupOfFiles(nameFile):
    filesGroup = []
    bibtextFileRead = bibtexparser.parse_file(pathOfFiles(nameFile))
    for fileEntries in bibtextFileRead.entries:
        libraryOfProduct = {}
        if "abstract" in fileEntries.fields_dict:
            libraryOfProduct["abstract"] = fileEntries.fields_dict["abstract"].value
        libraryOfProduct["key"] = fileEntries.key
        libraryOfProduct["title"] = fileEntries.fields_dict["title"].value
        libraryOfProduct["author"] = fileEntries.fields_dict["author"].value
        filesGroup.append(libraryOfProduct)
    return filesGroup


def functioGroupResultsLeven(groupFiles, count: int):
    groupResultLenvenshtein = []
    for indexGroupBy in range(0, count, 1):
        elementOneOfFile = groupFiles[indexGroupBy]
        elementTwoOfFile = groupFiles[indexGroupBy + 1]
        groupResultLenvenshtein.append(
            ResulAlgorithm(
                elementOneOfFile["key"],
                elementTwoOfFile["key"],
                levenshtein.levenshtein_iterative(
                    elementOneOfFile["abstract"], elementTwoOfFile["abstract"]
                ),
            )
        )
    return groupResultLenvenshtein


def functioGroupResultsDistanceLCS(groupFiles, count: int):
    groupResultDistanceLCS = []

    for indexGroupBy in range(0, count, 1):
        elementOneOfFile = groupFiles[indexGroupBy]
        elementTwoOfFile = groupFiles[indexGroupBy + 1]
        groupResultDistanceLCS.append(
            ResulAlgorithm(
                elementOneOfFile["key"],
                elementTwoOfFile["key"],
                distanceLCS.editDistanceWith2Ops(
                    elementOneOfFile["abstract"], elementTwoOfFile["abstract"]
                ),
            )
        )
    return groupResultDistanceLCS


def functioGroupResultsCosineSimilarity(groupFiles, count: int):
    groupResultsCosineSimilary = []
    for indexGroupFiles in range(0, count, 1):
        elementOneOfFile = groupFiles[indexGroupFiles]
        elementTwoOfFile = groupFiles[indexGroupFiles + 1]
        groupResultsCosineSimilary.append(
            ResulAlgorithm(
                elementOneOfFile["key"],
                elementTwoOfFile["key"],
                cosineSimilary.cosine_similarity_between_texts(
                    elementOneOfFile["abstract"], elementTwoOfFile["abstract"]
                ),
            )
        )
    return groupResultsCosineSimilary


def functionGroupResultsJaccad(groupFiles, count: int):
    groupResultsJaccad = []
    for indexGroupFiles in range(0, count, 1):
        elementOneOfFile = groupFiles[indexGroupFiles]
        elementTwoOfFile = groupFiles[indexGroupFiles]
        groupResultsJaccad.append(
            ResulAlgorithm(
                elementOneOfFile["key"],
                elementTwoOfFile["key"],
                jaccadDistance.jaccard_distance(
                    elementOneOfFile["abstract"], elementTwoOfFile["abstract"]
                ),
            )
        )
    return groupResultsJaccad
