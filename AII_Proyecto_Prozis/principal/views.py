#encoding:utf-8
from principal.models import Articulo
# from principal.forms import BusquedaPorFechaForm, BusquedaPorGeneroForm
from principal.populateDB import populateDB
from django.shortcuts import render, redirect

#carga los datos desde la web en la BD
def carga(request):
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            num_articulos = populateDB()
            mensaje="Se han almacenado: " + str(num_articulos) +" articulos"
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
       
    return render(request, 'confirmacion.html')

#muestra el número de articulos que hay en la BD
def inicio(request):
    num_articulos = Articulo.objects.all().count()
    return render(request,'inicio.html', {'num_articulos':num_articulos})

#muestra un listado con los datos de los articulos
def lista_articulos(request):
    articulos=Articulo.objects.all()
    return render(request,'articulos.html', {'articulos':articulos})
