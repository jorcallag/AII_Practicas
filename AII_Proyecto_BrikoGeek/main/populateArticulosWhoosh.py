#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import re, os, shutil
from datetime import datetime
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, NUMERIC, KEYWORD, ID
from whoosh.qparser import QueryParser
from whoosh import qparser, query
from distutils.log import info
from enum import auto

dirindex="Index"
PAGINAS = 1 

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
        
def extraer_articulos():
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
 
def almacenar_datos():
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
    lista=extraer_articulos()
    for j in lista:
        #añade cada articulo de la lista al índice
        writer.add_document(titulo=str(j[0]), autor=str(j[1]), categoria=str(j[2]), imagen=str(j[3]), descripcion=str(j[4]))    
        i+=1
    writer.commit()
    
    return i
