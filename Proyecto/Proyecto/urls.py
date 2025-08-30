"""
URL configuration for Proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from DescargaApp import views as descarga_views  # type: ignore


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', descarga_views.vistaPrincipal, name='buscar_termino'),
    path('buscando/', descarga_views.pantalla_carga, name='pantalla_carga'),
    path('api/estado/', descarga_views.obtener_estado, name='obtener_estado'),
    path('api/actualizar_estado/', descarga_views.actualizar_estado, name='actualizar_estado'),

]
