#encoding: utf-8

class Cadena:
    
    def exercise_1a(self, s, c):
        return ",".join(list(s))
    
    def exercise_1b(self, s):
        return s.replace(' ', '_')
    
    def exercise_1c(self, s):
        translation = str.maketrans('0123456789', 'XXXXXXXXXX')
        return s.translate(translation)
    
    def exercise_1d(self, s):
        l = []
        i = 0
        for x in s:
            l.append(x)
            i+=1
            if i == 3:
                l.append('.')
                i = 0
        return "".join(l)
    
    def exercise_2a(self, s1, s2):
        return s2 in s1
    
    def exercise_2b(self, s1, s2):
        if s1.lower() < s2.lower():
            return s1
        else: 
            return s2