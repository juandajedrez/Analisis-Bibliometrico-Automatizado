from django.shortcuts import render

# Create your views here.
def vistaPrincipal(request):
    termino = request.GET.get('termino', '').strip()

    # Puedes hacer algo con el término, por ejemplo, pasarlo a la plantilla
    contexto = {
        'termino': termino,
        # Puedes agregar más datos si lo necesitas
    }

    return render(request, 'index.html', contexto)

def pantalla_carga(request):
    termino = request.GET.get('termino', '').strip()
    return render(request, 'carga.html', {'termino': termino})

# views.py
from django.http import JsonResponse

estado_actual = "Iniciando..."

def actualizar_estado(request):
    global estado_actual
    nuevo_estado = request.GET.get('estado', '')
    if nuevo_estado:
        estado_actual = nuevo_estado
    return JsonResponse({'estado': estado_actual})

def obtener_estado(request):
    return JsonResponse({'estado': estado_actual})


