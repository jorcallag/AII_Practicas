#encoding: utf-8

class Personaje:
    
        def __init__(self):
            self.vida=100
            self.posicion={"Norte":0,"Sur":0,"Este":0,"Oeste":0}  # Diccionario con la coordenadas [Norte, Sur, Este, Oeste] 
            self.velocidad=10
            
        def recibir_ataque(self,fuerza):
            self.vida = self.vida - fuerza
            if self.vida <= 0:
                print ("Te has quedado sin vida")
            else:
                print ("Te queda", self.vida, "vida")
                
        def mover(self, direccion):
            self.posicion[direccion] = self.posicion[direccion]+self.velocidad

class Soldado(Personaje):
    
        def __init__(self):
            Personaje.__init__(self)
            self.ataque = 10
            
        def atacar(self, personaje):
            personaje.recibir_ataque(self.ataque)
                
class Campesino(Personaje):
    
        def __init__(self):
            Personaje.__init__(self)
            self.cosecha = 10
        def cosechar(self):
            return self.cosecha
        
class Herencia:
    
    def __init__(self):
            soldado=Soldado()
            campesino=Campesino()
            soldado.atacar(campesino)
            soldado.atacar(campesino)
            print (campesino.cosechar())
                
if __name__ == "__main__":
    herencia=Herencia()
