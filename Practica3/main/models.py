#encoding:utf-8

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from numpy.f2py.crackfortran import verbose
from django.template.defaultfilters import default

class Genero(models.Model):
    nombre = models.TextField(primary_key=True, verbose_name='Genero')

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering =('nombre', )

class Anime(models.Model):
    idAnime = models.TextField(primary_key=True, verbose_name='idAnime')
    titulo = models.TextField(verbose_name='Título')
    generos = models.ManyToManyField(Genero)
    formato = models.TextField(verbose_name='Formato')
    nEpisodios = models.IntegerField(verbose_name='nEpisodios', default = 0)

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ('titulo', )

class Puntuacion(models.Model):
    idUsuario = models.IntegerField(verbose_name='idUsuario')
    idAnime = models.ForeignKey(Anime,on_delete=models.CASCADE, verbose_name='idAnime')
    puntuacion = models.IntegerField(verbose_name='Puntuación', validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    def __str__(self):
        return (str(self.puntuacion))
    
    class Meta:
        ordering=('idAnime','idUsuario', )