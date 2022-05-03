#encoding:utf-8
from main.models import Pelicula, Usuario, Ocupacion

from bs4 import BeautifulSoup
import urllib.request
import lxml
from datetime import datetime

path = "data"

#función auxiliar que hace scraping en la web y carga los datos en la base datos
def populateUsuario():
    
    Usuario.objects.all().delete()
    
    lista=[]
    fileobj=open(path+"\\u.user", "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        lista.append(Usuario(idUsuario=int(rip[0].strip()), edad=int(rip[1].strip()), genero=str(rip[2].strip()), ocupacion=Ocupacion.objects.get(nombre=str(rip[3].strip())), codigoPostal=int(rip[4].strip())))
    fileobj.close()
    Usuario.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    return len(lista)
        
def populateOcupacion():
    
    Ocupacion.objects.all().delete()
    
    lista=[]
    fileobj=open(path+"\\u.occupation", "r")
    for line in fileobj.readlines():
        lista.append(Ocupacion(nombre=str(line)))
    fileobj.close()
    Usuario.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    return len(lista)