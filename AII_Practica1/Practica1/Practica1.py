#Joaquin Almarcha Conejero
#Enrique Chamber Gonzalez de Quevedo
#Jorge Luis Calderon Laguna

#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3
import re
import lxml
from datetime import datetime
from numpy.f2py.capi_maps import getstrlength
import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

PAGINAS = 4

# lineas para evitar error SSL
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def extraer_eventos():
    lista=[]
    
    for p in range(1,PAGINAS+1):
        req = urllib.request.Request("https://sevilla.cosasdecome.es/eventos/filtrar?pg=1",
                    headers={'User-Agent': 'Mozilla/5.0'})
        f = urllib.request.urlopen(req)
        s = BeautifulSoup(f, 'lxml')

        l = s.find_all("article", class_= "post-summary")

        for i in l:
            articulo = i.find("div",class_="post-details")
            
            titulo = articulo.a.string.strip()
            print(titulo)
            
            info = articulo.find("div",class_="post-infopost")

            c = info.find("div",class_="categoria")
            if c:
                categoria = c.find("div",class_="value").a.string
                if " y " in categoria:
                    categoria = categoria.replace(' y ',',').strip().split(",")
                    cat1 = categoria[0]
                    cat2 = categoria[1]
                else:
                    cat1 = categoria.strip()
                    cat2 = "Desconocida"
            else:
                cat1 = "Desconocida"
                cat2 = "Desconocida"
            
            print(cat1)
            print(cat2)
            
            f1 = urllib.request.urlopen(i.a['href'])
            j = BeautifulSoup(f1,"lxml")
            
            fechas = j.find("div",class_="fechas").find("div", class_="value").text
            if fechas:
                if " al " in fechas:
                    fechas = fechas.replace(' al ',',').string.split(",")
                    fecha_inicial = datetime.strptime(fechas[0].strip(), '%d/%m/%Y')
                    fecha_final = datetime.strptime(fechas[1].strip(), '%d/%m/%Y')
                else:
                    print(fechas)
                    fecha_inicial = datetime.strptime(fechas.strip(), '%d/%m/%Y')
                    fecha_final = ""
            else:
                    fecha_inicial = ""
                    fecha_final = ""
            
            direccion = j.find("div",class_="direccion")
            if direccion:
                direccion = direccion.find("div", class_="value").string
            else:
                direccion = "Desconocida"
            print(direccion)
                
            lugar = j.find("div",class_="lugar")
            if lugar:
                lugar = lugar.find("div", class_="value").p.string
            else:
                lugar = "Desconocido"
            print(lugar)
            
            poblacion = j.find("div",class_="poblacion")
            if poblacion:
                poblacion = poblacion.find("div", class_="value").a.string
            else:
                poblacion = "Desconocida"
            print(poblacion)
            
            #horario = re.compile("\d+:\d+").search(j.find("div",class_="hora").find("div", class_="value").i.string.strip()).group()
            horario = ""
          
            lista.append((titulo,lugar,direccion,poblacion,fecha_inicial,fecha_final,horario,cat1,cat2))
        
    return lista
 
