#encoding:utf-8
from django.db import models

class Articulo(models.Model):
    
    idArticulo = models.AutoField(primary_key=True, verbose_name='idArticulo')
    nombre = models.TextField(verbose_name='Nombre')
    precio = models.TextField(verbose_name='Precio')
    valorEnergetico = models.TextField(verbose_name='Valor Energetico')
    grasas = models.TextField(verbose_name='Grasas')
    grasasSaturadas = models.TextField(verbose_name='Grasas Saturadas')
    hidratosDeCarbono = models.TextField(verbose_name='Hidratos de Carbono')
    azucares = models.TextField(verbose_name='Azucares')
    proteinas = models.TextField(verbose_name='Proteinas')
    sal = models.TextField(verbose_name='Sal')

    def __str__(self):
        return self.nombre
    
