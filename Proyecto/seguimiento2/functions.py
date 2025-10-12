import grafo

from ..parte2.algorithmClassic import levenshtein
from ..parte2.functions import groupOfFiles


def getArrayOfDataBibTex():
    runArrayFilesOneLoop(groupOfFiles(""))


def runArrayFilesOneLoop(arrayFiles):
    for indexArrayFiles in range(0, len(arrayFiles) - 1, 1):
        grafo.addGraph(
            runArrayOfFiles(
                arrayFiles[indexArrayFiles], arrayFiles, indexArrayFiles + 1
            )
        )


def runArrayOfFiles(titleArticle, arrayFiles, index):
    auxliaryCountResult = 100
    auxiliaryArticle = {}
    for indexArrayFiles in range(index, len(arrayFiles), 1):
        auxiliaryResultLevenshtein = levenshtein.levenshtein_iterative(
            titleArticle, arrayFiles[indexArrayFiles]["title"]
        )
        if auxiliaryResultLevenshtein < auxliaryCountResult:
            auxiliaryArticle = arrayFiles[indexArrayFiles]
            auxliaryCountResult = auxiliaryResultLevenshtein
    return auxiliaryArticle
