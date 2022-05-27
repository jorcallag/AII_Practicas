#encoding:utf-8
from django import forms
from main.models import Genero
   
class GeneroBusquedaForm(forms.Form):
    genero = forms.ModelChoiceField(label="Seleccione un genero ", queryset=Genero.objects.all())
    
class UsuarioBusquedaForm(forms.Form):
    idUsuario = forms.CharField(label="Id de Usuario", widget=forms.TextInput, required=True)
    
class UsuarioFormatoBusquedaForm(forms.Form):
    idUsuario = forms.CharField(label="Id de Usuario", widget=forms.TextInput, required=True)
    formato = forms.CharField(label="Formato", widget=forms.TextInput, required=True)