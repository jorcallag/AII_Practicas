#encoding: utf-8

from Exercise_Python_General.Cadena import Cadena
from Exercise_Python_General.Lista import Lista
from Exercise_Python_General.Busqueda import Busqueda
from Exercise_Python_General.Diccionario import Diccionario

cadenas = Cadena()
print(cadenas.exercise_1a('123456789', ','))
print(cadenas.exercise_1b('mi archivo de texto.txt'))
print(cadenas.exercise_1c('Su clave es: 1540'))
print(cadenas.exercise_1d('2552552550'))  
print(cadenas.exercise_2a('subcadena','cadena')) 
print(cadenas.exercise_2b('kde','Gnome'))

print("\n-------------------------------------------------\n")

listas = Lista()
listas.exercise_1a(('Luis', 'Marta', 'Paula'))
listas.exercise_1b(('Luis', 'Marta', 'Paula','Luis'), 1, 2)            
listas.exercise_1c((('Luis', 'h'), ('Marta', 'm'), ('Paula', 'm')))
listas.exercise_2a((('García', 'Luis', 'M'), ('Carrillo', 'Marta', 'J'), ('Fernández', 'Paula', 'M')))

print("\n-------------------------------------------------\n")

busquedas = Busqueda()
busquedas.exercise_1a((('Jorge García', '12345'), ('Luisa Montero', '54321'), ('Inés Roca Díaz', '67890')), 'García')

print("\n-------------------------------------------------\n")

diccionario = Diccionario()
diccionario.exercise_1a({'Jorge':'12345', 'Luisa':'54321', 'Marta':'67890'})

print("\n-------------------------------------------------\n")






