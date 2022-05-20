#encoding:utf-8
from django import forms
from main.models import Producto

class BusquedaPorPrecioForm(forms.Form):
    precio = forms.FloatField(label="Introduzca el precio máximo", required=False, min_value=0) 
    
class BusquedaPorNombreForm(forms.Form):
    nombre = forms.Field(label="Introduzca nombre", required=False) 
