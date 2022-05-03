#encoding:utf-8
from principal.models import Temporada, Equipo, Jornada, Partido

from bs4 import BeautifulSoup
import urllib.request
import re

TEMP_INI = 2015 # temporada inicial a cargar
NUM_TEMP = 6 # número de temporadas

def populateDatabase():
    
    #borrar tablas
    Temporada.objects.all().delete()
    Equipo.objects.all().delete()
    Jornada.objects.all().delete()
    Partido.objects.all().delete()
    
    #cargamos NUM_TEMP temporadas desde la TEMP_INI
    temporadas = [str(TEMP_INI+t)+'_'+str(TEMP_INI+1++t) for t in range(0,NUM_TEMP)]

    for temporada in temporadas:
        f = urllib.request.urlopen("http://resultados.as.com/resultados/futbol/primera/"+temporada+"/calendario/")
        s = BeautifulSoup(f,"lxml")
        #creamos la temporada
        tem = Temporada.objects.create(anyo=int(temporada[:4]))
        
        for i in s.find_all("div", class_= ["cont-modulo","resultados"]):
            numero = int(re.compile('\d+').search(i['id']).group(0))
            fecha = i.find("span", class_=["fecha-evento"]).string.strip()
            #creamos la jornada
            jor = Jornada.objects.create(temporada=tem, numero=numero, fecha = fecha)
            
            partidos = i.find_all("tr",id=True)
            for p in partidos:
                equipos= p.find_all("span",class_="nombre-equipo")
                
                nombre_local = equipos[0].string.strip().lower()
                link_local = equipos[0].parent['href']
                #si el equipo no existe se crea
                local, created = Equipo.objects.get_or_create(nombre=nombre_local)
                #si es un equipo nuevo se le añaden todos los campos
                if created:
                    if not crearEquipo(nombre_local,link_local):
                        print("No se ha podido modificar el equipo "+nombre_local)
                    
                nombre_visitante = equipos[1].string.strip().lower()
                link_visitante = equipos[1].parent['href']
                #si el equipo no existe se crea
                visitante, created = Equipo.objects.get_or_create(nombre=nombre_visitante)
                #si es un equipo nuevo se le añaden todos los campos
                if created:
                    if not crearEquipo(nombre_visitante,link_visitante):
                        print("No se ha podido modificar el equipo "+nombre_visitante)
                resultado_enlace = p.find("a",class_="resultado")
                if resultado_enlace != None:
                    goles=re.compile('(\d+).*(\d+)').search(resultado_enlace.string.strip())
                    goles_l=int(goles.group(1))
                    goles_v=int(goles.group(2))
                    
                    par = Partido.objects.create(jornada=jor, local=local, visitante=visitante, goles_local=goles_l, goles_visitante=goles_v)
              
    return True

def crearEquipo(nombre,link):
    try:
        f = urllib.request.urlopen("https://resultados.as.com" + link)
        s = BeautifulSoup(f,"lxml")
        
        info = s.find("section", class_="info-social")
        
        fundacion = info.find("strong", itemprop="foundingDate").string.strip()
        estadio = info.find(string=re.compile("Sede:")).parent.strong.string.strip()
        aforo = info.find(string=re.compile("Aforo:")).parent.strong.string.strip()
        if (info.find(string=re.compile("Dirección:"))):
            direccion = info.find(string=re.compile("Dirección:")).parent.strong.string.strip()
        else:
            direccion = "Desconocida"
        Equipo.objects.filter(nombre=nombre).update(fundacion= int(fundacion), estadio = estadio, aforo = int(aforo), direccion = direccion)       
    except:
        return False
    else:
        return True


