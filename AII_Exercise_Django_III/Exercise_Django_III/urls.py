from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
    path('',views.inicio),
    path('carga/',views.carga),
    path('usuarios/', views.usuarios),
    path('peliculasmejorpuntuadas/', views.peliculas_mejor_puntuadas),
    path('peliculaspora�o/', views.peliculas_por_a�o),
    path('peliculaspuntuadasporusuario/', views.peliculas_puntuadas_por_usuario),
    ]
