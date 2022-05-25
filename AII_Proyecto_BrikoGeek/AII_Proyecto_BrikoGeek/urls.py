"""AII_Proyecto_BrikoGeek URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.inicio),
    path('cargaDB/',views.cargaDB),
    path('productos/', views.lista_productos),
    path('buscar_productosporprecio/', views.buscar_productosporprecio),
    path('buscar_productospornombre/', views.buscar_productospornombre),
    
    path('cargaWhoosh/',views.cargaWhoosh),
    path('articulos/',views.lista_articulos)
    ]
