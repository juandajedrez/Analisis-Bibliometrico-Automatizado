import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from . import \
    functions  # asegúrate de que el módulo 'functions' existe y está bien importado


# Función auxiliar para procesar datos de entrada
def get_post_data(request):
    try:
        data = json.loads(request.body)
        dato = data.get("dato", None)
        if dato is None or dato == "":
            return None
        return int(dato)
    except Exception:
        return None


@csrf_exempt
def returnJacardi(request):
    if request.method == "POST":
        dato = get_post_data(request)
        if dato is None:
            return JsonResponse({"error": "Dato inválido o vacío"}, status=400)

        try:
            results = functions.functionGroupResultsJaccad(functions.pathOfFiles, dato)
            data = [
                {"key1": r.key1, "key2": r.key2, "distance": r.distance}
                for r in results
            ]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse(
                {"error": f"Error al ejecutar Jaccard: {str(e)}"}, status=500
            )

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def returnDistanceLCS(request):
    if request.method == "POST":
        dato = get_post_data(request)
        if dato is None:
            return JsonResponse({"error": "Dato inválido o vacío"}, status=400)

        try:
            results = functions.functioGroupResultsDistanceLCS(
                functions.pathOfFiles, int(dato)
            )
            data = [
                {"key1": r.key1, "key2": r.key2, "distance": r.distance}
                for r in results
            ]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse(
                {"error": f"Error al ejecutar LCS: {str(e)}"}, status=500
            )

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def returnCosin(request):
    if request.method == "POST":
        dato = get_post_data(request)
        if dato is None:
            return JsonResponse({"error": "Dato inválido o vacío"}, status=400)

        try:
            results = functions.functioGroupResultsCosineSimilarity(
                functions.pathOfFiles, int(dato)
            )
            data = [
                {"key1": r.key1, "key2": r.key2, "distance": r.distance}
                for r in results
            ]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse(
                {"error": f"Error al ejecutar Coseno: {str(e)}"}, status=500
            )

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def returnLeven(request):
    if request.method == "POST":
        dato = get_post_data(request)
        if dato is None:
            return JsonResponse({"error": "Dato inválido o vacío"}, status=400)

        try:
            results = functions.functioGroupResultsLeven(
                functions.pathOfFiles, int(dato)
            )
            data = [
                {"key1": r.key1, "key2": r.key2, "distance": r.distance}
                for r in results
            ]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse(
                {"error": f"Error al ejecutar Levenshtein: {str(e)}"}, status=500
            )

    return JsonResponse({"error": "Método no permitido"}, status=405)
