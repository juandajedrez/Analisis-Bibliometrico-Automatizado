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

from DescargaApp import views as descarga_views  # type: ignore
from django.contrib import admin
from django.urls import path
from parte2 import views as views_algorithm
from parte3 import views as analizar_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", descarga_views.vistaPrincipal, name="buscar_termino"),
    path("buscando/", descarga_views.pantalla_carga, name="pantalla_carga"),
    path("api/estado/", descarga_views.obtener_estados, name="obtener_estado"),
    path("jacardi", views_algorithm.returnJacardi, name="jacardi"),
    path("lcs", views_algorithm.returnDistanceLCS, name="lcs"),
    path("cosen", views_algorithm.returnCosin, name="cosin"),
    path("leven", views_algorithm.returnLeven, name="leven"),
    path("order/ready", descarga_views.mostrar_html, name="Mostrar html"),
    path("analizer", analizar_views.analizar_keywords, name="analizador keywords"),
    path("analizer/view", descarga_views.mostrar_analizador, name="view analizer"),    
    path('requerimiento4/', views.generate_dendograma_view,name="generate_dendograma_view"),
    path('dendrogram/<str:tipo>/', views.dendrogram_detail, name='dendrogram_detail'),
    path('requerimiento5/',views.generate_visuals_view, name="generate_visuals_view")
]
