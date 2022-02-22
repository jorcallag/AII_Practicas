#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3
import os, ssl  # lineas para evitar error SSL

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and 
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

TEMPORADA="2017_2018"

def extraer_jornadas():
    url="http://resultados.as.com/resultados/futbol/primera/"+TEMPORADA+"/calendario/"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f)
    
    l = s.find_all("div", class_= ["cont-modulo","resultados"])
    return l

def imprimir_lista(cursor):
    v = Toplevel()
    v.title("TEMPORADA "+TEMPORADA)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand=sc.set)
    jornada=0
    for row in cursor:
        if row[0] != jornada:
            jornada=row[0]
            lb.insert(END,"\n")
            s = 'JORNADA '+ str(jornada)
            lb.insert(END,s)
            lb.insert(END,"-----------------------------------------------------")
        s = "     " + row[1] +' '+ str(row[3]) +'-'+ str(row[4]) +' '+  row[2]
        lb.insert(END,s)
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command = lb.yview)

 
def almacenar_bd():
    conn = sqlite3.connect('as.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS JORNADAS") 
    conn.execute('''CREATE TABLE JORNADAS
       (JORNADA       INTEGER NOT NULL,
       LOCAL          TEXT    NOT NULL,
       VISITANTE      TEXT    NOT NULL,
       GOLES_L        INTEGER    NOT NULL,
       GOLES_V        INTEGER NOT NULL,
       LINK           TEXT);''')
    l = extraer_jornadas()
    for i in l:
        jornada = int(re.compile('\d+').search(i['id']).group(0))
        partidos = i.find_all("tr",id=True)
        for p in partidos:
            equipos= p.find_all("span",class_="nombre-equipo")
            local = equipos[0].string.strip()
            visitante = equipos[1].string.strip()
            resultado_enlace = p.find("a",class_="resultado")
            if resultado_enlace != None:
                goles=re.compile('(\d+).*(\d+)').search(resultado_enlace.string.strip())
                goles_l=goles.group(1)
                goles_v=goles.group(2)
                link = resultado_enlace['href']
                
                conn.execute("""INSERT INTO JORNADAS VALUES (?,?,?,?,?,?)""",(jornada,local,visitante,goles_l,goles_v,link))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM JORNADAS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()


def listar_bd():
    conn = sqlite3.connect('as.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT * FROM JORNADAS ORDER BY JORNADA")
    imprimir_lista(cursor)
    conn.close()
    
def buscar_jornada():
    def aux():
        conn = sqlite3.connect('as.db')
        conn.text_factory = str  
        cursor = conn.execute("SELECT * FROM JORNADAS WHERE JORNADA = ?", (E1.get(),))
        imprimir_lista(cursor)
        conn.close()
        
    v = Toplevel()
    v.title("Buscar jornada")
    L1 = Label(v, text = "Jornada número:")
    L1.pack( side = LEFT)
    E1 = Entry(v, bd = 5)
    E1.pack(side = LEFT)
    buscar = Button(v, text="Buscar", command = aux)
    buscar.pack(side = RIGHT)
  
def ventana_principal():
    top = Tk()
    top.title("TEMPORADA "+ TEMPORADA)
    almacenar = Button(top, text="Almacenar Resultados", command = almacenar_bd)
    almacenar.pack(side = TOP)
    listar = Button(top, text="Listar Jornadas", command = listar_bd)
    listar.pack(side = TOP)
    buscar = Button(top, text="Buscar Jornada", command = buscar_jornada)
    buscar.pack(side = TOP)
    top.mainloop()
    

if __name__ == "__main__":
    ventana_principal()