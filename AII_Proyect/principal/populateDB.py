#encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
import lxml
from principal.models import Articulo

PAGINAS = 1  #numero de paginas

#función auxiliar que hace scraping en la web y carga los datos en la base datos
def populateDB():
    
    #borramos todas las tablas de la BD
    Articulo.objects.all().delete()
    
    #extraemos los datos de la web con BS
    for p in range(1,PAGINAS+1):
        url="https://www.prozis.com/es/es/alimentacion-saludable/q/page/"+str(p)
        f = urllib.request.urlopen(url)
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
                      
            p = Articulo.objects.create(nombre = nombre, precio = precio,
                                    infoNutricional = infoNutricional,
                                    valorEnergetico = valorEnergetico,                               
                                    grasas = grasas,
                                    grasasSaturadas = grasasSaturadas,
                                    hidratosDeCarbono = hidratosDeCarbono,
                                    azucares = azucares,
                                    proteinas = proteinas,
                                    sal = sal)          
        
    return Articulo.objects.count()
    

        