def almacenar_bd():
    conn = sqlite3.connect('catas.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS CATA") 
    conn.execute('''CREATE TABLE CATA
       (TITULO        TEXT    NOT NULL,
       lUGAR          TEXT    ,
       DIRECCION         TEXT    ,
       POBLACION        TEXT    ,
       FECHA_INICIAL      DATE    ,
       FECHA_FINAL      DATE    ,
       HORARIO    TEXT    ,
       CATEGORIA1    TEXT    ,
       CATEGORIA2    TEXT    );''')
    

    for i in extraer_eventos():              
        conn.execute("""INSERT INTO CATA VALUES (?,?,?,?,?,?,?,?,?)""",i)
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM CATA")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
  
def buscar_por_celebracion():  
    def listar(event):
            conn = sqlite3.connect('catas.db')
            conn.text_factory = str
            fecha = datetime.strptime(str(entry.get()),"%d de %B de %Y")
            cursor = conn.execute("SELECT TITULO, LUGAR, DIRECCION, POBLACION, FECHA as CONCAT(FECHA_INICIAL, ' - ', FECHA_FINAL), HORARIO, CATEGORIA FROM CATA WHERE FECHAINICIAL >= ? AND FECHAFINAL <= ?", (fecha,fecha))
            conn.close
            listar_catas(cursor)
    v = Toplevel()
    label = Label(v, text="Introduzca la fecha (dd de Mes de aaaa) ")
    label.pack(side=LEFT)
    entry = Entry(v)
    entry.bind("<Return>", listar)
    entry.pack(side=LEFT)



def buscar_por_categoria():
    def listar(event):
            conn = sqlite3.connect('catas.db')
            conn.text_factory = str
            cursor = conn.execute("SELECT TITULO, LUGAR, DIRECCION, POBLACION, FECHA_INICIAL, FECHA_FINAL, HORARIO, CATEGORIA1, CATEGORIA2 FROM CATA WHERE CATEGORIA1 = '" + str(entry.get()) + "' OR CATEGORIA2 = '" + str(entry.get()) + "'")
            conn.close
            listar_catas(cursor)

    conn = sqlite3.connect('catas.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT DISTINCT CATEGORIA1 FROM (SELECT * FROM (SELECT DISTINCT CATEGORIA1 FROM CATA) as TB1 UNION (SELECT DISTINCT CATEGORIA2 FROM CATA))")
    categorias = [d[0] for d in cursor]


    ventana = Toplevel()
    label = Label(ventana,text="Seleccione una Categoría: ")
    label.pack(side=LEFT)
    entry = Spinbox(ventana, width= 30, values=categorias)
    entry.bind("<Return>", listar)
    entry.pack(side=LEFT)

    conn.close



def listar_catas(cursor):      
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        fecha = str(row[3])
        if(getstrlength(str(row[4])) > 1 & str(row[4]) != '00/00/0000'): fecha += ' - ' + str(row[4])
        categoria = str(row[6])
        if(getstrlength(str(row[7])) > 1): categoria += ', ' + str(row[7])
        s = 'EVENTO: ' + row[0]
        lb.insert(END, s)
        lb.insert(END, "------------------------------------------------------------------------")
        s = "      LUGAR: " + str(row[1]) + " / DIRECCION: " + str(row[2]) + " / POBLACION: " + str(row[3]) + " / FECHA: " + fecha + " / HORARIO: " + str(row[5]) + " / CATEGORIA: " + categoria
        lb.insert(END, s)
        lb.insert(END,"\n\n")
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)


def listar_todos():
    conn = sqlite3.connect('catas.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT TITULO, LUGAR, DIRECCION, POBLACION, FECHA as CONCAT(FECHA_INICIAL, ' - ', FECHA_FINAL), HORARIO, CATEGORIA FROM CATA")
    conn.close
    listar_catas(cursor)
    
    
def listar_nocturnos():
    conn = sqlite3.connect('catas.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT TITULO, LUGAR, DIRECCION, POBLACION, FECHA as CONCAT(FECHA_INICIAL, ' - ', FECHA_FINAL), HORARIO, CATEGORIA FROM CATA WHERE HORARIO > '19:00'")
    conn.close
    listar_catas(cursor)  
  
def ventana_principal():       
    root = Tk()
    root.geometry("150x100")

    menubar = Menu(root)
    
    datosmenu = Menu(menubar, tearoff=0)
    datosmenu.add_command(label="Cargar", command=almacenar_bd)
    datosmenu.add_separator()   
    datosmenu.add_command(label="Salir", command=root.quit)
    
    menubar.add_cascade(label="Datos", menu=datosmenu)
    
    buscarmenu = Menu(menubar, tearoff=0)
    buscarmenu.add_command(label="Eventos", command=listar_catas)
    #buscarmenu.add_command(label="Eventos por la noche", command=listar_nocturnos())
    
    menubar.add_cascade(label="Listar", menu=buscarmenu)
    
    buscarmenu = Menu(menubar, tearoff=0)
    buscarmenu.add_command(label="Fecha de celebracion", command=buscar_por_celebracion)
    #buscarmenu.add_command(label="Eventos por categoria", command=buscar_por_categoria())
    
    menubar.add_cascade(label="Buscar", menu=buscarmenu)
        
    root.config(menu=menubar)
    root.mainloop()

    

if __name__ == "__main__":
    ventana_principal()