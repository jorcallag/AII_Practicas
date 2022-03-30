#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3
import lxml

# lineas para evitar error SSL
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def cargar():
    respuesta = messagebox.askyesno(title="Confirmar",message="Esta seguro que quiere recargar los datos. \nEsta operaciÃ³n puede ser lenta")
    if respuesta:
        almacenar_bd()

def extraer_elementos():
    lista=[]
    
    for num_paginas in range(1,2):
        url = "https://zacatrus.es/juegos-de-mesa.html?p="+str(num_paginas)
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f, 'lxml')
        lista_una_pagina = s.ol.find_all("div", class_="product-item-details")
        lista.extend(lista_una_pagina)
        
    return lista


def almacenar_bd():
    conn = sqlite3.connect('juego.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS JUEGO")
    conn.execute('''CREATE TABLE JUEGO
       (TITULO        TEXT NOT NULL,
        VOTOS         REAL,
        PRECIO        REAL,
        TEMATICA      TEXT,          
        COMPLEJIDAD   TEXT);''')

    lista_juego = extraer_elementos()
    
    for juego in lista_juego:
        titulo = juego.find("a", class_=["product-item-link"]).string.strip()
        votos = juego.find("div", class_=["rating-result"])
        if votos: 
            votos = votos['title']
            votos = re.compile('\d+').search(votos).group()
        else:
            votos = -1
        precio  = juego.find("span",class_=["price"]).string.strip()
        precio = re.compile('\d+,\d+').search(precio).group()
        print(precio)
        
        #tematica = "".join(datos.find("div",class_=["tags"]).stripped_strings)
        #complejidad = list(vino.find("p",class_=["price"]).stripped_strings)[0]

        conn.execute("""INSERT INTO JUEGO (TITULO, VOTOS, PRECIO) VALUES (?,?,?)""",
                     (titulo, votos, float(precio.replace(',','.'))))
        conn.commit()

    cursor = conn.execute("SELECT COUNT(*) FROM JUEGO")
    messagebox.showinfo("Base Datos",
                        "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()

def listar_todos():
    conn = sqlite3.connect('juego.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT TITULO, VOTOS, PRECIO, TEMATICA, COMPLEJIDAD FROM JUEGO")
    conn.close
    listar_juegos(cursor)

    
def listar_juegos(cursor):      
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        s = 'JUEGO: ' + row[0]
        lb.insert(END, s)
        lb.insert(END, "------------------------------------------------------------------------")
        s = "     VOTOS: " + str(row[1]) + '%' + ' | PRECIO: ' + str(row[2]) + '€'#+ ' | TEMATICA: ' + row[3]+ ' | COMPLEJIDAD: ' + row[4]
        lb.insert(END, s)
        lb.insert(END,"\n\n")
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)

def ventana_principal():
    raiz = Tk()

    menu = Menu(raiz)

    #DATOS
    menudatos = Menu(menu, tearoff=0)
    menudatos.add_command(label="Cargar", command=cargar)
    menudatos.add_command(label="Listar", command=listar_todos)
    menudatos.add_command(label="Salir", command=raiz.quit)
    menu.add_cascade(label="Datos", menu=menudatos)

    raiz.config(menu=menu)

    raiz.mainloop()

if __name__ == "__main__":
    ventana_principal()