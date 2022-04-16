#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import re, os, shutil
from datetime import datetime
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, NUMERIC, KEYWORD, ID, DATETIME
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser, query

dirindex="Index"
PAGINAS = 1 #número de páginas

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
    
def cargar():
    respuesta = messagebox.askyesno(title="Confirmar",message="Esta seguro que quiere recargar los datos. \nEsta operación puede ser lenta")
    if respuesta:
        almacenar_datos()
        
def extraer_peliculas():
    lista = []
    
    for p in range(1, PAGINAS+1):
        url = "https://www.elseptimoarte.net/estrenos/" + str(p)
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f, 'lxml')
    
        lista_link_peliculas = s.find("ul", class_="elements").find_all("li")

        for link_pelicula in lista_link_peliculas:
            f1 = urllib.request.urlopen("https://www.elseptimoarte.net/"+link_pelicula.a['href'])
            s1 = BeautifulSoup(f1, 'lxml')
            datos = s1.find("main", class_="informativo").find("section",class_="highlight").div.dl
            titulo_original = datos.find("dt",string="Título original").find_next_sibling("dd").string.strip()
            #si no tiene tÃ­tulo se pone el tÃ­tulo original
            if (datos.find("dt",string="Título")):
                titulo = datos.find("dt",string="Título").find_next_sibling("dd").string.strip()
            else:
                titulo = titulo_original      
            pais = "".join(datos.find("dt",string="País").find_next_sibling("dd").stripped_strings)
            fecha = datetime.strptime(datos.find("dt",string="Estreno en España").find_next_sibling("dd").string.strip(), '%d/%m/%Y')
            
            generos_director = s1.find("div",id="datos_pelicula")
            generos = "".join(generos_director.find("p",class_="categorias").stripped_strings)
            director = "".join(generos_director.find("p",class_="director").stripped_strings)        
    
            lista.append((titulo, titulo_original, pais, fecha, director, generos))
    
    return lista

def almacenar_datos():
    #define el esquema de la información
    schem = Schema(titulo=TEXT(stored=True), titulo_original=TEXT(stored=True), pais=TEXT(stored=True), fecha=DATETIME(stored=True), director=TEXT(stored=True), generos=TEXT(stored=True))
    
    #eliminamos el directorio del índice, si existe
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    #creamos el índice
    ix = create_in("Index", schema=schem)
    #creamos un writer para poder añadir documentos al indice
    writer = ix.writer()
    i=0
    lista=extraer_peliculas()
    for j in lista:
        #añade cada juego de la lista al índice
        writer.add_document(titulo=str(j[0]), titulo_original=str(j[1]), pais=str(j[2]), fecha=j[3], director=str(j[4]), generos=str(j[5]))    
        i+=1
    writer.commit()
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " peliculas")

def imprimir_lista(cursor):
    v = Toplevel()
    v.title("PELICULAS")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row['titulo'])
        lb.insert(END,"    Titulo original: "+ str(row['titulo_original']))
        lb.insert(END,"    Pais: "+ str(row['pais']))
        lb.insert(END,"    Fecha: "+ row['fecha'].strftime('%d-%m-%Y'))
        lb.insert(END,"    Director: "+ row['director'])
        lb.insert(END,"    Generos: "+ row['generos'])
        lb.insert(END,"\n\n")
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command = lb.yview)

def buscar_titulo():
    def listar_titulo(event):
            ix=open_dir(dirindex)   
            with ix.searcher() as searcher:
                myquery = MultifieldParser(["titulo"], ix.schema).parse(str(entry.get()))
                results = searcher.search(myquery)
                imprimir_lista(results)
            
    v = Toplevel()
    label = Label(v, text="Introduzca consulta sobre título: ")
    label.pack(side=LEFT)
    entry = Entry(v)
    entry.bind("<Return>", listar_titulo)
    entry.pack(side=LEFT)
    
    
def buscar_genero():
    def listar_genero(event):    
        with ix.searcher() as searcher:
            entrada = str(en.get().lower())
            #se busca como una frase porque hay temáticas con varias palabras
            query = QueryParser("generos", ix.schema).parse('"'+entrada+'"')
            results = searcher.search(query)
            imprimir_lista(results)
    
    v = Toplevel()
    v.title("Búsqueda por géneros")
    l = Label(v, text="Seleccione género a buscar:")
    l.pack(side=LEFT)
    
    ix=open_dir("Index")      
    with ix.searcher() as searcher:
        #lista de todas las temáticas disponibles en el campo de temáticas
        lista_tematicas = [i.decode('utf-8') for i in searcher.lexicon('generos')]
    
    en = Spinbox(v, values=lista_tematicas, state="readonly")
    en.bind("<Return>", listar_genero)
    en.pack(side=LEFT)        
    
    
def buscar_fecha():
    def listar_fecha(event):
            myquery='{'+ str(entry.get()) + ' TO]'
            ix=open_dir(dirindex)   
            try:
                with ix.searcher() as searcher:
                    query = QueryParser("fecha", ix.schema).parse(myquery)
                    results = searcher.search(query)
                    imprimir_lista(results)
            except:
                messagebox.showerror("ERROR", "Formato de fecha incorrecto")
            
    v = Toplevel()
    label = Label(v, text="Introduzca la fecha (AAAAMMDD): ")
    label.pack(side=LEFT)
    entry = Entry(v)
    entry.bind("<Return>", listar_fecha)
    entry.pack(side=LEFT)    
    

    
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
    buscarmenu.add_command(label="Descripción", command=buscar_titulo)
    buscarmenu.add_command(label="Fecha", command=buscar_genero)
    buscarmenu.add_command(label="Fecha", command=buscar_fecha)
    
    menubar.add_cascade(label="Categoría y título", menu=buscarmenu)
        
    root.config(menu=menubar)
    root.mainloop()

    

if __name__ == "__main__":
    ventana_principal()