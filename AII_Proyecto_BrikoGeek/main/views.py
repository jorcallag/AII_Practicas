#encoding:utf-8
from bs4 import BeautifulSoup
import urllib.request
import re, os, shutil

from main.models import Producto
from main.forms import BusquedaPorPrecioForm, BusquedaPorNombreForm
from main.populateProductosDB import populateDB
from django.shortcuts import render, redirect

from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, NUMERIC, KEYWORD, ID
from whoosh.qparser import QueryParser
from whoosh import qparser, query

dirindex="Index"
PAGINAS = 1 

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

#carga los datos desde la web en la BD
def cargaDB(request):
 
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            num_productos = populateDB()
            mensaje="Se han almacenado: " + str(num_productos) +" productos" 
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacionDB.html')

def cargaWhoosh(request):
 
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            num_articulos = almacenar_datos_whoosh()
            mensaje="Se han almacenado: " + str(num_articulos) +" articulos" 
            return render(request, 'cargaWhoosh.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacionWhoosh.html')

def inicio(request):
    num_productos = Producto.objects.all().count()
    
    ix=open_dir(dirindex)
    with ix.searcher() as searcher:
        results = searcher.search(query.Every())
        num_articulos = len(results)            
    
    return render(request,'inicio.html', {'num_productos':num_productos, 'num_articulos':num_articulos})

#muestra un listado con los datos de los productos
def lista_productos(request):
    productos=Producto.objects.all()
    return render(request,'productos.html', {'productos':productos})

def lista_articulos(request): #ERROR
    ix=open_dir(dirindex)
    with ix.searcher() as searcher:
        articulos = searcher.search(query.Every())
        print(len(articulos))
        
        return render(request,'articulos.html', {'articulos':articulos})

def buscar_productosporprecio(request):
    formulario = BusquedaPorPrecioForm()
    productos = None
    
    if request.method=='POST':
        formulario = BusquedaPorPrecioForm(request.POST)      
        if formulario.is_valid():
            productos = Producto.objects.filter(precio__lte=formulario.cleaned_data['precio'])
            
    return render(request, 'productosbusquedaporprecio.html', {'formulario':formulario, 'productos':productos})

def buscar_productospornombre(request):
    formulario = BusquedaPorNombreForm()
    productos = None
    
    if request.method=='POST':
        formulario = BusquedaPorNombreForm(request.POST)      
        if formulario.is_valid():
            productos = Producto.objects.filter(nombre__gte=formulario.cleaned_data['nombre'])
            
    return render(request, 'productosbusquedapornombre.html', {'formulario':formulario, 'productos':productos})




        
def extraer_articulos_whoosh():
    lista=[]
    
    for p in range(1,PAGINAS+1):
        url="https://blog.bricogeek.com/page/"+str(p)+"/"
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f,"lxml")      
        
        l = s.find_all("article", class_= "articulo")

        for i in l:
                        
            titulo = i.a.string.strip()
            infoPublicacion = i.find("span", itemprop="publisher")
            autor = infoPublicacion.find("strong", rel="author").string.strip()
            categoria = infoPublicacion.find("a").string.strip()
            
            # fecha = infoPublicacion.getText()
            # print(fecha)
            
            imagen = i.find("div", class_="articulo_img").img['src']
            enlace = "https://blog.bricogeek.com" + i.a['href']
            
            d1 = i.findAll("p")
            descripcion = ""
            for d in d1:
                    d = d.getText()
                    if d != "\n":
                        descripcion = descripcion + d
            descripcion = descripcion + ": " + enlace + "\n"    
            lista.append((titulo, autor, categoria, imagen, descripcion))
        
    return lista
 
def almacenar_datos_whoosh():
    #define el esquema de la información
    schem = Schema(titulo=TEXT(stored=True), autor=TEXT(stored=True), categoria=KEYWORD(stored=True,commas=True,lowercase=True), imagen=TEXT(stored=True), descripcion=TEXT(stored=True))
    
    #eliminamos el directorio del índice, si existe
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    #creamos el índice
    ix = create_in("Index", schema=schem)
    #creamos un writer para poder añadir documentos al indice
    writer = ix.writer()
    i=0
    lista=extraer_articulos_whoosh()
    for j in lista:
        #añade cada articulo de la lista al índice
        writer.add_document(titulo=str(j[0]), autor=str(j[1]), categoria=str(j[2]), imagen=str(j[3]), descripcion=str(j[4]))    
        i+=1
    writer.commit()
    
    return i
