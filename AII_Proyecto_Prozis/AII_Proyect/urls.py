from django.contrib import admin
from django.urls import path
from principal import views

urlpatterns = [
    path('',views.inicio),
    path('carga/',views.carga),
    path('articulos/', views.lista_articulos),
    ]
