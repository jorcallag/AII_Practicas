#encoding: utf-8

class Lista:
        
    def exercise_1a(self, t):
        for e in t:
            print("Estimado/a", e, "vote por mi")
            
    def exercise_1b(self, t, p, n):
        x = t[p:p+n]
        self.exercise_1a(x)
    
    def exercise_1c(self, t):
        for e in t:
            if e[1]=='h':
                print("Estimado", e[0], "vote por mi")
            else:
                print("Estimada", e[0], "vote por mi")
                
    def exercise_2a(self, t):
        for e in t:
            print(e[1], e[2],".", e[0])