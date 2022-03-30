#encoding: utf-8

class Corcho:
        def __init__(self,nombre):
            self.bodega = nombre

class Botella:
        def __init__(self,corcho):
            self.corcho=corcho
            print ('Botella de la bodega',corcho.bodega)
             
class Sacacorcho:
        def __init__(self):
            self.corcho=None

        def destapar(self,botella):
            print ('descorchar')
            self.corcho=botella.corcho
            botella.corcho=None
            
        def limpiar(self):
            self.corcho=None
            print ('limpiar')

class Objeto:
        def __init__(self):
            corcho=Corcho('Yllera')
            botella=Botella(corcho)
            sacacorcho=Sacacorcho()
            sacacorcho.destapar(botella)
            sacacorcho.limpiar()
            
if __name__ == "__main__":
    objeto = Objeto()
