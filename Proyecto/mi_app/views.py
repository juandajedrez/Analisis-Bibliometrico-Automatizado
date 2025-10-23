from django.shortcuts import render
import os
from django.templatetags.static import static
from pathlib import Path
from django.http import FileResponse
from django.conf import settings


# Create your views here.
from django.http import HttpResponse
from .scripts import generate_dendograma, generate_visuals

def hola(request):
# Vista principal que carga el formulario de búsqueda en 'index.html'.
# Extrae el término ingresado por el usuario desde la URL (GET) y lo pasa al template.
    return render(request, "prueba.html")

def generate_dendograma_view(request):
    text = generate_dendograma()
    html_text = text.replace('\n', '<br>')
    return render(request,"clusteringResult.html",{"result" : html_text})


def dendrogram_detail(request, tipo):
    filename = f'dendrogram_{tipo}.png'
    filepath = os.path.join(settings.BASE_DIR,'mi_app','static', 'mi_app', 'outputs', filename)
    print(filepath)

    # Verificar que la imagen existe
    if not os.path.exists(filepath):
        return HttpResponse("error")

    image_url = static(f'mi_app/outputs/{filename}')
    print (image_url)
    return render(request, 'dendrogram_detail.html', {'image_url': image_url})

def generate_visuals_view(request):
    generate_visuals()

    # Ruta absoluta al archivo
    file_path = os.path.join(settings.BASE_DIR, "mi_app/static/mi_app/imagenes/visualizaciones.pdf")

    
    # Devuelve el archivo como respuesta para descarga
    return FileResponse(open(file_path, "rb"), as_attachment=True, filename="visualizaciones.pdf")
    
    
