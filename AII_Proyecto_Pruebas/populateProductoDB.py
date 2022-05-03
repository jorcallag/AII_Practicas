#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import re, os, shutil
import sqlite3

PAGINAS = 1

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def cargar():
    respuesta = messagebox.askyesno(title="Confirmar",message="Esta seguro que quiere recargar los datos. \nEsta operaci�n puede ser lenta")
    if respuesta:
        almacenar_datos()
        
def extraer_productos():
    lista=[]
    
    for p in range(1,PAGINAS+1):
        url="https://tienda.bricogeek.com/5-arduino?p="+str(p)
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f,"lxml")      
        
        l = s.find_all("li", class_= "ajax_block_product")

        for i in l:
                        
            nombre = i.find("meta", itemprop= "name")["content"]
            print(nombre)
            imagen = i.find("meta", itemprop= "image")["content"]
            precio = i.find("meta", itemprop= "lowPrice")["content"]
            url1 = i.find("a", class_= "product_img_link")["href"]
            f1 = urllib.request.urlopen(url1)
            s1 = BeautifulSoup(f1, 'lxml')
            
            referencia = s1.find("span", itemprop= "sku").string.strip()
            descripcion = s1.find("div", id= "short_description_content").getText();
            
            # d1 = s1.findAll("div", class_= "rte")
            # descripcion = ""
            # for d in d1:
            #         d = d.getText()
            #         if d != "\n":
            #             descripcion = descripcion + d
            
            lista.append((nombre, imagen, referencia, precio, descripcion))
        
    return lista


def imprimir_lista(cursor):
    v = Toplevel()
    v.title("Productos BrikoGeek")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,"    Imagen: "+ str(row[1]))
        lb.insert(END,"    Referencia: "+ str(row[2]))
        lb.insert(END,"    Precio: "+ str(row[3]) + "€")
        lb.insert(END,"    Descripcion: "+ str(row[4]))
        lb.insert(END,"\n\n")
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command = lb.yview)

 
def almacenar_datos():
    conn = sqlite3.connect('productos.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS PRODUCTOS") 
    conn.execute('''CREATE TABLE PRODUCTOS
       (NOMBRE        TEXT    NOT NULL,
       IMAGEN          TEXT    ,
       REFERENCIA        TEXT    ,
       PRECIO         FLOAT    ,
       DESCRIPCION        TEXT);''')

    for i in extraer_productos():              
        conn.execute("""INSERT INTO PRODUCTOS VALUES (?,?,?,?,?)""",i)
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM PRODUCTOS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()     
    
def buscar_precio():
    def listar_todo(event):
            conn = sqlite3.connect('productos.db')
            conn.text_factory = str
            cursor = conn.execute("SELECT * FROM PRODUCTOS WHERE PRECIO <= ? ORDER BY PRECIO", (str(entry.get()),))
            conn.close
            imprimir_lista(cursor)
    ventana = Toplevel()
    label = Label(ventana, text="Indique el precio máximo: ")
    label.pack(side=LEFT)
    entry = Entry(ventana)
    entry.bind("<Return>", listar_todo)
    entry.pack(side=LEFT)
    
def buscar_nombre():  
    def listar_todo(event):
            conn = sqlite3.connect('productos.db')
            conn.text_factory = str
            cursor = conn.execute("SELECT * FROM PRODUCTOS WHERE NOMBRE LIKE '%" + str(entry.get()) + "%'")
            conn.close
            imprimir_lista(cursor)   
    
    ventana = Toplevel()
    label = Label(ventana,text="Introduzca nombre del producto: ")
    label.pack(side=LEFT)
    entry = Entry(ventana)
    entry.bind("<Return>", listar_todo)
    entry.pack(side=LEFT)     

def ventana_principal():      
    def listar_todo():
        conn = sqlite3.connect('productos.db')
        conn.text_factory = str  
        cursor = conn.execute("SELECT * FROM PRODUCTOS")
        imprimir_lista(cursor)
        conn.close()
             
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
    buscarmenu.add_command(label="Precio", command=buscar_precio)
    buscarmenu.add_command(label="Nombre", command=buscar_nombre)
    
    menubar.add_cascade(label="Buscar", menu=buscarmenu)
        
    root.config(menu=menubar)
    root.mainloop()

    

if __name__ == "__main__":
    ventana_principal()