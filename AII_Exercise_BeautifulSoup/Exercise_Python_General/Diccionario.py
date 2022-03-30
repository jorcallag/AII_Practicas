#encoding: utf-8

class Diccionario:

        def exercise_1a(self,d):
            while True:
                nombre = input('Introduzca nombre: ')
                if nombre == '*':
                    break
                if nombre in d:
                    print ('Teléfono', d[nombre])
                    respuesta = input('Es correcto(s/n)? ')
                    if respuesta == 'n':
                        numero = input('Introduzca el nuevo número ')
                        d[nombre] = numero
                else:
                    numero = input('Introduzca un teléfono para el nuevo nombre')
                    d[nombre] = numero
            print (d)
