#encoding:utf-8
from main.models import Producto

from bs4 import BeautifulSoup
import urllib.request
import lxml

PAGINAS = 3
        
def populateDB():
    
    Producto.objects.all().delete()
  
    for p in range(1,PAGINAS+1):
        url="https://tienda.bricogeek.com/5-arduino?p="+str(p)
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f,"lxml")      
        
        l = s.find_all("li", class_= "ajax_block_product")

        for i in l:
                        
            nombre = i.find("meta", itemprop= "name")["content"]
            imagen = i.find("meta", itemprop= "image")["content"]
            precio = i.find("meta", itemprop= "lowPrice")["content"]
            url1 = i.find("a", class_= "product_img_link")["href"]
            f1 = urllib.request.urlopen(url1)
            s1 = BeautifulSoup(f1, 'lxml')
            
            referencia = s1.find("span", itemprop= "sku").string.strip()
            descripcion = s1.find("div", id= "short_description_content").getText();
            
            producto_obj = Producto.objects.get_or_create(nombre=nombre, imagen=imagen, 
                                                      precio=precio, referencia=referencia,
                                                      descripcion=descripcion)
        
    return Producto.objects.count()
