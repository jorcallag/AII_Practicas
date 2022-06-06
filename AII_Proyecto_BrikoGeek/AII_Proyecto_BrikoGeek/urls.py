
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.inicio),
    path('cargaDB/',views.cargaDB),
    path('productos/', views.lista_productos),
    path('buscar_productosporprecio/', views.buscar_productosporprecio),
    path('buscar_productospornombre/', views.buscar_productospornombre),
    
    path('cargaWhoosh/',views.cargaWhoosh),
    path('articulos/',views.lista_articulos),
    path('buscar_articulosporcategoria/', views.buscar_articulosporcategoria),
    path('buscar_articulosportitulo/', views.buscar_articulosportitulo)
    ]
