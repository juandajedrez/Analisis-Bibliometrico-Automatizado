import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .functions import KeywordAnalyzerComplete, abstractsVerification
from .library import concepts_of_generative_ai_in_education


# 🔹 Endpoint que procesa el análisis
@csrf_exempt
def analizar_keywords(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            palabras_clave = concepts_of_generative_ai_in_education
            top_n = data.get("top_n", 15)

            if not palabras_clave:
                return JsonResponse(
                    {"error": "Debe incluir 'palabras_clave'."}, status=400
                )

            abstracts = abstractsVerification()
            analizador = KeywordAnalyzerComplete(palabras_clave)
            resultado = analizador.analizar(abstracts, top_n=top_n)

            return JsonResponse(
                resultado, safe=False, json_dumps_params={"ensure_ascii": False}
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)
