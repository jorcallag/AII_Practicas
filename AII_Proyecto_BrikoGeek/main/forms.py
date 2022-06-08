#encoding:utf-8
from django import forms
from main.models import Producto

from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, NUMERIC, KEYWORD, ID
from whoosh.qparser import QueryParser
from whoosh import qparser, query
from numpy.random.mtrand import choice

dirindex="Index"

class BusquedaPorPrecioForm(forms.Form):
    precio = forms.FloatField(label="Introduzca el precio máximo", required=False, min_value=0) 
    
class BusquedaPorNombreForm(forms.Form):
    nombre = forms.Field(label="Introduzca el nombre del producto", required=False) 
    
class BusquedaPorCategoriaForm(forms.Form):
    ix=open_dir("Index")      
    with ix.searcher() as searcher:
        lista_categorias = [(i.decode('utf-8'), i.decode('utf-8')) for i in searcher.lexicon('categoria')]
        
    categoria = forms.ChoiceField(label="Seleccione una categoria", choices = lista_categorias)
    
class BusquedaPorTituloForm(forms.Form):
    titulo = forms.Field(label="Introduzca el titulo del articulo", required=False) 
