#encoding:utf-8
from django.db import models
from django.contrib.admin.utils import help_text_for_field
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.enums import Choices

class Usuario(models.Model):
    idUsuario = models.IntegerField(primary_key=True, verbose_name='idUsuario')
    edad = models.PositiveSmallIntegerField(max_length=2, verbose_name= 'Edad')
    sexo = models.CharField(max_length=1, verbose_name= 'Sexo', help_text_for_field= 'M/F')
    ocupacion = models.ForeignKey(verbose_name= 'Ocupacion')
    codigoPostal = models.TextField(max_length=5, verbose_name='Codigo Postal')
    
    def __str__(self):
        return self.idUsuario
    
class Pelicula(models.Model):
    idPelicula = models.IntegerField(primary_key=True, verbose_name='idPelicula')
    titulo = models.TextField(verbose_name='Título')
    fechaEstreno = models.DateField(verbose_name='Fecha de Estreno')
    IMDbURL = models.URLField(verbose_name='Url')
    categoria = models.ForeignKey(verbose_name='Categoria')

    def __str__(self):
        return self.idPelicula
    
class Categoria(models.Model):
    idCategoria = models.IntegerField(primary_key=True, verbose_name='idCategoria')
    nombre = models.CharField(max_length=30, verbose_name='Nombre')

    def __str__(self):
        return self.idCategoria
    
class Ocupacion(models.Model):
    idOcupacion = models.AutoField(primary_key=True, verbose_name='idOcupacion')
    nombre = models.CharField(max_length=30,verbose_name='Nombre')

    def __str__(self):
        return self.nombre
    
class Puntuacion(models.Model):
    Puntuaciones = ((1, "Muy mala"), (2, "Mala"), (3, "Regular"), (4, "Buena"), (5, "Muy buena"))
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idPelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(verbose_name='Puntuacion', validators=[MinValueValidator(0), MaxValueValidator(5)], Choices=Puntuaciones)

    def __str__(self):
        return self.puntuacion
    



    
