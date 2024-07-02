"""
URL configuration for portal_inmo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from gestion.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', indice, name='indice'),
    path('registro/', registro, name='registro'),
    path('actualizar_usuario/', actualizar_usuario, name='actualizar_usuario'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('propiedades/', listar_propiedades, name='listar_propiedades'),
    path('propiedad/<int:propiedad_id>/solicitud_arriendo/', solicitud_arriendo, name='solicitud_arriendo'),
    path('publicar_propiedad/', publicar_propiedad, name='publicar_propiedad'),
    path('propiedad/<int:pk>/', detalle_propiedad, name='detalle_propiedad'),
    path('dashboard/', dashboard_propiedades, name='dashboard_propiedades'),
    path('propiedad/<int:pk>/editar/', editar_propiedad, name='editar_propiedad'),
    path('solicitudes/', solicitudes_arriendo, name='solicitudes_arriendo'),
    path('solicitud/<int:solicitud_id>/aceptar/', aceptar_solicitud, name='aceptar_solicitud'),
    path('solicitud/<int:solicitud_id>/rechazar/', rechazar_solicitud, name='rechazar_solicitud'),
]
