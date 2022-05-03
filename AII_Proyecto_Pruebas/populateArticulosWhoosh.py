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

def cargar():
    respuesta = messagebox.askyesno(title="Confirmar",message="Esta seguro que quiere recargar los datos. \nEsta operación puede ser lenta")
    if respuesta:
        almacenar_datos()
        
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


def imprimir_lista(cursor):
    v = Toplevel()
    v.title("Articulos BrikoGeek")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row['titulo'])
        lb.insert(END,"    Autor: "+ str(row['autor']))
        lb.insert(END,"    Categoria: "+ str(row['categoria']))
        lb.insert(END,"    Imagen: "+ str(row['imagen']))
        lb.insert(END,"    Descripcion: "+ str(row['descripcion']))
        lb.insert(END,"\n\n")
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command = lb.yview)

 
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
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " articulos")
    
def buscar_titulo():
    def mostrar_lista(event):
        ix=open_dir("Index")
        with ix.searcher() as searcher:
            query = QueryParser("titulo", ix.schema).parse('"'+str(en.get())+'"')
            results = searcher.search(query,limit=10) #devuelve los 10 primeros
            imprimir_lista(results)
    
    v = Toplevel()
    v.title("Búsqueda por titulo")
    l = Label(v, text="Introduzca el titulo que desea buscar:")
    l.pack(side=LEFT)
    en = Entry(v, width=75)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    
def buscar_categoria():
    def mostrar_lista(event):    
        with ix.searcher() as searcher:
            entrada = str(en.get().lower())
            #se busca como una frase porque hay categoria con varias palabras
            query = QueryParser("categoria", ix.schema).parse('"'+entrada+'"')
            results = searcher.search(query)
            imprimir_lista(results)
    
    
    v = Toplevel()
    v.title("Búsqueda por categoria")
    l = Label(v, text="Seleccione la categoria que desea buscar:")
    l.pack(side=LEFT)
    
    ix=open_dir("Index")      
    with ix.searcher() as searcher:
        #lista de todas las categorias disponibles en el campo de categorias
        lista_tematicas = [i.decode('utf-8') for i in searcher.lexicon('categoria')]
    
    en = Spinbox(v, values=lista_tematicas, state="readonly")
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
          

def ventana_principal():      
    def listar_todo():
        ix=open_dir(dirindex)
        with ix.searcher() as searcher:
            results = searcher.search(query.Every())
            imprimir_lista(results) 
             
    root = Tk()
    root.geometry("150x100")

    menubar = Menu(root)
    
    datosmenu = Menu(menubar, tearoff=0)
    datosmenu.add_command(label="Cargar", command=almacenar_datos)
    datosmenu.add_command(label="Listar", command=listar_todo)
    datosmenu.add_separator()   
    datosmenu.add_command(label="Salir", command=root.quit)
    
    menubar.add_cascade(label="Datos", menu=datosmenu)
    
    buscarmenu = Menu(menubar, tearoff=0)
    buscarmenu.add_command(label="Titulo", command=buscar_titulo)
    buscarmenu.add_command(label="Categoria", command=buscar_categoria)
    
    menubar.add_cascade(label="Buscar", menu=buscarmenu)
        
    root.config(menu=menubar)
    root.mainloop()

    

if __name__ == "__main__":
    ventana_principal()