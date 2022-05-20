#encoding:utf-8
from main.models import Producto
from main.forms import BusquedaPorPrecioForm, BusquedaPorNombreForm
from main.populateProductosDB import populateDB
from django.shortcuts import render, redirect

#carga los datos desde la web en la BD
def carga(request):
 
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            num_productos = populateDB()
            mensaje="Se han almacenado: " + str(num_productos) +" productos"
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')

#muestra el número de productos que hay en la BD
def inicio(request):
    num_productos=Producto.objects.all().count()
    return render(request,'inicio.html', {'num_productos':num_productos})

#muestra un listado con los datos de los productos
def lista_productos(request):
    productos=Producto.objects.all()
    return render(request,'productos.html', {'productos':productos})

def buscar_productosporprecio(request):
    formulario = BusquedaPorPrecioForm()
    productos = None
    
    if request.method=='POST':
        formulario = BusquedaPorPrecioForm(request.POST)      
        if formulario.is_valid():
            productos = Producto.objects.filter(precio__lte=formulario.cleaned_data['precio'])
            
    return render(request, 'peliculasbusquedaporprecio.html', {'formulario':formulario, 'productos':productos})

def buscar_productospornombre(request):
    formulario = BusquedaPorNombreForm()
    productos = None
    
    if request.method=='POST':
        formulario = BusquedaPorNombreForm(request.POST)      
        if formulario.is_valid():
            productos = Producto.objects.filter(nombre__gte=formulario.cleaned_data['nombre'])
            
    return render(request, 'peliculasbusquedapornombre.html', {'formulario':formulario, 'productos':productos})


