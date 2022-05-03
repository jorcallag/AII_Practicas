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

dirindex="Index"
PAGINAS = 1  #numero de paginas

# lineas para evitar error SSL
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
        req = urllib.request.Request("http://www.prozis.com/es/es/alimentacion-saludable/q/page/"+str(p), headers={'User-Agent': 'Mozilla/5.0'})
        f = urllib.request.urlopen(req)
        s = BeautifulSoup(f,"lxml")
        
        l = s.find_all("div", class_= "data-groupi")

        for i in l:
            
            req1 = urllib.request.Request(i.a['href'], headers={'User-Agent': 'Mozilla/5.0'})
            f1 = urllib.request.urlopen("https://www.prozis.com/" + req1)
            s1 = BeautifulSoup(f1, 'lxml')
            l1 = s1.find('section',class_='product-item-section')
            l2 = s1.find('section',class_='pdp-tabs-section')
            
            nombre = l1.h1.string.strip()
            
            precio = l1.find('div',class_='product-page-price').string.strip()
            
            infoNutricional = l2.findAll('div',class_='nut-facts-list')
            valorEnergetico = infoNutricional[0].find('div', class_='val').string.strip()
            grasas = infoNutricional[1].find('div', class_='val').string.strip()
            grasasSaturadas = infoNutricional[2].find('div', class_='val').string.strip()
            hidratosDeCarbono = infoNutricional[3].find('div', class_='val').string.strip()
            azucares = infoNutricional[4].find('div', class_='val').string.strip()
            proteinas = infoNutricional[5].find('div', class_='val').string.strip()
            sal = infoNutricional[6].find('div', class_='val').string.strip()
            # ingredientes
            # advertencias
            # modoDeEmpleo
                      
            lista.append((nombre,precio,valorEnergetico,grasas,grasasSaturadas,hidratosDeCarbono,azucares,proteinas,sal))
        
    return lista


def imprimir_lista(cursor):
    v = Toplevel()
    v.title("Articulos Prozis")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row['nombre'])
        lb.insert(END,"    Precio: "+ str(row['precio']) + " €")
        lb.insert(END,"    Valor energetico: "+ row['valorEnergetico'])
        lb.insert(END,"    Grasas: "+ row['grasas'])
        lb.insert(END,"    Grasas saturadas: "+ row['grasasSaturadas'])
        lb.insert(END,"    Hidratos de carbono: "+ row['hidratosDeCarbono'])
        lb.insert(END,"    Azucares: "+ row['azucares'])
        lb.insert(END,"    Proteinas: "+ row['proteinas'])
        lb.insert(END,"    Sal: "+ row['sal'])
        lb.insert(END,"    Ingredientes: "+ row['ingredientes'])
        lb.insert(END,"    Advertencias: "+ row['advertencias'])
        lb.insert(END,"    Modo de empleo: "+ row['modoDeEmpleo'])
        lb.insert(END,"\n\n")
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command = lb.yview)

 
def almacenar_datos():
    #define el esquema de la información
    schem = Schema(nombre=TEXT(stored=True), precio=TEXT(stored=True))
    
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
        #añade cada juego de la lista al índice
        writer.add_document(titulo=str(j[0]), precio=str(j[1]), valorEnergetico=str(j[2]), grasas=str(j[3]), grasasSaturadas=str(j[3]), 
                            hidratosDeCarbono=str(j[4]), azucares=str(j[5]), proteinas=str(j[6]), sal=str(j[7]))    
        i+=1
    writer.commit()
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " articulos")          

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
    
    # buscarmenu = Menu(menubar, tearoff=0)
    # buscarmenu.add_command(label="Detalles", command=buscar_detalles)
    # buscarmenu.add_command(label="Temáticas", command=buscar_tematicas)
    # buscarmenu.add_command(label="Precio", command=buscar_precio)
    # buscarmenu.add_command(label="Jugadores", command=buscar_jugadores)
    
    # menubar.add_cascade(label="Buscar", menu=buscarmenu)
        
    root.config(menu=menubar)
    root.mainloop()

if __name__ == "__main__":
    ventana_principal()