#encoding:utf-8
from bs4 import BeautifulSoup
import urllib.request
import re, os, shutil

from main.models import Anime, Puntuacion, Genero
from main.populateDB import populate
from django.shortcuts import render, redirect
from main.forms import GeneroBusquedaForm, UsuarioFormatoBusquedaForm
from main.recommendations import  transformPrefs, getRecommendations
import shelve
from django.conf import settings

def cargaDB(request):
 
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            num_animes = populate()
            mensaje="Se han almacenado: " + str(num_animes) +" animes" 
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacionDB.html')

# Funcion que carga en el diccionario Prefs todas las puntuaciones de usuarios a animes. Tambien carga el diccionario inverso
# Serializa los resultados en dataRS.dat
def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataPractica3.dat")
    ratings = Puntuacion.objects.all()
    for ra in ratings:
        user = int(ra.idUsuario)
        itemid = int(ra.idAnime.idAnime)
        rating = float(ra.puntuacion)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf.close()

def recomendar_animes_usuario_RSusuario(request):
    formulario = UsuarioFormatoBusquedaForm()
    items = None

    if request.method=='POST':
        formulario = UsuarioFormatoBusquedaForm(request.POST)

        if formulario.is_valid():
            idUsuario=formulario.cleaned_data['idUsuario']
            formato=formulario.cleaned_data['formato']
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            rankings = getRecommendations(Prefs,int(idUsuario), formato)
            recomendadas= rankings[:2]
            animes = []
            puntuaciones = []
            for re in recomendadas:
                animes.append(Anime.objects.get(pk=re[1]))
                puntuaciones.append(re[0])
            items= zip(animes,puntuaciones)

    return render(request, 'recomendar_anime_usuarios.html', {'formulario':formulario, 'items':items, 'usuario':idUsuario, 'formato':formato, 'STATIC_URL':settings.STATIC_URL})

def inicio(request):
    num_animes = Anime.objects.all().count()        
    
    return render(request,'inicio.html', {'num_animes':num_animes})

#muestra un listado con los datos de los productos
def lista_animes(request):
    animes=Anime.objects.all()
    return render(request,'animes.html', {'animes':animes})

def buscar_anime_por_genero(request):
    formulario = GeneroBusquedaForm()
    animes = None
    
    if request.method=='POST':
        formulario = GeneroBusquedaForm(request.POST)      
        if formulario.is_valid():
            genero = Genero.objects.get(nombre=formulario.cleaned_data['genero'])
            animes = genero.anime_set.all()
            
    return render(request, 'busqueda_anime_genero.html', {'formulario':formulario, 'animes':animes})

