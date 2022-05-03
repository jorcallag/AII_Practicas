from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
    path('',views.inicio),
    path('carga/',views.carga),
    path('usuarios/', views.usuarios),
    path('peliculasmejorpuntuadas/', views.peliculas_mejor_puntuadas),
    path('peliculasporaño/', views.peliculas_por_año),
    path('peliculaspuntuadasporusuario/', views.peliculas_puntuadas_por_usuario),
    ]
