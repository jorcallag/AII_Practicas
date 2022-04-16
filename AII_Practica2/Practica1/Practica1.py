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
PAGINAS = 1 #n�mero de p�ginas

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def cargar():
    respuesta = messagebox.askyesno(title="Confirmar",message="Esta seguro que quiere recargar los datos. \nEsta operación puede ser lenta")
    if respuesta:
        almacenar_datos()
        listar_todo()    
        
def almacenar_datos():
    schem = Schema(categoria=TEXT(stored=True), titulo=TEXT(stored=True), enlace=TEXT(stored=True), descripcion=TEXT(stored=True), fecha=DATETIME(stored=True))
    
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    ix = create_in("Index", schema=schem)
    writer = ix.writer()
    i=0
    lista=extraer_noticias()
    for j in lista:
        writer.add_document(categoria=str(j[0]), titulo=str(j[1]), enlace=str(j[2]), descripcion=str(j[3]), fecha=j[3])   
        i+=1
    writer.commit()
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " noticias")    
    
def imprimir_lista(cursor):
    v = Toplevel()
    v.title("NOTICIAS")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row['titulo'])
        lb.insert(END,"    Categoría: "+ str(row['categoria']))
        lb.insert(END,"    Enlace: "+ str(row['enlace']))
        lb.insert(END,"    Descripción: "+ str(row['descripcion']))
        lb.insert(END,"    Fecha: "+ row['fecha'].strftime('%d/%m/%Y'))
        lb.insert(END,"\n\n")
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command = lb.yview)
    
def listar_todo():
    ix=open_dir(dirindex)
    with ix.searcher() as searcher:
        results = searcher.search(query.Every())
        imprimir_lista(results) 
    
def ventana_principal():       
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
    buscarmenu.add_command(label="Descripción", command=buscar_descripcion)
    buscarmenu.add_command(label="Fecha", command=buscar_fecha)
    buscarmenu.add_command(label="Categoría y Título", command=buscar_categoria)
    
    menubar.add_cascade(label="Buscar", menu=buscarmenu)
        
    root.config(menu=menubar)
    root.mainloop()  
        
    