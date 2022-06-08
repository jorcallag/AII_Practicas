#encoding:utf-8
from bs4 import BeautifulSoup
import urllib.request
import re, os, shutil

from main.models import Producto
from main.forms import BusquedaPorPrecioForm, BusquedaPorNombreForm, BusquedaPorCategoriaForm, BusquedaPorTituloForm
from main.populateProductosDB import populateDB
from django.shortcuts import render, redirect

from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, NUMERIC, KEYWORD, ID
from whoosh.qparser import QueryParser
from whoosh import qparser, query
from django.template.context_processors import request

dirindex="Index"
PAGINAS = 100

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

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

def lista_productos(request):
    productos=Producto.objects.all()
    return render(request,'productos.html', {'productos':productos})

def lista_articulos(request):
    ix=open_dir(dirindex)
    with ix.searcher() as searcher:
        articulos = searcher.search(query.Every(), limit=1000)
        
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
            productos = Producto.objects.filter(nombre__contains=formulario.cleaned_data['nombre'])
            
    return render(request, 'productosbusquedapornombre.html', {'formulario':formulario, 'productos':productos})

def buscar_articulosporcategoria(request):
    formulario = BusquedaPorCategoriaForm()
    articulos = None
    lista = []
    
    if request.method=='POST':
        formulario = BusquedaPorCategoriaForm(request.POST)      
        if formulario.is_valid():
            ix=open_dir(dirindex)
            with ix.searcher() as searcher:
                query = QueryParser("categoria", ix.schema).parse(formulario.cleaned_data['categoria'])            
                articulos = searcher.search(query, limit=1000)
                
                for r in articulos:
                    titulo = r.values()[5]
                    autor = r.values()[0] 
                    categoria = r.values()[1] 
                    imagen = r.values()[4] 
                    descripcion = r.values()[2] 
                    enlace = r.values()[3]
                    lista.append([titulo, autor, categoria, imagen, descripcion, enlace])
    
    return render(request, 'articulosbusquedaporcategoria.html', {'formulario':formulario, 'articulos':lista})


def buscar_articulosportitulo(request):
    formulario = BusquedaPorTituloForm()
    articulos = None
    lista = []
    
    if request.method=='POST':
        formulario = BusquedaPorTituloForm(request.POST)      
        if formulario.is_valid():
            ix=open_dir("Index")
            with ix.searcher() as searcher:
                query = QueryParser("titulo", ix.schema).parse(formulario.cleaned_data['titulo'])
                articulos = searcher.search(query, limit=1000)
                
                for r in articulos:
                    titulo = r.values()[5]
                    autor = r.values()[0] 
                    categoria = r.values()[1] 
                    imagen = r.values()[4] 
                    descripcion = r.values()[2] 
                    enlace = r.values()[3]
                    lista.append([titulo, autor, categoria, imagen, descripcion, enlace])
    
    return render(request, 'articulosbusquedaportitulo.html', {'formulario':formulario, 'articulos':lista})
                
def extraer_articulos_whoosh():
    lista=[]
    
    for p in range(1,PAGINAS+1):
        url="https://blog.bricogeek.com/page/"+str(p)
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f,"lxml")      
        
        l = s.find_all("article", class_= "articulo")

        for i in l:
                        
            titulo = i.a.string.strip()
            infoPublicacion = i.find("span", itemprop="publisher")
            autor = infoPublicacion.find("strong", rel="author").string.strip()
            categoria = infoPublicacion.find("a").string.strip()
            
            imagen = i.find("div", class_="articulo_img").img['src']
            enlace = "https://blog.bricogeek.com" + i.a['href']
            
            d1 = i.findAll("p")
            descripcion = ""
            for d in d1:
                    d = d.getText()
                    if d != "\n":
                        descripcion = descripcion + d
            descripcion = descripcion + ":"
            lista.append((titulo, autor, categoria, imagen, descripcion, enlace))
        
    return lista
 
def almacenar_datos_whoosh():
    schem = Schema(titulo=TEXT(stored=True), autor=KEYWORD(stored=True,commas=True,lowercase=True), categoria=KEYWORD(stored=True,commas=True,lowercase=True), imagen=TEXT(stored=True), descripcion=TEXT(stored=True), enlace=TEXT(stored=True))
    
    #if os.path.exists("Index"):
    #    shutil.rmtree("Index")
    #os.mkdir("Index")
    
    ix = create_in("Index", schema=schem)
    writer = ix.writer()
    i=0
    lista=extraer_articulos_whoosh()
    for j in lista:
        writer.add_document(titulo=str(j[0]), autor=str(j[1]), categoria=str(j[2]), imagen=str(j[3]), descripcion=str(j[4]), enlace=str(j[5]))    
        i+=1
    writer.commit()
    
    return i
