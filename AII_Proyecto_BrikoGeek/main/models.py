#encoding:utf-8
from django.db import models

#datos de los productos
class Producto(models.Model):
    nombre = models.TextField(verbose_name='Nombre')
    imagen = models.URLField(verbose_name='URL de Imagen')
    referencia = models.TextField(verbose_name='Referencia')
    precio = models.FloatField(default=0, verbose_name='Precio')
    descripcion = models.TextField(verbose_name='Descripcion')
    
    def __str__(self):
        return self.nombre
