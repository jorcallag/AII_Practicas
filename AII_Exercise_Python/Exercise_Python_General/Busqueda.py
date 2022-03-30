#encoding: utf-8

class Busqueda:
    
    def exercise_1a(self, t, s):
        for e in t:
            if s in e[0]:
                print("Nombre:", e[0])
                print("Telefono:", e[1])