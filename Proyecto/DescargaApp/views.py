from django.shortcuts import render
from django.http import JsonResponse
from .scripts import run
from .scripts_folder.EstadoGlobal import estado_ieee, estado_sage

# Vista principal que carga el formulario de búsqueda en 'index.html'.
# Extrae el término ingresado por el usuario desde la URL (GET) y lo pasa al template.
def vistaPrincipal(request):
    termino = request.GET.get('termino', '').strip()  # Limpia espacios en blanco
    contexto = {
        'termino': termino,
    }
    return render(request, 'index.html', contexto)

# Vista que se activa tras enviar el término de búsqueda.
# Ejecuta el proceso de scraping con el término, limpia los estados anteriores y carga la pantalla de espera.
def pantalla_carga(request):
    termino = request.GET.get('termino', '').strip()
    run(termino)  # Llama al script principal que inicia el scraping
    estado_ieee.clear()  # Reinicia el estado para IEEE
    estado_sage.clear()  # Reinicia el estado para SAGE
    return render(request, 'carga.html', {'termino': termino})

# Vista que expone los estados actuales del scraping en formato JSON.
# Se usa para actualizar dinámicamente la interfaz con los datos de progreso.
def obtener_estados(request):
    return JsonResponse({
        'estado_ieee': estado_ieee.obtener_estado(),           # Estado general IEEE
        'estado_sage': estado_sage.obtener_estado(),           # Estado general SAGE
        'prueba_ieee': estado_ieee.obtener_prueba(),           # Última prueba realizada IEEE
        'prueba_sage': estado_sage.obtener_prueba(),           # Última prueba realizada SAGE
        'encontrados_ieee': estado_ieee.obtener_encontrados(), # Total encontrados IEEE
        'encontrados_sage': estado_sage.obtener_encontrados(), # Total encontrados SAGE
        'descargados_ieee': estado_ieee.obtener_descargados(), # Total descargados IEEE
        'descargados_sage': estado_sage.obtener_descargados()  # Total descargados SAGE
    })